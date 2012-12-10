# -*- coding: utf-8 -*-
import os


def setUpPackage():
    message = 'MONGO_URI not found in environment variables'
    assert 'MONGO_URI' in os.environ, message
