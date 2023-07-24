#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import random

import pandas as pd
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.common_tools import CommonTool
from utils.search_from_db import *

def get_random_use_system(env):
    """
    获取创建需求时的涉及系统
    :return:
    """
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT options from rpa_coe.requirement_form WHERE id = 3 and title = '涉及系统'"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    result = json.loads(statistics_list.iat[0,0])
    random_num = random.randint(1, len(result)) - 1
    return result[random_num]


if __name__ == '__main__':
    print(get_random_use_system("huaweicloud_province"))
    # get_requirement_task_id( "65d288f5-a345-11ec-8545-fa163eee70bf")