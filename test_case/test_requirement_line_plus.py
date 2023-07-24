#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
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
from rpa.rpa_orc_coe import RpaOrcCoe
from rpa.rpa_orc_serv import RpaOrcServ
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema

@pytest.mark.make_data_for_rpa_platform
@allure.feature('创建待提交需求')
class TestCreateSavedRequirement:
    def setup_class(self):
        if 'yw_headers' not in os.environ.keys():
            self.yw_info = CommonTool().get_token("yewu")
            self.yw_token = self.yw_info['token']
            self.process_owner = self.yw_info['username']
            self.yw_headers = {"Authorization": "Bearer " + self.yw_token}

            os.environ['yw_token'] = self.yw_token
            os.environ['yw_user'] = self.process_owner
            os.environ['yw_headers'] = json.dumps(self.yw_headers)
        else:
            self.yw_token = os.environ['yw_token']
            self.process_owner = os.environ['yw_user']
            self.yw_headers = os.environ['yw_headers']

        if 'admin_headers' not in os.environ.keys():
            # 登录管理员账号，获取管理员账号的token
            self.admin_info = CommonTool().get_token("admin")
            self.admin_token = self.admin_info['token']
            self.admin_user = self.admin_info['username']
            self.admin_headers = {"Authorization": "Bearer " + self.admin_token}
            #

            os.environ['admin_token'] = self.admin_token
            os.environ['admin_user'] = self.admin_user
            os.environ['admin_headers'] = json.dumps(self.admin_headers)
        else:
            self.admin_token = os.environ['admin_token']
            self.admin_user = os.environ['admin_user']
            self.admin_headers = os.environ['admin_headers']

        if 'kf_headers' not in os.environ.keys():
            # 登录开发账号，获取开发账号的token
            self.kf_info = CommonTool().get_token("kaifa")
            self.kf_token = self.kf_info['token']
            self.kf_user = self.kf_info['username']
            self.kf_headers = {"Authorization": "Bearer " + self.kf_token}

            os.environ['kf_token'] = self.kf_token
            os.environ['kf_user'] = self.kf_user
            os.environ['kf_headers'] = json.dumps(self.kf_headers)
        else:
            self.kf_token = os.environ['kf_token']
            self.kf_user = os.environ['kf_user']
            self.kf_headers = os.environ['kf_headers']

        env = os.environ['env']
        self.org_id = ""
        self.org_name = ""
        self.tag_id = ""
        self.tag_name = ""
        #获取随机的organization_info
        self.org_info = get_random_organization_info(env)
        self.org_id = self.org_info['id']
        self.org_name = self.org_info['name']


        #获取随机的tag_info
        self.tag_info = get_random_process_tag_info(env)
        self.tag_id = self.tag_info['id']
        self.tag_name = self.tag_info['tag_name']

        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


    @allure.title("创建待提交需求")
    def test_create_saved_requirement(self,set_base_url, get_env):
        print("\n")
        print("================================场景一：创建待提交需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)

    @allure.title("删除待提交需求")
    def test_delete_saved_requirement(self,set_base_url, get_env):
        print("\n")
        print("================================场景二：删除待提交需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().delete_requirement(set_base_url,requirement_id, self.yw_headers)

    @allure.title('创建"待管理员评估"需求')
    def test_submit_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景三：创建'待管理员评估'需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)

    @allure.title('驳回"待管理员评估"需求')
    def test_reject_saved_requirement(self,set_base_url, get_env):
        print("\n")
        print("================================场景四：驳回'待管理员评估'需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().reject_requirement(set_base_url,requirement_id, self.admin_headers, self.admin_user )

    @allure.title('创建"待管理员审批"需求')
    def test_estimate_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景五：创建'待管理员审批'需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)

    @allure.title('驳回"待管理员审批"需求')
    def test_reject_estimate_requirement(self,set_base_url, get_env):
        print("\n")
        print("================================场景六：驳回'待管理员审批'需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().reject_requirement(set_base_url,requirement_id, self.admin_headers, self.admin_user )

    @allure.title('创建"待开发"需求')
    def test_verify_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景七：创建'待开发'需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)

    @allure.title('终止"待开发"需求')
    def test_abort_to_be_developed_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景八：终止一个待开发的需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().abort_requirement(set_base_url, requirement_id, self.admin_headers)

    @allure.title('"对待开发"的需求操作需求变更,状态："待确认变更"')
    def test_change_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景九：'待开发'需求操作需求变更,状态：'待确认变更'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)

    @allure.title('"待开发-待确认变更"需求操作"确认需求变更"')
    def test_confirm_change_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十：'待开发-待确认变更'需求操作'确认需求变更'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().confirm_change_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)

    @allure.title('"待开发-待确认变更"需求操作"驳回需求变更",状态："待开发"')
    def test_reject_change_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十一：'待开发-待确认变更'需求操作'驳回需求变更',状态：'待开发'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().abort_change_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)

    @allure.title('终止"待开发-待确认变更"需求')
    def test_abort_change_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十二：终止'待开发-待确认变更'需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().abort_requirement(set_base_url, requirement_id, self.admin_headers)


    @allure.title('创建"待发布"需求')
    def test_to_be_released_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十三：创建一个待发布的需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)

    @allure.title('终止"待发布"需求')
    def test_abort_to_be_released_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十四：终止一个待发布的需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().abort_requirement(set_base_url, requirement_id, self.admin_headers)

    @allure.title('业务员对"待发布"需求操作"需求变更",状态："待确认变更"')
    def test_change_to_be_released_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十五：业务员对'待发布'需求操作'需求变更',状态：'待确认变更'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)

    @allure.title('业务员对"待发布-需求变更"需求操作"确认需求变更",状态："待提交"')
    def test_confirm_change_to_be_released_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十六：业务员对'待发布-需求变更'需求操作'确认需求变更',状态：'待提交'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().confirm_change_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)

    @allure.title('业务员对"待发布-需求变更"需求操作"驳回需求变更",状态："待发布"')
    def test_reject_change_to_be_released_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十七：业务员对'待发布-需求变更'需求操作'驳回需求变更',状态：'待发布'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().abort_change_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)

    @allure.title('创建"待验收"需求')
    def test_to_be_accept_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十八：创建一个待验收状态的需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)

    @allure.title('创建"待上线"需求')
    def test_to_be_onine_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景十九：操作验收通过，创建一个'待上线'状态的需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url,requirement_id,self.yw_headers)

    @allure.title('验收失败，需求状态变为"待发布"')
    def test_fail_to_accept_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十：操作验收失败，需求状态变为'待发布'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_fail_to_acceptance(set_base_url, requirement_id, self.yw_headers, self.process_owner)

    @allure.title('待验收-需求变更，需求状态变为"待确认变更"')
    def test_change_to_be_accept_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十一：待验收-需求变更，需求状态变为'待发布'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)

    @allure.title('待验收-需求变更-确认变更，需求状态变为"待提交"')
    def test_confirm_change_to_be_accept_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十二：待验收-需求变更-确认变更，需求状态变为'待提交'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().confirm_change_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)

    @allure.title('待验收-需求变更-驳回变更，需求状态变为"待验收"')
    def test_reject_change_to_be_accept_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十三：待验收-需求变更-驳回变更，需求状态变为'待验收'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().abort_change_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)

    @allure.title('待验收-需求变更-终止')
    def test_abort_change_to_be_accept_requirement(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十四：待验收-需求变更-终止'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().change_requirement(set_base_url, requirement_id, self.yw_headers, self.process_owner)
        RpaOrcCoe().abort_requirement(set_base_url, requirement_id, self.admin_headers)

    @allure.title('需求流程审核通过，创建一个"已上线"状态的需求')
    def test_pass_requirement_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十五：需求流程审核通过，创建一个'已上线'状态的需求========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)

    @allure.title('需求流程审核失败，需求状态变为"待发布"')
    def test_fail_to_pass_requirement_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十六：需求流程审核失败，需求状态变为'待发布'========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().fail_to_pass_process(set_base_url, process_name, self.admin_headers, get_env)

    @allure.title('启用需求流程')
    def test_enable_requirement_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十七：启用需求流程========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)

    @allure.title('禁用需求流程')
    def test_disable_requirement_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十八：禁用需求流程========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_disable(set_base_url, process_name, self.admin_headers, get_env)

    @allure.title('发布需求来源的流程至应用市场')
    def test_release_requirement_process_to_app_market(self, set_base_url, get_env):
        print("\n")
        print("================================场景二十九：发布需求来源的流程至应用市场========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().release_to_app_market(set_base_url,process_name,self.admin_headers, self.admin_user, get_env, self.org_id, self.tag_id)

    @allure.title('选择一个空闲状态的机器人，运行需求流程')
    def test_run_requirement_process_with_free_robot(self, set_base_url, get_env):
        print("\n")
        print("================================场景三十：发布需求来源的流程至应用市场========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().select_robot_for_process_and_run(set_base_url, process_name, self.admin_headers,  get_env, "free")

    @allure.title('选择一个非空闲状态的机器人，运行需求流程')
    def test_run_requirement_process_with_busy_robot(self, set_base_url, get_env):
        print("\n")
        print("================================场景三十一：选择一个非空闲状态的机器人，运行需求流程========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().select_robot_for_process_and_run(set_base_url, process_name, self.admin_headers,  get_env, "not free")

    @allure.title('手动取消一个待运行的需求流程任务')
    def test_cancle_an_unfinished_task(self, set_base_url, get_env):
        print("\n")
        print("================================场景三十一：手动取消一个待运行的需求流程任务========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        execution_id = RpaOrcServ().select_robot_for_process_and_run(set_base_url, process_name, self.admin_headers,  get_env, "not free")
        RpaOrcServ().cancle_task_before_run(set_base_url, execution_id, self.admin_headers)

    @allure.title('将历史任务对应的流程禁用后，重新运行该流程任务，生成一个"异常->流程运行异常"的任务')
    def test_retry_a_finished_task_which_process_is_be_disabled(self, set_base_url, get_env):
        print("\n")
        print("================================场景三十二：将历史任务对应的流程禁用后，重新运行该流程任务，生成一个'异常->流程运行异常'的任务========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        execution_id = RpaOrcServ().select_robot_for_process_and_run(set_base_url, process_name, self.admin_headers,  get_env, "free")
        RpaOrcServ().process_disable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().redo_history_task(set_base_url,execution_id,self.admin_headers)

    @allure.title('删除一个已完成的需求流程任务')
    def test_delete_a_finished_task(self, set_base_url, get_env):
        print("\n")
        print("================================场景三十三：删除一个已完成的需求流程任务========================================")
        requirement_id = RpaOrcCoe().create_saved_requirement(set_base_url,self.yw_headers, self.process_owner, get_env, self.org_id, self.org_name, self.tag_name)
        RpaOrcCoe().submit_requirement(set_base_url, requirement_id, self.yw_headers)
        RpaOrcCoe().estimate_requirement(set_base_url, requirement_id, self.admin_headers, self.admin_user)
        RpaOrcCoe().verify_data(set_base_url, requirement_id, self.admin_headers, self.admin_user, self.kf_user)
        RpaOrcCoe().confirm_develop_requirement(set_base_url, requirement_id, self.kf_headers, self.kf_user)
        process_name = RpaOrcCoe().develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().submit_develop_requirement(set_base_url,requirement_id,self.kf_headers)
        RpaOrcCoe().release_acceptance(set_base_url, requirement_id, self.yw_headers)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        execution_id = RpaOrcServ().select_robot_for_process_and_run(set_base_url, process_name, self.admin_headers,  get_env, "free")
        RpaOrcServ().delete_task_after_finish_run(set_base_url, execution_id, self.admin_headers)

if __name__ == '__main__':
    pytest.main(["-s","test_requirement_line_plus.py"])
    # jsona = ["aa","bb"]
    # print(jsona)
    # TestCreateSavedRequirement().create_saved_requirement()
    # TestCreateSavedRequirement().test_create_saved_requirement()
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])


