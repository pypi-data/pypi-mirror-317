# -*- coding: utf-8 -*-
def is_equal_to_13(value):
    dict13 = {
            "num":13,
            "char":"13",
            "roman":"XIII",
            "zh-cn":"十三",
            "zh-cnL":"壹拾叁",
            "en-US":"thirteen"
            }
    return value in dict13.values()


def is_equal_to_4(value):
    dict13 = {
            "num":4,
            "char":"4",
            "roman":"IV",
            "zh-cn":"四",
            "zh-cnL":"肆",
            "en-US":"four"
            }
    return value in dict13.values()
