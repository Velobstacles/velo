# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os


def setUpPackage():
    os.environ['MONGO_URI'] = 'mongodb://localhost/velobstacles'
    os.environ['VELO_DB_NAME'] = 'velobstacles'
