# -*- coding: utf-8 -*-
import os


def setUpPackage():
    os.environ['MONGO_URI'] = 'mongodb://localhost/velobstacles'
