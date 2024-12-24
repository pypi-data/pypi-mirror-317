import re
from datetime import datetime

from funcy import group_by

from ..log import LOGGER
from .vars import servers_v


def group(seq, f):
    _tmp = group_by(f, seq)
    return _tmp[True], _tmp[False]


HK_REGEX = re.compile(r"🇭🇰|香港|HK|HongKong", re.IGNORECASE)
TW_REGEX = re.compile(r"🇨🇳|台湾|TW|Taiwan", re.IGNORECASE)
SG_REGEX = re.compile(r"🇸🇬|新加坡|SG|Singapore", re.IGNORECASE)
JP_REGEX = re.compile(r"🇯🇵|日本|JP|Japan", re.IGNORECASE)
KR_REGEX = re.compile(r"🇰🇷|韩国|KR|KOR|Korea", re.IGNORECASE)
US_REGEX = re.compile(r"🇺🇸|USA|US|美国", re.IGNORECASE)
EU_REGEX = re.compile(
    (
        r"🇬🇧|🇫🇷|🇳🇱|🇪🇸|🇩🇪|🇮🇪|UK|GBR|英国|DNK|NLD|Netherlands|POL|"
        r"西班牙|ESP|法国|FRA|德国|DEU|Germany|France"
        r"|Switzerland|Sweden|Austria|Ireland|Hungary"
        r"|Ireland|Ireland"
    ),
    re.IGNORECASE,
)
AUS_RUS_REGEX = re.compile(r"🇷🇺|🇦🇺|RUS|俄|澳大利亚|AUS|Russia|Australia", re.IGNORECASE)


def get():
    servers = servers_v.get()
    # rules = rules_v.get()
    proxy_names = [server["name"] for server in servers]
    proxy_names.sort()
    LOGGER.info("共 %d 个服务器信息", len(proxy_names))
    HK, remain = group(proxy_names, lambda name: bool(re.findall(HK_REGEX, name)))
    TW, remain = group(remain, lambda name: bool(re.findall(TW_REGEX, name)))
    SG, remain = group(remain, lambda name: bool(re.findall(SG_REGEX, name)))
    RUS_AUS, remain = group(remain, lambda name: bool(re.findall(AUS_RUS_REGEX, name)))
    US, remain = group(remain, lambda name: bool(re.findall(US_REGEX, name)))
    JP, remain = group(remain, lambda name: bool(re.findall(JP_REGEX, name)))
    KR, remain = group(remain, lambda name: bool(re.findall(KR_REGEX, name)))
    EU, remain = group(remain, lambda name: bool(re.findall(EU_REGEX, name)))
    remain.extend(RUS_AUS)
    Others = remain
    now = datetime.now().strftime("%H-%M-%S")
    others_name = f"O@{now}"
    return {
        "HK": HK,
        "TW": TW,
        "SG": SG,
        "US": US,
        "JP": JP,
        "KR": KR,
        "EU": EU,
        others_name: Others,
    }
