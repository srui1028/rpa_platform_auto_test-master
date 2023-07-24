#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.common_tools import CommonTool
from utils.search_from_db import *

def get_robot_process_id(env, title):
    '''
    获取robot_process表的id,即流程版本id
    :param env:
    :param title:
    :return:
    '''
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT id from rpa_orc_serv.robot_process where title ='" + title + "' and deleted = 0"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return statistics_list.iat[0,0]

def get_process_name(env, title):
    '''
    获取流程name,即上传时的流程的文件名
    :param env:
    :param title:
    :return:
    '''
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT name from rpa_orc_serv.robot_process where title ='" + title + "' and deleted = 0"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return statistics_list.iat[0,0]

def get_process_resource_sn(env, title):
    '''
    获取流程resource_sn
    :param env:
    :param title:
    :return:
    '''
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT resource_sn from rpa_orc_serv.robot_process where title ='" + title + "' and deleted = 0"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return statistics_list.iat[0,0]

def get_process_file_path(env, title):
    '''
    获取流程在服务器上的存储路径
    :param env:
    :param title:
    :return:
    '''
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = f'''
        SELECT a.file_path from  rpa_orc_serv.robot_process p
    left join  rpa_orc_serv.attachment a
    on p.attachment_id = a.id
    WHERE p.name = "{title}"
    '''
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return statistics_list.iat[0,0]

