#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random

import pandas as pd
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.common_tools import CommonTool
from utils.search_from_db import *

#
# rpa_orc_serv和rpa_cs都有organization库，rpa_orc_serv会自动拉取rpa_cs的组织数据
def get_random_organization_id(env):
    '''
    获取随机的组织id
    :param env:
    :return:
    '''
    session = get_data_db_session(env)
    get_count_sql = '''
    SELECT count(*) from rpa_cs.organization where name <> 'root' and deleted=0
    '''
    data_engine = get_data_db_engine(env)
    count = pd.read_sql(get_count_sql, data_engine).iat[0,0]
    random_num = str(random.randint(1,count)-1)

    get_org_id_sql = f'''
    SELECT id from rpa_cs.organization where name <> 'root' and deleted=0 limit {random_num},1
    '''
    # print(get_org_id_sql)
    statistics_list = pd.read_sql(get_org_id_sql, data_engine)
    session.close()
    return str(statistics_list.iat[0,0])

def get_random_organization_info(env):
    '''
    获取随机的卓越中心organization_info(organization_id&&organization_name)--适用于需求&&流程
    :param env:
    :return:
    '''
    session = get_data_db_session(env)
    get_count_sql = '''
    SELECT count(*) from rpa_cs.organization where name <> 'root' and deleted=0
    '''
    data_engine = get_data_db_engine(env)
    count = pd.read_sql(get_count_sql, data_engine).iat[0, 0]
    random_num = str(random.randint(1, count) - 1)

    get_org_id_info_sql = f'''
    SELECT id,title from rpa_cs.organization where name <> 'root' and deleted=0 limit {random_num},1
    '''
    print("**********************")
    print(get_org_id_info_sql)
    statistics_list = pd.read_sql(get_org_id_info_sql, data_engine)
    session.close()
    tag_info={}
    tag_info['id'] = str(statistics_list.iat[0, 0])
    tag_info['name']  = str(statistics_list.iat[0, 1])
    return tag_info


if __name__ == '__main__':
    print(get_random_organization_info("huaweicloud_province"))