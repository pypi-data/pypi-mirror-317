#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:
# E-mail:
# Date  :
# Desc  :



from .color_print import ColorPrint


debug = ColorPrint.debug
info = ColorPrint.info
ok = ColorPrint.ok
warn = ColorPrint.warn
err = ColorPrint.err
fatal = ColorPrint.fatal
custom = ColorPrint.custom
line = ColorPrint.line

__all__ = [
    "ColorPrint",
    "debug",
    "ok",
    "info",
    "warn",
    "err",
    "fatal",
    "custom",
    "line",
]


