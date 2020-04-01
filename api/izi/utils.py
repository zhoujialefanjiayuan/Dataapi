#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Date    :   18/04/26 16:47:11
#   Desc    :   
#
from .base_client import BaseClient

def client(ak, sk):
    cli = BaseClient(ak, sk)
    return cli


