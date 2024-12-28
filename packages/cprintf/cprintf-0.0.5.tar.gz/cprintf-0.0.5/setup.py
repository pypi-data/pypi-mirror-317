#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:
# E-mail:
# Date  :
# Desc  :



from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cprintf',
    version="0.0.5",
    author='gm.zhibo.wang',
    author_email='gm.zhibo.wang@gmail.com',
    description='Printing and debugging with color',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/wang-zhibo/cprintf',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)

