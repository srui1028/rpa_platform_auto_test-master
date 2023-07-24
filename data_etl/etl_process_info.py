#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.common_tools import CommonTool
from utils.search_from_db import *

def get_process_info_id(env, title):
    '''
    获取process_info表中存储的流程id
    :param env:
    :param title:
    :return:
    '''
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT id from rpa_orc_serv.process_info where title ='" + title + "'"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return statistics_list.iat[0,0]
