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
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema


class TestRequirementLine:
    path = TEST_DATA_PATH + r"/create_requirement.yml"
    info = CommonTool().get_yaml_data_info(path)
    method = info['method']
    url = info['url']
    # headers = info['headers']
    param = CommonTool().get_yaml_data_for_req(path)['data']

    def setup_class(self):
        # logout_url = "http://172.19.192.44:30000/gateway/cs/api/private/v1/logout"
        self.env = os.environ['env']

        # admin, yewu, yewu_leader, pm, expert, tech_leader, kaifa_leader, kaifa
        # 登录业务账号，获取业务账号的token
        self.yw_info = CommonTool().get_token("yewu")
        self.yw_token = self.yw_info['token']
        self.process_owner = self.yw_info['username']
        self.yw_headers = {"Authorization": "Bearer " + self.yw_token}

        # 登录业务leader账号，获取业务leader账号的token
        self.yewu_leader_info = CommonTool().get_token("yewu_leader")
        self.yewu_leader_token = self.yewu_leader_info['token']
        self.yewu_leader_user = self.yewu_leader_info['username']
        self.yewu_leader_headers = {"Authorization": "Bearer " + self.yewu_leader_token}

        # 登录管理员账号，获取管理员账号的token
        self.admin_info = CommonTool().get_token("admin")
        self.admin_token = self.admin_info['token']
        self.admin_user = self.admin_info['username']
        self.admin_headers = {"Authorization": "Bearer " + self.admin_token}

        # 登录pm账号，获取pm账号的token
        self.pm_info = CommonTool().get_token("pm")
        self.pm_token = self.pm_info['token']
        self.pm_user = self.pm_info['username']
        self.pm_headers = {"Authorization": "Bearer " + self.pm_token}

        # 登录tech_leach账号，获取tech_leach账号的token
        self.tech_leader_info = CommonTool().get_token("tech_leader")
        self.tech_leader_token = self.tech_leader_info['token']
        self.tech_leader_user = self.tech_leader_info['username']
        self.tech_leader_headers = {"Authorization": "Bearer " + self.tech_leader_token}

        # 登录tech_ceo账号，获取tech_ceo账号的token
        self.tech_ceo_info = CommonTool().get_token("tech_ceo")
        self.tech_ceo_token = self.tech_leader_info['token']
        self.tech_ceo_user = self.tech_leader_info['username']
        self.tech_ceo_headers = {"Authorization": "Bearer " + self.tech_ceo_token}

        # 登录开发账号，获取开发账号的token
        self.kf_info = CommonTool().get_token("kaifa")
        self.kf_token = self.kf_info['token']
        self.kf_user = self.kf_info['username']
        self.kf_headers = {"Authorization": "Bearer " + self.kf_token}

        # 登录开发leader账号，获取开发账号的token
        self.kf_leader_info = CommonTool().get_token("kaifa_leader")
        self.kf_leader_token = self.kf_leader_info['token']
        self.kf_leader_user = self.kf_leader_info['username']
        self.kf_leader_headers = {"Authorization": "Bearer " + self.kf_leader_token}

        # 登录expert账号，获取expert账号的token
        self.expert_info = CommonTool().get_token("tech_leader")
        self.expert_token = self.expert_info['token']
        self.expert_user = self.expert_info['username']
        self.expert_headers = {"Authorization": "Bearer " + self.expert_token}



    @allure.feature('创建需求-流程-任务数据')
    @pytest.mark.requirement
    @pytest.mark.all
    @pytest.mark.parametrize('create_data, submit_data, yw_verify, pm_verify, expert_estimate, tech_estimate, dev_admin_estimate, confirm_develop_data, process_for_requriement_release, release_acceptance, process_estimate,process_enable, release_to_app_store, select_robots_for_run_process, run_process, detail, resp', param)
    @allure.title("{detail}")
    def test_requirement(self, set_base_url, create_data, submit_data, yw_verify, pm_verify, expert_estimate, tech_estimate, dev_admin_estimate,  confirm_develop_data,
                         process_for_requriement_release, release_acceptance, process_estimate, process_enable, release_to_app_store,
                         select_robots_for_run_process, run_process,detail, resp, get_env):
        # logout_url = "http://172.19.192.44:30000/gateway/cs/api/private/v1/logout"
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        #获取随机的tag_info
        tag_info = get_random_process_tag_info(get_env)
        tag_id = tag_info['id']
        tag_name = tag_info['tag_name']

        #获取随机的organization_info
        # org_id = '1158609790175745'
        org_info = get_random_organization_info(self.env)
        org_id = org_info['id']
        org_name = org_info['name']

        #获取随机的use_system(涉及系统）
        # use_system = get_random_use_system(self.env)  #！！！！！！！！1.4环境原来写的库里没存use_system,待确认
        print("\n")
        print("================================"+ detail +"========================================")
        #创建一个待提交状态的需求
        create_data['name'] = CommonTool().get_requirement_name()
        create_data['process_owner'] = self.process_owner  #获取需求创建者
        create_data['businessLabel'] = tag_name  #获取标签名
        create_data['labels'] = []
        create_data['labels'].append({'labelId': create_data['businessLabel']})
        # create_data['useSystem'] = use_system #获取涉及系统   #！！！！！！！！1.4环境原来写的库里没存use_system,待确认
        # create_data['organizationId'] = org_id  #获取组织id
        # create_data['organizationName'] = org_name  #获取组织名称
        # create_data['organization'] = org_id + "-" + org_name  #获取组织名称
        create_data['organization'] = "1191662310166528-阳朔电网"  #获取组织名称    #！！！！！！！！之前1.3环境建需求时没有限制用户的组织权限，1.4好像加了，使用的组织必须是
        # create_data['organization'] = "1191662102368256-桂林电网"  #获取组织名称    #！！！！！！！！之前1.3环境建需求时没有限制用户的组织权限，1.4好像加了，使用的组织必须是


        print("业务人员创建一个待提交的需求：")
        request_url = set_base_url + self.url
        res = requests.request(self.method, request_url, headers=self.yw_headers, json=create_data, stream=True)
        assert res.json().get("success") == True

        # 获取process_instance_id
        process_instance_id = res.json().get("result").get("id")
        time.sleep(3)
        # 通过process_instance_id从数据库中获取requirement_id
        requirement_id = get_requirement_id(self.env, process_instance_id)
        print("requirement_id 是: " + requirement_id)
        print("res 是: " + res.text)

        if len(submit_data) == 0:
            return
        print("业务人员提交需求：")
        # 获取task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.yw_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)

        submit_data['current_operator'] = self.process_owner

        # params_for_submit = {
        #     "current_operator": process_owner,
        #     "status": 2
        # }

        # 提交需求
        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.yw_headers, json=submit_data, stream=True)
        assert res.status_code == 204
        if len(yw_verify) == 0:
            return

        # 业务leaader审批需求
        print("业务leader审批需求：")
        time.sleep(3)
        # 获取task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.yw_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)

        yw_verify['current_operator'] = self.yewu_leader_user
        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.yw_headers, json=yw_verify, stream=True)
        assert res.status_code == 204
        if len(pm_verify) == 0:
            return

        # pm审批需求
        print("pm审批需求：")
        time.sleep(3)
        # 获取task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.pm_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)

        pm_verify['current_operator'] = self.pm_user
        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.pm_headers, json=pm_verify, stream=True)
        assert res.status_code == 204
        if len(expert_estimate) == 0:
            return

        print("专家评估需求：")
        #专家评估需求
        time.sleep(3)
        # 获取task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.expert_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)

        expert_estimate['current_operator'] = self.expert_user
        time.sleep(3)

        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.expert_headers, json=expert_estimate, stream=True)
        assert res.status_code == 204
        if len(tech_estimate) == 0:
            return

        print("技术评估需求：")
        #专家评估需求
        time.sleep(3)
        # 获取task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.tech_leader_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)

        tech_estimate['current_operator'] = self.expert_user
        time.sleep(3)

        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.tech_leader_headers, json=tech_estimate, stream=True)
        assert res.status_code == 204
        # if len(tech_ceo_estimate) == 0:
        #     return

        print("技术总监评估需求：")
        #专家评估需求
        time.sleep(3)
        # 获取task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.tech_leader_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)
        tech_ceo_estimate = {}
        tech_ceo_estimate['current_operator'] = self.expert_user
        tech_ceo_estimate['status'] = 25
        time.sleep(3)

        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.tech_ceo_headers, json=tech_ceo_estimate, stream=True)
        assert res.status_code == 204
        if len(dev_admin_estimate) == 0:
            return

        print("开发领导评估需求：")
        #开发领导评估需求
        time.sleep(3)
        # 获取task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.kf_leader_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)

        dev_admin_estimate['current_operator'] = self.kf_leader_user
        dev_admin_estimate['developer'] = self.kf_user

        time.sleep(3)

        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.kf_leader_headers, json=dev_admin_estimate, stream=True)
        assert res.status_code == 204
        if len(confirm_develop_data) == 0:
            return

        #
        # print("管理员审批需求：")
        # # 获取该需求在待审核状态的task_id
        # url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        # time.sleep(3)
        # res = requests.request("GET", url, headers=self.admin_headers, stream=True)
        # task_id = res.json().get("data").get("taskId")
        # print("task_id 是: " + task_id)
        #
        # # 管理员审核需求并分配开发人员
        # # params_for_verify = {
        # #     "current_operator" : "dwxbxntest3",
        # #     "design" : 1123512485363969,
        # #     "developer" : "dwxbtest006",
        # #     "pass": True,
        # #     "priority": 1,
        # #     "status": 4
        # # }
        # verify_data['current_operator'] = self.admin_user
        # verify_data['developer'] = self.kf_user
        # url = set_base_url + "/be/hyperpm/form/task/" + task_id
        # res = requests.request("POST", url, headers=self.admin_headers, json=verify_data, stream=True)
        # assert res.status_code == 204



        print("开发人员确认开发需求：")
        #开发人员操作
        time.sleep(3)

        # 获取该需求在待开发状态的task_id
        url = set_base_url + "/be/api/v1/requirement/" + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=self.kf_headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("获取该需求在待开发状态的task_id：")
        print("task_id 是: " + task_id)

        # 开发人员确认开发需求
        # params_for_confirm_develop = {
        #     "current_operator": "dwxbtest006",
        #     "developer": "dwxbtest006",
        #     "status": 5
        # }
        confirm_develop_data['current_operator'] = self.kf_user
        confirm_develop_data['developer'] = self.kf_user

        url = set_base_url + "/be/hyperpm/form/task/" + task_id
        res = requests.request("POST", url, headers=self.kf_headers, json=confirm_develop_data, stream=True)
        assert res.status_code == 204
        if len(process_for_requriement_release) == 0:
            return

        time.sleep(3)

        mrpax_file_name = CommonTool().get_mrpax_file()

        # 从设计器发布流程到流程列表
        print("从设计器发布流程到流程列表：")
        # process_name = process_for_requriement_release['projectName']
        process_name = mrpax_file_name
        process_for_requriement_release['projectName'] = process_name
        file_name = process_name+".mrpax"
        file_path = TEST_DATA_PATH + "mrpax/"+ file_name
        fo = open(file_path, 'rb')
        files = [
            ('mrpFile', (file_name, fo))
        ]
        print("mrpFile is " + file_path)

        # data = {
        #     "id" : requiremnt_id,
        # #     "projectDesc" : "projectDesc",
        # #     "projectName" :  "C",
        # #     "projectVersion" : "1.0.0",
        # #     "releaseIntroduce" : "releaseIntroduce",
        # #     # "useFile" : "",
        # #     "useIntroduce" : "useIntroduce"
        # # }

        process_for_requriement_release['id'] = requirement_id

        url = set_base_url + "/gateway/ac/api/private/v1/requirement/release"
        res = requests.request("PUT", url, headers=self.kf_headers, data=process_for_requriement_release, files=files)
        fo.close()
        print("res 是: " + res.text)
        if len(release_acceptance) == 0:
            return

        #避免文件使用重复，mrpax文件使用完毕后，删除使用过的mrpax
        CommonTool().remove_mrpax_file(file_path)

        time.sleep(5)
        # 业务人员操作验收通过
        print("业务人员操作验收通过：")
        url = set_base_url + "/be/api/v1/requirement/releaseAcceptance/" + str(requirement_id)
        # url = set_base_url + "/be/api/v1/requirement/releaseAcceptance/1506919216430051329"
        res = requests.request("PUT", url, headers=self.yw_headers, json=release_acceptance, stream=True)
        print("res 是: " + res.text)
        if len(process_estimate) == 0:
            return


        time.sleep(4)
        # 管理员操作流程-审核通过
        print("管理员操作流程-审核通过:")
        robot_process_id = str(etl_process.get_robot_process_id(self.env, process_name))
        url = set_base_url + "/gateway/orc-serv/api/private/v1/process/approve/" + robot_process_id
        res = requests.request("POST", url, headers=self.admin_headers, params=process_estimate)
        print("res 是: " + res.text)
        if len(process_enable) == 0:
            return


        time.sleep(3)

        if process_enable['currentVersionStatus'] == 1:
            #管理员启用流程
            print("管理员启用流程:")
            name_of_process_in_db = str(etl_process.get_process_name(self.env, process_name))
            process_enable['name'] = name_of_process_in_db
            url = set_base_url + "/gateway/orc-serv/api/private/v1/process/version/approval"
            res = requests.request("POST", url, headers=self.admin_headers, json=process_enable)
            print("res 是: " + res.text)
        elif process_enable['currentVersionStatus'] == 0:
            #管理员启用流程
            print("管理员启用流程:")
            process_enable['currentVersionStatus'] = 1
            name_of_process_in_db = str(etl_process.get_process_name(self.env, process_name))
            process_enable['name'] = name_of_process_in_db
            url = set_base_url + "/gateway/orc-serv/api/private/v1/process/version/approval"
            res = requests.request("POST", url, headers=self.admin_headers, json=process_enable)
            print("res 是: " + res.text)
            time.sleep(3)
            #管理员禁用流程：
            print("管理员禁用流程:")
            process_enable['currentVersionStatus'] = 0
            res = requests.request("POST", url, headers=self.admin_headers, json=process_enable)
            print(res.text)
        if len(release_to_app_store) == 0:
            return

        org_id_list = []
        org_id_list.append(org_id)

        tag_id_list = []
        # tag_id = get_random_process_tag_id(env)
        tag_id_list.append((tag_id))

        time.sleep(3)
        #管理员发布流程到应用市场：
        release_to_app_store['authorId'] = get_user_id(self.env,self.admin_user)
        release_to_app_store['authorName'] = self.admin_user
        release_to_app_store['fileUrl'] = get_process_file_path(self.env,name_of_process_in_db)  #流程在服务器的存储地址
        release_to_app_store['id'] = robot_process_id
        release_to_app_store['pluginId'] = str(get_process_info_id(self.env, process_name))  # plugin_id即流程id,即process_info表中的id
        release_to_app_store['pluginName'] = process_name
        release_to_app_store['resourceSn'] = get_process_resource_sn(self.env, process_name)
        release_to_app_store['organizationIds'] = org_id_list  # 随机生成组织id
        release_to_app_store['tagIds'] = tag_id_list             #!!!!!!待改

        url =  set_base_url + "/gateway/ac/api/private/v1/plugin/version/cs"
        res = requests.request("POST", url, headers=self.admin_headers, json=release_to_app_store,  stream=True)
        print("发布到流程市场:")
        print("res 是: " + res.text)
        if len(run_process) == 0:
            return

        time.sleep(3)

        robot_org_id = ""
        #为执行流程选择机器人：
        if select_robots_for_run_process['robotName'] == "free":
            robot_org_id = get_random_free_robot_id(self.env)
            robot_org_id = get_robot_organization_id(self.env, robot_org_id)  # 获取robotNme对应org_id
            select_robots_for_run_process['robotIds'] = get_robot_id_list_by_robot_id(robot_org_id)  # 通过随机生成的机器人id获取空闲机器人id列表
        elif select_robots_for_run_process['robotName'] == "not free":
            robot_org_id = get_random_not_free_robot_id(self.env)
            robot_org_id = get_robot_organization_id(self.env, robot_org_id)  # 获取robotNme对应org_id
            select_robots_for_run_process['robotIds'] = get_robot_id_list_by_robot_id(robot_org_id)  # 通过随机生成的机器人id获取非机器人id列表
        else:
            robot_org_id = get_robot_organization_id(self.env, get_robot_id(self.env, select_robots_for_run_process['robotName']))  # 获取robotNme对应org_id
            select_robots_for_run_process['robotIds'] = get_robot_id_list(self.env, select_robots_for_run_process['robotName'])  # 通过用例参数中指定的机器人名获取机器人id列表

        url = set_base_url + "/gateway/orc-serv/api/private/v1/jobs/select-robots"
        del select_robots_for_run_process['robotName']
        select_robots_for_run_process['labelName'] = CommonTool().get_robot_temp_label_name() #获取随机的uuid4labelname
        res = requests.request("POST", url, headers=self.admin_headers, json=select_robots_for_run_process,  stream=True)
        print("为执行流程选择机器人:")
        print(res.text)

        time.sleep(3)

        #管理员运行流程：
        print("管理员运行流程:")
        url = set_base_url + "/gateway/orc-serv/api/private/v1/processes/" + robot_process_id + "/get-instance"
        # url = set_base_url + "/gateway/orc-serv/api/private/v1/processes/1157549708525824/get-instance"
        run_process['conditions'] = select_robots_for_run_process['labelName']
        run_process['name'] = process_name + "_1.0.0"
        run_process['resourceSn'] = release_to_app_store['resourceSn']
        run_process['organizationId'] = robot_org_id

        res = requests.request("POST", url, headers=self.admin_headers, json=run_process,  stream=True)
        print("res 是: " + res.text)
        if len(run_process) == 0:
            return
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))




if __name__ == '__main__':
    pytest.main(["-s","test_requirements_line.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])


