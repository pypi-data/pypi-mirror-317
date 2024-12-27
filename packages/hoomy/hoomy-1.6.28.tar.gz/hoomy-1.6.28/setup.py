#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qicongsheng
from setuptools import setup, find_packages
from hoomy import help

setup(
    name='hoomy',
    version=help.get_version(),
    keywords='hoomy',
    description='Development tools for python',
    license='MIT License',
    url='https://github.com/qicongsheng/hoomy',
    author='qicongsheng',
    author_email='qicongsheng@outlook.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[

    ]
)
