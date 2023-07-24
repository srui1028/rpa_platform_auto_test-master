#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from datetime import datetime
from uuid import uuid4

import bcrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

import allure

from data_etl import etl_process
from data_etl.etl_ccl_tag import get_random_process_tag_id, get_random_process_tag_info
from data_etl.etl_organization import get_random_organization_id, get_random_organization_info
from data_etl.etl_organization_robot import get_robot_organization_id
from data_etl.etl_process import *
from data_etl.etl_process_info import get_process_info_id
from data_etl.etl_requirement import get_requirement_id
from data_etl.etl_requirement_form import get_random_use_system
from data_etl.etl_robot import get_robot_id_list, get_robot_id, get_random_free_robot_id, get_robot_id_list_by_robot_id, \
    get_random_not_free_robot_id
from data_etl.etl_user import get_user_id
from project_path import TEST_DATA_PATH
from utils import rpa_orc_serv
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema
from utils.rpa_orc_serv import RpaOrcServ


class TestImportProcess:
    # path = TEST_DATA_PATH + r"/import_process.yml"
    # info = CommonTool().get_yaml_data_info(path)
    # method = info['method']
    # url = info['url']
    # # headers = info['headers']
    # # param = CommonTool().get_yaml_data_for_req(path)['data']

    def setup_class(self):
        # logout_url = "http://172.19.192.44:30000/gateway/cs/api/private/v1/logout"
        self.env = os.environ['env']
        # 登录业务账号，获取业务账号的token
        self.yw_info = CommonTool().get_token("yewu")
        self.yw_token = self.yw_info['token']
        self.process_owner = self.yw_info['username']
        self.yw_headers = {"Authorization": "Bearer " + self.yw_token}

        # 登录管理员账号，获取管理员账号的token
        self.admin_info = CommonTool().get_token("admin")
        self.admin_token = self.admin_info['token']
        self.admin_user = self.admin_info['username']
        self.admin_headers = {"Authorization": "Bearer " + self.admin_token}

        # 登录开发账号，获取开发账号的token
        self.kf_info = CommonTool().get_token("kaifa")
        self.kf_token = self.kf_info['token']
        self.kf_user = self.kf_info['username']
        self.kf_headers = {"Authorization": "Bearer " + self.kf_token}


    @allure.feature('创建需求-流程-任务数据')
    @pytest.mark.requirement
    @pytest.mark.all
    def test_import_process(self, set_base_url):
        # 获取随机的organization_info
        # org_id = '1158609790175745'
        org_info = get_random_organization_info(self.env)
        org_id = org_info['id']

        mrpax_file_name = CommonTool().get_mrpax_file()

        # 从设计器发布流程到流程列表
        print("从设计器发布流程到流程列表：")
        # process_name = process_for_requriement_release['projectName']
        process_name = mrpax_file_name
        file_name = process_name+".mrpax"
        file_path = TEST_DATA_PATH + "mrpax/"+ file_name
        res = RpaOrcServ().import_local_mrpax(file_path, file_name,process_name, set_base_url, self.admin_user, self.admin_headers, org_id)
        print("res 是: " + str(res))






if __name__ == '__main__':
    pytest.main(["-s","test_import_process.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])


