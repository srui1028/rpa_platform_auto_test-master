#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:conftest.py.py
@time:2021/12/30
"""
import os
from datetime import datetime

import pytest
import requests

import bcrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

from _pytest.fixtures import SubRequest
from pytest import fixture
from typing import Any, Callable, Optional

from sqlalchemy.orm import sessionmaker

from utils.config_manager import get_config, get_root_path

ALLURE_ENVIRONMENT_PROPERTIES_FILE = "environment.properties"
ALLUREDIR_OPTION = "--alluredir"
cfg = get_config()


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="huaweicloud_province", help="Test environment: test for default.")
    parser.addoption("--isc", action="store", default="False" , help="if login with isc account")
    parser.addoption("--is_vc", action="store", default="False" , help="if login with isc account")

@pytest.fixture(scope="session", autouse=True)
def get_env(request):
    print(get_root_path())
    env = request.config.getoption("--env")
    os.environ['env'] = env
    return env

@pytest.fixture(scope="session", autouse=True)
def is_isc(request):
    isc = request.config.getoption("--isc")
    os.environ['isc'] = isc
    return isc

@pytest.fixture(scope="session", autouse=True)
def ifRelatingVc(request):
    is_vc = request.config.getoption("--is_vc")
    os.environ['is_vc'] = is_vc
    return is_vc

@fixture(scope="session", autouse=True)
def set_base_url(get_env):
    base_url = cfg.get(get_env, 'base_url')
    print(base_url)
    return base_url


@fixture(scope="session", autouse=True)
def set_user_header(get_env):
    username = get_config().get(get_env, 'username')
    userid = get_config().get(get_env, 'userid')
    header = {'x-user-id': userid, 'x-user-login': username}
    return header


@fixture(scope="session", autouse=True)
def rpa_platform_token(get_env):
    username = get_config().get(get_env, 'username')
    passwd = get_config().get(get_env, 'passwd')
    url = get_config().get(get_env, 'base_url') + get_config().get(get_env, 'login_in_url')
    params = {"password": passwd, "username": username}
    res = requests.request("POST", url,  json=params, stream=True)
    token = "Bearer " + res.json()['data']['id_token']
    return token

# @fixture(scope="session", autouse=True)
# def isc_yw_token(get_env):
#     username = get_config().get(get_env, 'isc_yw_username')
#     passwd = get_config().get(get_env, 'isc_yw_passwd')
#     params = {"password": passwd, "username": username}
#
#     public_key_url = get_config().get(get_env, 'base_url') + get_config().get(get_env, 'rsa_public_key_url')
#     res = requests.request("GET", public_key_url, stream=True)
#
#     public_pem = res.json().get("data").get("key").encode("utf-8")
#     with open("public.pem", "wb") as f:
#         f.write(public_pem)
#
#     # 用公钥加密并用base64转字符
#     username = params.get("username").encode('utf-8')
#     rsakey = RSA.importKey(open("public.pem").read())
#     cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
#     cipher_text = base64.b64encode(cipher.encrypt(username)).decode('utf-8')
#
#     # 获取salt
#     salt_url = get_config().get(get_env, 'base_url') + "/gateway/cs/api/public/v1/user/getSalt"
#     value = cipher_text
#
#     param = {"value": value}
#     res = requests.request("GET", salt_url, params=param, stream=True)
#
#     salt = res.json().get("data").get("salt")
#
#     timeStr = res.json().get("data").get("time")
#     tim = str(int(datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%f+08:00").timestamp() * 1000)).encode("utf-8")
#     cipher_time_text = base64.b64encode(cipher.encrypt(tim)).decode('utf-8')
#
#     # 获取token
#     password = params.get("password").encode("utf-8")
#     hashed = bcrypt.hashpw(password, ("$2a$10$" + salt).encode("utf-8")).decode('utf-8')
#
#     value_for_token = cipher_text + "$s~" + hashed + ".$2" + cipher_time_text
#
#     token_url = get_config().get(get_env, 'base_url') + "/gateway/cs/api/public/v3/authenticate"
#     token_param = {
#         "authMethod": 0,
#         "value": value_for_token
#     }
#
#     res = requests.request("POST", token_url, json=token_param, stream=True)
#     token = res.json().get("data").get("id_token")
#     return token
#
#
# @fixture(scope="session", autouse=True)
# def isc_admin_token(get_env):
#     username = get_config().get(get_env, 'isc_admin_username')
#     passwd = get_config().get(get_env, 'isc_admin_passwd')
#     params = {"password": passwd, "username": username}
#
#     public_key_url = get_config().get(get_env, 'base_url') + get_config().get(get_env, 'rsa_public_key_url')
#     res = requests.request("GET", public_key_url, stream=True)
#
#     public_pem = res.json().get("data").get("key").encode("utf-8")
#     with open("public.pem", "wb") as f:
#         f.write(public_pem)
#
#     # 用公钥加密并用base64转字符
#     username = params.get("username").encode('utf-8')
#     rsakey = RSA.importKey(open("public.pem").read())
#     cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
#     cipher_text = base64.b64encode(cipher.encrypt(username)).decode('utf-8')
#
#     # 获取salt
#     salt_url = get_config().get(get_env, 'base_url') + "/gateway/cs/api/public/v1/user/getSalt"
#     value = cipher_text
#
#     param = {"value": value}
#     res = requests.request("GET", salt_url, params=param, stream=True)
#
#     salt = res.json().get("data").get("salt")
#
#     timeStr = res.json().get("data").get("time")
#     tim = str(int(datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%f+08:00").timestamp() * 1000)).encode("utf-8")
#     cipher_time_text = base64.b64encode(cipher.encrypt(tim)).decode('utf-8')
#
#     # 获取token
#     password = params.get("password").encode("utf-8")
#     hashed = bcrypt.hashpw(password, ("$2a$10$" + salt).encode("utf-8")).decode('utf-8')
#
#     value_for_token = cipher_text + "$s~" + hashed + ".$2" + cipher_time_text
#
#     token_url = get_config().get(get_env, 'base_url') + "/gateway/cs/api/public/v3/authenticate"
#     token_param = {
#         "authMethod": 0,
#         "value": value_for_token
#     }
#
#     res = requests.request("POST", token_url, json=token_param, stream=True)
#     token = res.json().get("data").get("id_token")
#     return token
#
# @fixture(scope="session", autouse=True)
# def isc_kf_token(get_env):
#     username = get_config().get(get_env, 'isc_kf_username')
#     passwd = get_config().get(get_env, 'isc_kf_passwd')
#     params = {"password": passwd, "username": username}
#
#     public_key_url = get_config().get(get_env, 'base_url') + get_config().get(get_env, 'rsa_public_key_url')
#     res = requests.request("GET", public_key_url, stream=True)
#
#     public_pem = res.json().get("data").get("key").encode("utf-8")
#     with open("public.pem", "wb") as f:
#         f.write(public_pem)
#
#     # 用公钥加密并用base64转字符
#     username = params.get("username").encode('utf-8')
#     rsakey = RSA.importKey(open("public.pem").read())
#     cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
#     cipher_text = base64.b64encode(cipher.encrypt(username)).decode('utf-8')
#
#     # 获取salt
#     salt_url = get_config().get(get_env, 'base_url') + "/gateway/cs/api/public/v1/user/getSalt"
#     value = cipher_text
#
#     param = {"value": value}
#     res = requests.request("GET", salt_url, params=param, stream=True)
#
#     salt = res.json().get("data").get("salt")
#
#     timeStr = res.json().get("data").get("time")
#     tim = str(int(datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%f+08:00").timestamp() * 1000)).encode("utf-8")
#     cipher_time_text = base64.b64encode(cipher.encrypt(tim)).decode('utf-8')
#
#     # 获取token
#     password = params.get("password").encode("utf-8")
#     hashed = bcrypt.hashpw(password, ("$2a$10$" + salt).encode("utf-8")).decode('utf-8')
#
#     value_for_token = cipher_text + "$s~" + hashed + ".$2" + cipher_time_text
#
#     token_url = get_config().get(get_env, 'base_url') + "/gateway/cs/api/public/v3/authenticate"
#     token_param = {
#         "authMethod": 0,
#         "value": value_for_token
#     }
#
#     res = requests.request("POST", token_url, json=token_param, stream=True)
#     token = res.json().get("data").get("id_token")
#     return token



@fixture(scope="session", autouse=True)
def get_status_type(get_env):
    status_type = {
        '需求收集': [2,3],
        '流程开发': [4,5,6],
        '运行上线': [7,8]
    }
    return status_type


@fixture(scope="session", autouse=True)
def get_status_name(get_env):
    status_name = {
        '2': "待评估",
        '3': "待审核",
        '4': "待开发",
        '5': "待发布",
        '6': "待验收",
        '7': "待上线",
        '8': "已上线",
    }
    return status_name





@fixture(scope="session", autouse=True)
def set_db_engine(get_env):
    from sqlalchemy import create_engine
    if "_" in get_env:
        env = get_env.split("_")[0]
    else:
        env = get_env
    from urllib import parse
    master_data_db_passwd = parse.quote_plus(get_config().get(env + "_master", 'data_db_passwd'))
    province_data_db_passwd = parse.quote_plus(get_config().get(env + "_province", 'data_db_passwd'))

    master_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (
        get_config().get(env + "_master", 'data_db_user'), master_data_db_passwd,
        get_config().get(env + "_master", 'data_db_host'),
        get_config().get(env + "_master", 'data_db_port'), get_config().get(env + "_master", 'data_db_name')))
    master_db_session = sessionmaker(bind=master_engine)
    master_session = master_db_session()
    province_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (
        get_config().get(env + "_province", 'data_db_user'), province_data_db_passwd,
        get_config().get(env + "_province", 'data_db_host'),
        get_config().get(env + "_province", 'data_db_port'), get_config().get(env + "_province", 'data_db_name')))
    province_db_session = sessionmaker(bind=province_engine)
    province_session = province_db_session()
    return master_engine, master_session, province_engine, province_session


@fixture(scope="session", autouse=True)
def add_allure_environment_property(request: SubRequest) -> Optional[Callable]:
    environment_properties = dict()

    def maker(key: str, value: Any):
        environment_properties.update({key: value})

    yield maker
    alluredir = request.config.getoption(ALLUREDIR_OPTION)
    if not alluredir or not os.path.isdir(alluredir) or not environment_properties:
        return
    allure_env_path = os.path.join(alluredir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)
    with open(allure_env_path, 'w') as _f:
        data = '\n'.join([f'{variable}={value}' for variable, value in environment_properties.items()])
        _f.write(data)


@fixture(autouse=True)
def cenpprop(add_allure_environment_property: Callable, get_env, request) -> None:
    add_allure_environment_property("mark", request.config.getoption("-m"))
    add_allure_environment_property("env", get_env)


def pytest_sessionstart(session):
    session.results = dict()
    mark = session.config.getoption("-m")
    os.environ['mark'] = mark

# @fixture(scope="session", autouse=True)
# def login(get_env):
#     username = get_config().get(get_env, 'username')
#     passwd = get_config().get(get_env, 'passwd')
#     url = get_config().get(get_env, 'base_url') + get_config().get(get_env, 'login_in_url')
#     params = {"password": passwd, "username": username}
#     res = requests.request("POST", url,  json=params, stream=True)
#     token = "Bearer " + res.json()['data']['id_token']
#     return token

if __name__ == '__main__':
    pass
