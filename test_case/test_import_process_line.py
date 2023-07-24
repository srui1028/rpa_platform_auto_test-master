#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

import allure

from data_etl import etl_process
from data_etl.etl_ccl_tag import get_random_process_tag_info
from data_etl.etl_organization import get_random_organization_info
from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema
from rpa.rpa_orc_serv import RpaOrcServ


class TestImportProcess:
    def setup_class(self):
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

    @allure.title("导入本地流程到控制中心-流程列表")
    def test_import_local_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景一：导入本地流程到控制中心-流程列表========================================")
        RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)

    @allure.title("审核通过本地上传的流程")
    def test_pass_local_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景二：审核通过本地上传的流程========================================")
        process_name = RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)

    @allure.title("审核失败本地上传的流程")
    def test_fail_to_pass_local_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景三：审核失败本地上传的流程========================================")
        process_name = RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)
        RpaOrcServ().fail_to_pass_process(set_base_url, process_name, self.admin_headers, get_env)
    @allure.title("启用本地上传的流程")
    def test_enable_local_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景四：启用本地上传的流程========================================")
        process_name = RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
    @allure.title("禁用本地上传的流程")
    def test_disable_local_process(self, set_base_url, get_env):
        print("\n")
        print("================================场景五：禁用本地上传的流程========================================")
        process_name = RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_disable(set_base_url, process_name, self.admin_headers, get_env)

    @allure.title("发布本地上传的流程到应用市场")
    def test_release_local_process_to_app_market(self, set_base_url, get_env):
        print("\n")
        print("================================场景六：发布本地上传的流程到应用市场========================================")
        process_name = RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().release_to_app_market(set_base_url,process_name,self.admin_headers, self.admin_user, get_env, self.org_id, self.tag_id)

    @allure.title("选择一个空闲状态的机器人，运行本地上传的流程")
    def test_run_local_process_with_free_robot(self, set_base_url, get_env):
        print("\n")
        print("================================场景七：选择一个空闲状态的机器人，运行本地上传的流程========================================")
        process_name = RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().release_to_app_market(set_base_url,process_name,self.admin_headers, self.admin_user, get_env, self.org_id, self.tag_id)
        RpaOrcServ().select_robot_for_process_and_run(set_base_url, process_name, self.admin_headers,  get_env, "free")

    @allure.title("选择一个非空闲状态的机器人，运行本地上传的流程")
    def test_run_local_process_with_busy_robot(self, set_base_url, get_env):
        print("\n")
        print("================================场景八：选择一个非空闲状态的机器人，运行本地上传的流程========================================")
        process_name = RpaOrcServ().import_local_process(set_base_url,self.yw_headers, self.process_owner, self.org_id)
        RpaOrcServ().pass_process(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().process_enable(set_base_url, process_name, self.admin_headers, get_env)
        RpaOrcServ().release_to_app_market(set_base_url,process_name,self.admin_headers, self.admin_user, get_env, self.org_id, self.tag_id)
        RpaOrcServ().select_robot_for_process_and_run(set_base_url, process_name, self.admin_headers,  get_env, "not free")

if __name__ == '__main__':
    pytest.main(["-s","test_import_process_line.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])


