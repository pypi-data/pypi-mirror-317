import re
from itertools import chain

from pypinyin import Style, pinyin

from dae_transer.log import LOGGER

# 匹配常见的 emoji 范围和 [ ] &
emoji_and_symbols_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # 表情符号 (😀-🙏)
    "\U0001F300-\U0001F5FF"  # 各种符号和图标
    "\U0001F680-\U0001F6FF"  # 运输和地图符号
    "\U0001F1E0-\U0001F1FF"  # 国旗（区域指示符）
    "\U00002702-\U000027B0"  # 杂项符号
    "\U000024C2-\U0001F251"  # 补充符号
    "\[\]&"                  # 添加 [ ] 和 &
    "]+",
    flags=re.UNICODE
)


def remove_emoji(text: str):
    text2 = "".join(chain(*pinyin(text, style=Style.TONE3)))
    text2 = emoji_and_symbols_pattern.sub(r'', text2)
    return text2
    # return emoji_pattern.sub(r'', text).replace("[", "_").replace("]", "")