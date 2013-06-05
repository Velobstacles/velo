# -*- coding: utf-8 -*-
import os


def setUpPackage():
    os.environ['MONGO_URI'] = 'mongodb://localhost'
    os.environ['MONGO_DB_NAME'] = 'velo_test'


def tearDownPackage():
    remove_test_database()
    del os.environ['MONGO_URI']
    del os.environ['MONGO_DB_NAME']


def remove_test_database():
    from pyramid_mongokit import SingleDbConnection
    connection = SingleDbConnection(
        os.environ['MONGO_DB_NAME'],
        '',
        os.environ['MONGO_URI']
        )
    connection.drop_database(os.environ['MONGO_DB_NAME'])
