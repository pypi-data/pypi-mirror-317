import datetime
import os
import re
import sys
import importlib.resources
from pathlib import Path
from typing import Iterable

from jinja2 import Template

from ..config import CONFIG
from ..downloader import Downloader, DownloadRequest, DownloadText
from ..log import LOGGER
from ..parse import Parse
from .detail import get as get_proxy_groups
from .vars import dist_file_v, servers_v
from .utils import remove_emoji


class Worker:
    def __init__(self) -> None:
        self.configs = CONFIG.configs

    def download(self) -> Iterable[DownloadText]:
        downloader = Downloader(default_store_path=self.configs["store_path"])
        d = [i for i in CONFIG.configs["subscriptions"]]
        s = [
            DownloadRequest(
                i["url"], i["name"], i["dist"], datetime.timedelta(seconds=i["expire"])
            )
            for i in d
        ]
        download_resps: Iterable[DownloadText] = downloader.downloads(s)
        return download_resps

    def parse(self, download_resps: Iterable[DownloadText]):
        servers = []
        erros = 0
        for resp in download_resps:
            if resp.text is None:
                LOGGER.error("下载失败 %s", resp.url)
                erros += 1
                continue
            suffix = resp.dist.suffix.strip(".")
            tag = resp.name
            dist_file_v.set(resp.dist)
            for i in Parse.parse(resp.text, suffix, tag).res:
                i["name"] = i["name"].replace(" ", "")
                servers.append(i)
        if erros:
            sys.exit(1)
        exclude_server_regex = re.compile(
            r"|".join(
                [re.escape(keyword) for keyword in self.configs["servers"]["exclude"]]
            )
        )
        # LOGGER.debug(servers)
        servers = [
            server
            for server in servers
            if not re.findall(exclude_server_regex, server["name"])
        ]
        servers.sort(key=lambda x: x["name"])
        return servers

    def check(self, proxy_group, rules):
        action_set = set()
        group_set = set()
        for _, _, action in rules[:-1]:
            action_set.add(action)
        for group in proxy_group:
            group_set.add(group["name"])
        if "DIRECT" in action_set:
            action_set.remove("DIRECT")
        if "REJECT" in action_set:
            action_set.remove("REJECT")
        diffs = action_set.difference(group_set)
        if diffs:
            LOGGER.error("这些转发组没有设置：%s", ",".join(list(diffs)))
            raise TypeError()

    def combine(self):
        frame = CONFIG.configs["frame"]
        frame["proxies"] = self.server
        frame["proxy-groups"] = self.proxy_groups
        frame["rules"] = self.rules
        return frame

    def do(self):
        download_resps = self.download()
        servers = self.parse(download_resps)
        servers_v.set(servers)
        if template_path := CONFIG.configs.get("template_path", None):
            with open(template_path) as _f:
                tmp_str = _f.read()
        else:
            with importlib.resources.as_file(
                importlib.resources.files("dae_transer.static")
                / Path("config.dae.jinja2")
            ) as f:
                with open(f) as _f:
                    tmp_str = _f.read()
        tpl = Template(tmp_str)
        groups_ = get_proxy_groups()
        for i in servers:
            i["name"] = remove_emoji(i["name"])
        groups = {}
        for group, nodes in groups_.items():
            groups[group] = ", \n               ".join(
                sorted((remove_emoji(i) for i in nodes), key=lambda x:x.upper())
            )
        res = tpl.render(nodes=servers, groups=groups)

        dist_file = Path(self.configs.get("dist_file"))
        if not dist_file.is_absolute():
            dist_file = Path(os.getcwd()) / dist_file
        with open(dist_file, "w") as f:
            f.write(res)
            LOGGER.info("新的 dae 配置文件写入 %s", dist_file.as_posix())
        dist_file.chmod(0o600)
