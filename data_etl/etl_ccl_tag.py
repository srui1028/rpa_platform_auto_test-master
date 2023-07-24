#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random

import pandas as pd
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.common_tools import CommonTool
from utils.search_from_db import *

def get_random_process_tag_id(env):
    '''
    获取随机的卓越中心tag_id--适用于需求&&流程
    :param env:
    :return:
    '''
    session = get_data_db_session(env)
    get_count_sql = '''
    SELECT count(*) from rpa_coe.ccl_tag where tag_type=2 and deleted = 0
    '''
    data_engine = get_data_db_engine(env)
    count = pd.read_sql(get_count_sql, data_engine).iat[0,0]
    random_num = str(random.randint(1,count)-1)

    get_tag_id_sql = f'''
    SELECT id from rpa_coe.ccl_tag where tag_type=2 and deleted = 0 limit {random_num},1
    '''
    # print(get_tag_id_sql)
    statistics_list = pd.read_sql(get_tag_id_sql, data_engine)
    session.close()
    return str(statistics_list.iat[0,0])

def get_random_process_tag_info(env):
    '''
    获取随机的卓越中心tag_info(tag_id&&tag_name)--适用于需求&&流程
    :param env:
    :return:
    '''
    session = get_data_db_session(env)
    get_count_sql = '''
    SELECT count(*) from rpa_coe.ccl_tag where tag_type=2 and deleted = 0
    '''
    data_engine = get_data_db_engine(env)
    count = pd.read_sql(get_count_sql, data_engine).iat[0, 0]
    random_num = str(random.randint(1, count) - 1)

    get_tag_info_sql = f'''
    SELECT id,tag_name from rpa_coe.ccl_tag where tag_type=2 and deleted = 0 limit {random_num},1
    '''
    # print(get_tag_info_sql)
    statistics_list = pd.read_sql(get_tag_info_sql, data_engine)
    session.close()
    tag_info={}
    tag_info['id'] = str(statistics_list.iat[0, 0])
    tag_info['tag_name']  = str(statistics_list.iat[0, 1])
    return tag_info


def get_random_component_tag_id(env):
    '''
    获取随机的组件tag_id
    :param env:
    :return:
    '''
    session = get_data_db_session(env)
    get_count_sql = '''
    SELECT count(*) from rpa_coe.ccl_tag where tag_type=1 and deleted = 0
    '''
    data_engine = get_data_db_engine(env)
    count = pd.read_sql(get_count_sql, data_engine).iat[0,0]
    random_num = str(random.randint(0,count)-1)

    get_component_id_sql = f'''
    SELECT id from rpa_coe.ccl_tag where tag_type=1 and deleted = 0 limit {random_num},1
    '''
    # print(get_component_id_sql)
    statistics_list = pd.read_sql(get_component_id_sql, data_engine)
    session.close()
    return str(statistics_list.iat[0,0])

if __name__ == '__main__':
    print(get_random_process_tag_info("huaweicloud_province"))