#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import random
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.search_from_db import *

def get_robot_id(env, robot_name):
    """
    获取机器人id
    :return:
    """
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT id from rpa_orc_serv.robot where name = '" + robot_name + "'"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return str(statistics_list.iat[0,0])

def get_robot_name(env, robot_id):
    """
    获取机器人名
    :return:
    """
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT name from rpa_orc_serv.robot where id = '" + robot_id + "'"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return str(statistics_list.iat[0,0])

def get_robot_id_list(env, robot_name_str):
    robot_name_list = str.split(robot_name_str, ",")
    robot_id_list = []
    for i in range(len(robot_name_list)):
        id = get_robot_id(env, robot_name_list[i])
        robot_id_list.append(id)
    return robot_id_list

def get_random_free_robot_id(env):
    '''
    获取随机的robot_id
    :param env:
    :return:
    '''
    session = get_data_db_session(env)
    get_count_sql = '''
    SELECT count(*) from rpa_orc_serv.robot where status = 0 and deleted=0
    '''
    data_engine = get_data_db_engine(env)
    count = pd.read_sql(get_count_sql, data_engine).iat[0,0]
    if count==0:
        return -1
    random_num = str(random.randint(1,count)-1)

    get_robot_id_sql = f'''
    SELECT id from rpa_orc_serv.robot where deleted=0 limit {random_num},1
    '''
    # print(get_org_id_sql)

    statistics_list = pd.read_sql(get_robot_id_sql, data_engine)
    session.close()
    robot_id = str(statistics_list.iat[0,0])
    print("选择的机器人是：" + get_robot_name(env,robot_id))
    return robot_id

def get_random_not_free_robot_id(env):
    '''
    获取随机的robot_id
    :param env:
    :return:
    '''
    session = get_data_db_session(env)
    get_count_sql = '''
    SELECT count(*) from rpa_orc_serv.robot where status <> 0 and deleted=0
    '''
    data_engine = get_data_db_engine(env)
    count = pd.read_sql(get_count_sql, data_engine).iat[0,0]
    if count==0:
        return -1

    random_num = str(random.randint(1,count)-1)

    get_robot_id_sql = f'''
    SELECT id from rpa_orc_serv.robot where deleted=0 limit {random_num},1
    '''
    # print(get_org_id_sql)

    statistics_list = pd.read_sql(get_robot_id_sql, data_engine)
    session.close()
    robot_id = str(statistics_list.iat[0,0])
    print("选择的机器人是：" + get_robot_name(env,robot_id))
    return robot_id

def get_robot_id_list_by_robot_id(robot_id_str):
    robot_id_list = str.split(robot_id_str, ",")
    return robot_id_list

if __name__ == '__main__':
    print(get_random_not_free_robot_id("huaweicloud_province"))
    # get_requirement_task_id( "65d288f5-a345-11ec-8545-fa163eee70bf")