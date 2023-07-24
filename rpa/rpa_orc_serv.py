import ast
import os
import time
from uuid import uuid4

import requests

from api_path import *
from data_etl import etl_process
from data_etl.etl_organization_robot import get_robot_organization_id
from data_etl.etl_process import get_process_file_path, get_process_resource_sn
from data_etl.etl_process_info import get_process_info_id
from data_etl.etl_robot import get_random_free_robot_id, get_robot_id_list_by_robot_id, get_random_not_free_robot_id, \
    get_robot_id, get_robot_id_list
from data_etl.etl_user import get_user_id
from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool


class RpaOrcServ:
    def import_local_mrpax(self,file_path, file_name,process_name, base_url, user, headers, org_id):
        fo = open(file_path, 'rb')
        files = [
            ('file', (file_name, fo))
        ]
        print("mrpFile is " + file_path)
        process_name_uuid = str(uuid4())
        resourceSn = str(uuid4())
        data = {
            "title": process_name,
            "name" : process_name_uuid,
            "version": "1.0.0",
            "deleted": 0,
            "processType": 1,
            "comments": "This is comments for process " + process_name,
            "resourceSn": resourceSn,
            # "type": "mrpax",
            "createdBy": user,
            "labelList": []
        }
        url = base_url + "/gateway/orc-serv/api/private/v2/process-info"
        process_res = requests.request("POST", url, headers=headers, data=data, files=files).json()
        fo.close()


        organizations = []
        organizationsDict = {}
        organizationsDict['organizationId'] = org_id
        organizationsDict['organizationSn'] = str(uuid4())
        organizations.append(organizationsDict)
        org_data = {
            'organizations' : organizations,
            'processId' : process_res['data']['id'],
            'processName' : process_name_uuid,
            'processSn' : resourceSn
        }

        url = base_url + "/gateway/orc-serv/api/private/v1/organization-processes/organizations"
        res = requests.request("PUT", url, headers=headers, json=org_data).json()

        print("组织关联流程返回: " + str(res))

        # #避免文件使用重复，mrpax文件使用完毕后，删除使用过的mrpax
        CommonTool().remove_mrpax_file(file_path)
        #
        return process_res

    def import_local_process(self, set_base_url, yw_headers, process_owner, org_id):
        mrpax_file_name = CommonTool().get_mrpax_file()

        print("从本地导入流程到流程列表：")
        process_name = mrpax_file_name
        file_name = process_name+".mrpax"
        file_path = TEST_DATA_PATH + "mrpax/"+ file_name
        res = RpaOrcServ().import_local_mrpax(file_path, file_name,process_name, set_base_url, process_owner, yw_headers, org_id)
        print("res 是: " + str(res))
        return process_name

    def estimate_process(self, base_url, robot_process_id, approve, headers):
        '''
        :param base_url:
        :param robot_process_id:
        :param approve: 1审核通过
        :return:
        '''
        url = base_url + "/gateway/orc-serv/api/private/v1/process/approve/" + str(robot_process_id)
        param = {
            "approve": approve
        }
        res = requests.request("POST", url, headers=headers, params=param).json()
        return res

    def get_requirement_task_id(self, base_url, requirement_id, headers):
        # 获取task_id
        url = base_url + GET_REQUIREMENT_TASK_ID + requirement_id
        time.sleep(3)
        res = requests.request("GET", url, headers=headers, stream=True)
        task_id = res.json().get("data").get("taskId")
        print("task_id 是: " + task_id)
        return task_id

    def pass_process(self, set_base_url, process_name, admin_headers, env):
        '''
        流程审核通过
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        data = {}
        data['approve'] = 1
        print("需求流程审核通过：")
        time.sleep(3)
        # 管理员操作流程-审核通过
        print("管理员操作流程-审核通过:")
        robot_process_id = str(etl_process.get_robot_process_id(env, process_name))
        url = set_base_url + ESTIMATE_REQUIREMENT_PROCESS + robot_process_id
        res = requests.request("POST", url, headers=admin_headers, params=data)
        print("res 是: " + res.text)

    def fail_to_pass_process(self, set_base_url, process_name, admin_headers, env):
        '''
        流程审核失败，被驳回
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        data = {}
        data['approve'] = 0
        data['reason'] = "这是审核失败原因"
        print("流程审核通过：")
        time.sleep(3)
        # 管理员操作流程-审核通过
        print("管理员操作流程-审核通过:")
        robot_process_id = str(etl_process.get_robot_process_id(env, process_name))
        url = set_base_url + ESTIMATE_REQUIREMENT_PROCESS + robot_process_id
        res = requests.request("POST", url, headers=admin_headers, params=data)
        print("res 是: " + res.text)

    def process_enable(self, set_base_url, process_name, admin_headers, env):
        '''
        启用流程
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        path = TEST_DATA_PATH + r"/process_enable.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        time.sleep(3)

        # 管理员启用流程
        print("管理员启用流程:")
        name_of_process_in_db = str(etl_process.get_process_name(env, process_name))
        data['name'] = name_of_process_in_db
        url = set_base_url + PROCESS_ENABLE
        res = requests.request("POST", url, headers=admin_headers, json=data)
        print("res 是: " + res.text)

    def process_disable(self, set_base_url, process_name, admin_headers, env):
        '''
        禁用流程
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        path = TEST_DATA_PATH + r"/process_disable.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        time.sleep(3)

        # 管理员启用流程
        print("管理员禁用流程:")
        name_of_process_in_db = str(etl_process.get_process_name(env, process_name))
        data['name'] = name_of_process_in_db
        url = set_base_url + PROCESS_ENABLE
        res = requests.request("POST", url, headers=admin_headers, json=data)
        print("res 是: " + res.text)

    def release_to_app_market(self, set_base_url, process_name, admin_headers, admin_user, env, org_id, tag_id):
        '''
        发布流程至应用市场
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        path = TEST_DATA_PATH + r"/release_to_app_market.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        data = param['data']
        detail = param['detail']
        print(detail + "：")
        time.sleep(3)

        org_id_list = []
        org_id_list.append(org_id)

        tag_id_list = []
        # tag_id = get_random_process_tag_id(env)
        tag_id_list.append((tag_id))

        name_of_process_in_db = str(etl_process.get_process_name(env, process_name))
        robot_process_id = str(etl_process.get_robot_process_id(env, process_name))

        time.sleep(3)
        #管理员发布流程到应用市场：
        data['authorId'] = get_user_id(env,admin_user)
        data['authorName'] = admin_user
        data['fileUrl'] = get_process_file_path(env,name_of_process_in_db)  #流程在服务器的存储地址
        data['id'] = robot_process_id
        data['pluginId'] = str(get_process_info_id(env, process_name))  # plugin_id即流程id,即process_info表中的id
        data['pluginName'] = process_name
        data['resourceSn'] = get_process_resource_sn(env, process_name)
        data['organizationIds'] = org_id_list  # 随机生成组织id
        data['tagIds'] = tag_id_list             #!!!!!!待改

        url =  set_base_url + RELEASE_TO_APP_MARKET
        res = requests.request("POST", url, headers=admin_headers, json=data,  stream=True)
        print("发布到流程市场:")
        print("res 是: " + res.text)

    def select_robot_for_process_and_run(self, set_base_url, process_name, admin_headers,  env, robot_type):
        path = TEST_DATA_PATH + r"/run_process.yml"
        info = CommonTool().get_yaml_data_info(path)
        method = info['method']
        url = info['url']
        param = CommonTool().get_yaml_data_dict(path)
        run_process = param['data']
        detail = param['detail']
        print(detail + "：")
        time.sleep(3)

        print("为流程任务选择" + robot_type + "机器人：")
        data = {}
        time.sleep(3)

        robot_org_id = ""
        # 为执行流程选择机器人：
        if robot_type == "free":
            robot_org_id = get_random_free_robot_id(env)
            robot_org_id = get_robot_organization_id(env, robot_org_id)  # 获取robotNme对应org_id
            data['robotIds'] = get_robot_id_list_by_robot_id(robot_org_id)  # 通过随机生成的机器人id获取空闲机器人id列表
        elif robot_type != "free":
            robot_org_id = get_random_not_free_robot_id(env)
            robot_org_id = get_robot_organization_id(env, robot_org_id)  # 获取robotNme对应org_id
            data['robotIds'] = get_robot_id_list_by_robot_id(robot_org_id)  # 通过随机生成的机器人id获取非机器人id列表
        else:
            robot_org_id = get_robot_organization_id(env, get_robot_id(env, data['robotName']))  # 获取robotNme对应org_id
            data['robotIds'] = get_robot_id_list(env, data['robotName'])  # 通过用例参数中指定的机器人名获取机器人id列表

        url = set_base_url + SELECT_ROBOT
        data['labelName'] = CommonTool().get_robot_temp_label_name()  # 获取随机的uuid4labelname
        res = requests.request("POST", url, headers=admin_headers, json=data, stream=True)
        print("为执行流程选择机器人:")
        print(res.text)

        time.sleep(3)

        robot_process_id = str(etl_process.get_robot_process_id(env, process_name))


        # 管理员运行流程：
        print("管理员运行流程:")
        url = set_base_url + RUN_PROCESS.replace("$xxx", robot_process_id)
        run_process['conditions'] = data['labelName']
        run_process['name'] = process_name + "_1.0.0"
        run_process['resourceSn'] = get_process_resource_sn(env, process_name)
        run_process['organizationId'] = robot_org_id

        res = requests.request("POST", url, headers=admin_headers, json=run_process, stream=True)
        print("res 是: " + res.text)
        execution_id = str(res.json()['data']['id'])
        return execution_id
        # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


    def cancle_task_before_run(self, set_base_url, execution_id, admin_headers):
        '''
        手动取消未完成的任务
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        time.sleep(3)
        url = set_base_url + CANCLE_TASK_BEFORE_RUN.replace("$xxx",execution_id)
        print("手动取消待运行任务:")
        res = requests.request("PUT", url, headers=admin_headers)
        print("res 是: " + res.text)

    def delete_task_after_finish_run(self, set_base_url, execution_id, admin_headers):
        '''
        删除已完成的任务
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        time.sleep(3)
        url = set_base_url + DELETE_TASK_After_FINISH_RUN.replace("$xxx",execution_id)
        print("删除已完成的任务:")
        res = requests.request("PUT", url, headers=admin_headers)
        print("res 是: " + res.text)

    def redo_history_task(self, set_base_url, execution_id, admin_headers):
        '''
        重新运行历史任务
        :param set_base_url:
        :param process_name:
        :param admin_headers:
        :param env:
        :return:
        '''
        time.sleep(3)
        data = {}
        data['outputParams'] = []
        data['params'] = []
        url = set_base_url + REDO_TASK.replace("$xxx",execution_id)
        print("重新运行历史任务:")
        res = requests.request("POST", url, headers=admin_headers, json=data, stream=True)
        print("res 是: " + res.text)