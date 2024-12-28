#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:
# E-mail: gm.zhibo.wang@gmail.com
# Date  :
# Desc  :


from __future__ import print_function, unicode_literals
import sys
import json
import pprint


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
        # 这里使用 _auto_format 来做自动格式处理
        text = self._auto_format(message)
        print(text, file=sys.stdout)
        # 实例化后就删除对象，和原逻辑保持一致
        del self

    @classmethod
    def _auto_format(cls, message):
        """
        根据 message 的类型或内容做自动格式化输出：
        1. 如果是 dict、list 或者能被 JSON 解析，就用 JSON 格式化。
        2. 否则尝试使用 pprint。
        3. 如果都不合适，则直接按字符串输出。
        """
        if isinstance(message, (dict, list)):
            try:
                return json.dumps(message, indent=4, ensure_ascii=False)
            except (TypeError, ValueError):
                # 如果 JSON 序列化失败，则退而使用 pprint
                return pprint.pformat(message)

        if isinstance(message, str):
            # 尝试解析 JSON
            try:
                parsed = json.loads(message)
                # 如果成功，就再转为美观的 JSON 字符串
                return json.dumps(parsed, indent=4, ensure_ascii=False)
            except (json.JSONDecodeError, TypeError, ValueError):
                # 如果无法被解析成 JSON，则直接返回原字符串
                return message

        # 其他类型则用 pprint.pformat
        return pprint.pformat(message)

    @classmethod
    def _get_repr(cls, message, format_mode='auto'):
        """
        将非字符串转化为字符串或其美观形式（根据 format_mode）。
        """
        if format_mode == 'raw':
            # 强制直接转字符串（或 repr）
            return str(message) if isinstance(message, str) else repr(message)

        elif format_mode == 'json':
            # 强制 JSON 格式化
            try:
                return json.dumps(message, indent=4, ensure_ascii=False)
            except (TypeError, ValueError):
                # JSON 不可用就退回到 pprint
                return pprint.pformat(message)

        elif format_mode == 'pprint':
            # 强制 pprint
            return pprint.pformat(message)

        else:
            # 'auto' 模式自动判断
            return cls._auto_format(message)

    @classmethod
    def _print_in_color(cls, message, color='NONE', file=sys.stdout, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        通用的内部打印方法，支持前后缀 & 不同格式化模式。
        """
        text = cls._get_repr(message, format_mode=format_mode)
        print(
            cls.colors[color] + prefix + text + suffix + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def get_colored_string(cls, message, color='NONE', prefix='', suffix='', format_mode='auto'):
        """
        返回带 ANSI 颜色控制符的字符串，但不打印。
        """
        text = cls._get_repr(message, format_mode=format_mode)
        return cls.colors[color] + prefix + text + suffix + cls.colors['ENDC']

    @classmethod
    def debug(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印调试信息(紫色)到 stdout
        """
        cls._print_in_color(message, color='DEBUG', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stdout, **kwargs)

    @classmethod
    def ok(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印普通成功或确认信息(蓝色)到 stdout
        """
        cls._print_in_color(message, color='OK', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stdout, **kwargs)

    @classmethod
    def info(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印普通信息(绿色)到 stdout
        """
        cls._print_in_color(message, color='INFO', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stdout, **kwargs)

    @classmethod
    def warn(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印警告信息(黄色)到 stderr
        """
        cls._print_in_color(message, color='WARNING', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stderr, **kwargs)

    @classmethod
    def err(cls, message, interrupt=False, fatal_message="Fatal error: Program stopped.",
            prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印错误信息(亮红)到 stderr
        interrupt=True 时会停止程序执行并打印 fatal_message
        """
        cls._print_in_color(message, color='ERR', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stderr, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='ERR', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def fatal(cls, message, interrupt=False, fatal_message="Fatal error: Program stopped.",
              prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印致命错误信息(红色)到 stderr
        interrupt=True 时会停止程序执行并打印 fatal_message
        """
        cls._print_in_color(message, color='FATAL', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stderr, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='FATAL', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def custom(cls, message, color_code, prefix='', suffix='', format_mode='auto', file=sys.stdout, **kwargs):
        """
        自定义颜色输出。color_code 是一个 ANSI 转义序列字符串，例如: '\\033[96m' (青色)。
        """
        text = cls._get_repr(message, format_mode=format_mode)
        print(
            color_code + prefix + text + suffix + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def line(cls, length=50, char='-', color='INFO', file=sys.stdout, **kwargs):
        """
        打印一条分割线
        """
        cls._print_in_color(char * length, color=color, file=file, **kwargs)


"""


if __name__ == '__main__':
    # 使用示例
    ColorPrint.info("普通字符串")
    ColorPrint.info('{"hello": "world", "list": [1, 2, 3]}')
    ColorPrint.info({"hello": "world", "list": [1, 2, 3]})
    ColorPrint.warn({"warn_key": True})
    ColorPrint.err("这是一条错误信息", format_mode='pprint')
    ColorPrint.fatal("This is a fatal error.")
    ColorPrint.ok('强制使用 pprint 模式', format_mode='pprint')
    ColorPrint.debug('强制使用 raw 模式', format_mode='raw')
    ColorPrint.line()
    ColorPrint.custom("This is a custom color message in cyan!", "\033[96m")
    ColorPrint.line(char='=', length=60, color='OK')


"""
