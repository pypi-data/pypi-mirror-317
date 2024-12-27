#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:
# E-mail: gm.zhibo.wang@gmail.com
# Date  :
# Desc  :



from __future__ import print_function, unicode_literals
import sys



class ColorPrint:
    """
    A utility class for printing colored text to stdout or stderr in Python.
    """

    colors = {
        'NONE':    '\033[0m',
        'DEBUG':   '\033[95m',  # 紫色
        'OK':      '\033[94m',  # 蓝色
        'INFO':    '\033[92m',  # 绿色
        'WARNING': '\033[93m',  # 黄色
        'ERR':     '\033[91m',  # 亮红
        'FATAL':   '\033[31m',  # 红色
        'ENDC':    '\033[0m',   # 结束符
    }

    def __init__(self, message):
        """
        在实例化时，默认以普通白色输出到 stdout
        """
        print(message, file=sys.stdout)
        del self

    @classmethod
    def _get_repr(cls, message):
        """
        将非字符串转化为字符串或其 repr 形式。
        """
        if isinstance(message, str):
            return message
        return repr(message)

    @classmethod
    def _print_in_color(cls, message, color='NONE', file=sys.stdout, prefix='', suffix='', **kwargs):
        """
        通用的内部打印方法，支持前后缀。
        """
        text = cls._get_repr(message)
        print(
            cls.colors[color] + prefix + text + suffix + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def get_colored_string(cls, message, color='NONE', prefix='', suffix=''):
        """
        返回带 ANSI 颜色控制符的字符串，但不打印。
        """
        text = cls._get_repr(message)
        return cls.colors[color] + prefix + text + suffix + cls.colors['ENDC']

    @classmethod
    def debug(cls, message, prefix='', suffix='', *args, **kwargs):
        """
        打印调试信息(紫色)到 stdout
        """
        cls._print_in_color(message, color='DEBUG', prefix=prefix, suffix=suffix, file=sys.stdout, *args, **kwargs)

    @classmethod
    def ok(cls, message, prefix='', suffix='', *args, **kwargs):
        """
        打印普通成功或确认信息(蓝色)到 stdout
        """
        cls._print_in_color(message, color='OK', prefix=prefix, suffix=suffix, file=sys.stdout, *args, **kwargs)

    @classmethod
    def info(cls, message, prefix='', suffix='', *args, **kwargs):
        """
        打印普通信息(绿色)到 stdout
        """
        cls._print_in_color(message, color='INFO', prefix=prefix, suffix=suffix, file=sys.stdout, *args, **kwargs)

    @classmethod
    def warn(cls, message, prefix='', suffix='', *args, **kwargs):
        """
        打印警告信息(黄色)到 stderr
        """
        cls._print_in_color(message, color='WARNING', prefix=prefix, suffix=suffix, file=sys.stderr, *args, **kwargs)

    @classmethod
    def err(cls, message, interrupt=False, fatal_message="Fatal error: Program stopped.",
            prefix='', suffix='', *args, **kwargs):
        """
        打印错误信息(亮红)到 stderr
        interrupt=True 时会停止程序执行并打印 fatal_message
        """
        cls._print_in_color(message, color='ERR', prefix=prefix, suffix=suffix, file=sys.stderr, *args, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='ERR', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def fatal(cls, message, interrupt=False, fatal_message="Fatal error: Program stopped.",
              prefix='', suffix='', *args, **kwargs):
        """
        打印致命错误信息(红色)到 stderr
        interrupt=True 时会停止程序执行并打印 fatal_message
        """
        cls._print_in_color(message, color='FATAL', prefix=prefix, suffix=suffix, file=sys.stderr, *args, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='FATAL', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def custom(cls, message, color_code, prefix='', suffix='', file=sys.stdout, *args, **kwargs):
        """
        自定义颜色输出。color_code 是一个 ANSI 转义序列字符串，例如: '\\033[96m' (青色)。
        """
        # 临时颜色字典可以直接扩展，或者仅用于本次调用
        print(
            color_code + prefix + cls._get_repr(message) + suffix + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def line(cls, length=50, char='-', color='INFO', file=sys.stdout, *args, **kwargs):
        """
        打印一条分割线
        """
        cls._print_in_color(char * length, color=color, file=file, *args, **kwargs)




"""
if __name__ == "__main__":
    # 示例测试
    ColorPrint.debug("Debug info")
    ColorPrint.ok("Everything looks good.")
    ColorPrint.info("This is some info.")
    ColorPrint.warn("This is a warning.")
    ColorPrint.err("This is an error message.")
    ColorPrint.fatal("This is a fatal error.")
    ColorPrint.line()
    ColorPrint.custom("This is a custom color message in cyan!", "\033[96m")
    ColorPrint.line(char='=', length=60, color='OK')
"""

