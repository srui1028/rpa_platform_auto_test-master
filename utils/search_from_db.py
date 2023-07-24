#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:search_from_db.py
@time:2021/12/28
"""
import os
from urllib import parse

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.config_manager import get_config


# data_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (
#     get_config().get('test', 'data_db_user'), get_config().get('test', 'data_db_passwd'),
#     get_config().get('test', 'data_db_host'),
#     get_config().get('test', 'data_db_port'), get_config().get('test', 'data_db_name')))
#
# rpa_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (
#     get_config().get('test', 'rpa_db_user'), get_config().get('test', 'rpa_db_passwd'),
#     get_config().get('test', 'rpa_db_host'),
#     get_config().get('test', 'rpa_db_port'), get_config().get('test', 'rpa_db_name')))


def get_data_db_engine(env):
    data_db_passwd = parse.quote_plus(get_config().get(env, 'data_db_passwd'))
    data_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (
        get_config().get(env, 'data_db_user'), data_db_passwd,
        get_config().get(env, 'data_db_host'), get_config().get(env, 'data_db_port'),
        get_config().get(env, 'data_db_name')))
    return data_engine


def get_rpa_db_engine(env):
    rpa_db_passwd = parse.quote_plus(get_config().get(env, 'rpa_db_passwd'))
    rpa_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (
        get_config().get(env, 'rpa_db_user'), rpa_db_passwd,
        get_config().get(env, 'rpa_db_host'), get_config().get(env, 'rpa_db_port'),
        get_config().get(env, 'rpa_db_name')))
    return rpa_engine


def get_data_db_session(env):
    Data_DBSession = sessionmaker(bind=get_data_db_engine(env))
    db_session = Data_DBSession()
    return db_session


def get_rpa_db_session(env):
    Rpa_DBSession = sessionmaker(bind=get_rpa_db_engine(env))
    rpa_session = Rpa_DBSession()
    return rpa_session


if __name__ == '__main__':
    s = get_rpa_db_session('ali_master')
    from db_to_rest_compare_tools.orms.dm_user import DmUser
    d = s.query(DmUser.id).all()
    print(d)

    pass
