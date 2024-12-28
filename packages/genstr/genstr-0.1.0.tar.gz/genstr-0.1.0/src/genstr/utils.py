import re
from enum import Enum


class Mode(Enum):
    PURE_NUMBERS = 1 # 纯数字
    PURE_LETTERS = 2 # 纯字母
    PURE_NUMBERS_LETTERS = 3 # 纯数字+纯字母
    MIXED_CHARACTERS = 4 # 字符混合
    MIXED_EXCLUDE_PURE = 5 # 字符混合，杂米：所有-纯字母-纯数字
    CUSTOM_CHARACTERS = 6 # 自定义字符
    CUSTOM_EXCLUDE_PURE = 7 # 自定义字符：所有-纯字母-纯数字
    CUSTOM_PURE_NUMBERS_LETTERS= 8 # 自定义字符：纯字母+纯数字

def is_characters(s):
    '''
    正则表达式匹配只包含数字或字母的字符串
    '''
    return bool(re.fullmatch(r'[a-zA-Z0-9]*', s))
