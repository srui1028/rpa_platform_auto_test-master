import ast
import os
import time
from uuid import uuid4

import requests

from api_path import *
from data_etl import etl_process
from data_etl.etl_ccl_tag import get_random_process_tag_info
from data_etl.etl_organization import get_random_organization_info
from data_etl.etl_requirement import get_requirement_id
from project_path import TEST_DATA_PATH
from rpa.rpa_orc_serv import RpaOrcServ
from utils.common_tools import CommonTool


class RpaOrcCoe:
    def create_saved_requirement(self, set_base_url,yw_headers, process_owner, env, org_id, org_name, tag_name):
        path = TEST_DATA_PATH + r"/create_saved_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']

        if org_id == "":
            org_id = "1"
            org_name = "公共组织"

        #获取随机的use_system(涉及系统）
        # use_system = get_random_use_system(self.env)
        #创建一个待提交状态的需求
        data['name'] = CommonTool().get_requirement_name()
        data['process_owner'] = process_owner  #获取需求创建者
        data['businessLabel'] = tag_name  #获取标签名
        data['labels'] = []
        data['labels'].append({'labelId': data['businessLabel']})
        # create_data['useSystem'] = use_system #获取涉及系统   #！！！！！！！！1.4环境原来写的库里没存use_system,待确认
        # create_data['organizationId'] = org_id  #获取组织id
        # create_data['organizationName'] = org_name  #获取组织名称
        # create_data['organization'] = org_id + "-" + org_name  #获取组织名称
        data['organization'] = "1-公共组织"  #获取组织名称    #！！！！！！！！之前1.3环境建需求时没有限制用户的组织权限，1.4好像加了，使用的组织必须是
        # create_data['organization'] = "1191662102368256-桂林电网"  #获取组织名称    #！！！！！！！！之前1.3环境建需求时没有限制用户的组织权限，1.4好像加了，使用的组织必须是


        print(detail + "：")
        request_url = set_base_url + url
        res = requests.request(method, request_url, headers=yw_headers, json=data, stream=True)
        assert res.json().get("success") == True

        # 获取process_instance_id
        process_instance_id = res.json().get("result").get("id")
        time.sleep(3)
        # 通过process_instance_id从数据库中获取requirement_id
        requirement_id = get_requirement_id(env, process_instance_id)
        os.environ['requirement_id'] = requirement_id
        print("需求id是: " + requirement_id)
        print("需求名称是: " + data['name'])
        print("res 是: " + res.text)
        return requirement_id

    def delete_requirement(self, set_base_url, requirement_id, yw_headers):
        print("业务员删除待提交需求：")
        time.sleep(3)
        url = set_base_url + DELETE_REQUIREMENT + requirement_id
        res = requests.request("DELETE", url, headers=yw_headers, stream=True)
        print("res 是: " + res.text)
        assert res.status_code == 200

    def reject_requirement(self, set_base_url, requirement_id, admin_headers, admin_user):
        path = TEST_DATA_PATH + r"/reject_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        # 管理员操作
        time.sleep(3)
        # 获取task_id
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, admin_headers)

        data['current_operator'] = admin_user

        time.sleep(3)
        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=admin_headers, json=data, stream=True)
        # print("res 是: " + res.text)
        assert res.status_code == 204

    def submit_requirement(self, set_base_url, requirement_id, yw_headers):
        path = TEST_DATA_PATH + r"/submit_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        time.sleep(3)
        # 获取task_id
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, yw_headers)

        data['current_operator'] = os.environ['yw_user']

        # 提交需求
        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=yw_headers, json=data, stream=True)
        # print("res 是: " + res.text)
        assert res.status_code == 204


    def estimate_requirement(self, set_base_url, requirement_id, admin_headers, admin_user):
        path = TEST_DATA_PATH + r"/estimate_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        # 管理员操作
        # 获取task_id
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, admin_headers)
        # 管理员评估需求
        data['current_operator'] = admin_user
        data['automationRatio'] = data['automationRatio']
        data['developmentDuration'] = data['developmentDuration']
        time.sleep(3)

        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=admin_headers, json=data, stream=True)
        print("res 是: " + res.text)
        assert res.status_code == 204

    def verify_data(self, set_base_url, requirement_id, admin_headers, admin_user, kf_user):
        path = TEST_DATA_PATH + r"/verify_data.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        # 获取该需求在待审核状态的task_id
        time.sleep(3)
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, admin_headers)

        data['current_operator'] = admin_user
        data['developer'] = kf_user
        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=admin_headers, json=data, stream=True)
        assert res.status_code == 204

    def change_requirement(self, set_base_url, requirement_id, yw_headers, yw_user):
        path = TEST_DATA_PATH + r"/change_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        # 获取该需求在待审核状态的task_id
        time.sleep(3)
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, yw_headers)

        data['current_operator'] = yw_user
        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=yw_headers, json=data, stream=True)
        assert res.status_code == 204

    def confirm_change_requirement(self, set_base_url, requirement_id, admin_headers, admin_user):
        '''
        管理员操作变更通过
        :param set_base_url:
        :param requirement_id:
        :param admin_headers:
        :param admin_user:
        :return:
        '''
        path = TEST_DATA_PATH + r"/confirm_change_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        # 获取该需求在待审核状态的task_id
        time.sleep(3)
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, admin_headers)

        data['current_operator'] = admin_user
        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=admin_headers, json=data, stream=True)
        assert res.status_code == 204

    def abort_change_requirement(self, set_base_url, requirement_id, admin_headers, admin_user):
        '''
        管理员操作驳回需求变更
        :param set_base_url:
        :param requirement_id:
        :param admin_headers:
        :param admin_user:
        :return:
        '''
        path = TEST_DATA_PATH + r"/abort_change_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        # 获取该需求在待审核状态的task_id
        time.sleep(3)
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, admin_headers)

        data['current_operator'] = admin_user
        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=admin_headers, json=data, stream=True)
        assert res.status_code == 204

    def abort_requirement(self, set_base_url, requirement_id, admin_headers):
        path = TEST_DATA_PATH + r"/abort_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        url = set_base_url + ABORT_REQUIREMENT + requirement_id
        time.sleep(3)
        res = requests.request("PUT", url, headers=admin_headers, json=data, stream=True)
        assert res.status_code == 200


    def confirm_develop_requirement(self, set_base_url, requirement_id, kf_headers, kf_user):
        path = TEST_DATA_PATH + r"/confirm_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")

        # 获取该需求在待审核状态的task_id
        time.sleep(3)
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, kf_headers)
        print("task_id 是: " + task_id)

        data['current_operator'] = kf_user
        data['developer'] = kf_user

        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=kf_headers, json=data, stream=True)
        assert res.status_code == 204


    def develop_requirement(self, set_base_url, requirement_id, kf_headers):
        path = TEST_DATA_PATH + r"/develope_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")

        mrpax_file_name = CommonTool().get_mrpax_file()

        # 从设计器发布流程到流程列表
        print("从设计器发布流程到流程列表：")
        process_name = mrpax_file_name
        data['projectName'] = process_name
        file_name = process_name + ".mrpax"
        file_path = TEST_DATA_PATH + "mrpax/" + file_name
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

        data['id'] = requirement_id

        url = set_base_url + develop_REQUIREMENT
        res = requests.request("PUT", url, headers=kf_headers, data=data, files=files)
        fo.close()
        print("res 是: " + res.text)

        #避免文件使用重复，mrpax文件使用完毕后，删除使用过的mrpax
        CommonTool().remove_mrpax_file(file_path)
        return process_name


    def submit_develop_requirement(self, set_base_url, requirement_id, kf_headers):
        '''
        提交开发需求，状态变为待验收
        :param set_base_url:
        :param requirement_id:
        :param kf_headers:
        :return:
        '''
        path = TEST_DATA_PATH + r"/submit_develop_requirement.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + " ：")

        time.sleep(3)

        url = set_base_url + RELEASE_REQUIREMENT + requirement_id
        res = requests.request("POST", url, headers=kf_headers, json=data,  stream=True)
        print("res 是: " + res.text)

    def release_acceptance(self, set_base_url, requirement_id, yw_headers):
        '''
        需求验收通过
        :param set_base_url:
        :param requirement_id:
        :param yw_headers:
        :return:
        '''
        path = TEST_DATA_PATH + r"/release_acceptance.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")

        time.sleep(5)
        # 业务人员操作验收通过
        print("业务人员操作验收通过：")
        url = set_base_url + REQUIREMENT_RELEASE_ACCEPTANCE + str(requirement_id)
        res = requests.request("PUT", url, headers=yw_headers, json=data, stream=True)
        print("res 是: " + res.text)

    def release_fail_to_acceptance(self, set_base_url, requirement_id, yw_headers, yw_user):
        '''
        需求验收失败
        :param set_base_url:
        :param requirement_id:
        :param yw_headers:
        :param yw_user:
        :return:
        '''
        path = TEST_DATA_PATH + r"/release_fail_to_acceptance.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")

        # 获取该需求的task_id
        time.sleep(3)
        task_id = RpaOrcServ().get_requirement_task_id(set_base_url, requirement_id, yw_headers)
        print("task_id 是: " + task_id)

        data['current_operator'] = yw_user

        url = set_base_url + SUBMIT_REQUIREMENT + task_id
        res = requests.request("POST", url, headers=yw_headers, json=data, stream=True)
        assert res.status_code == 204

