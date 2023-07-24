import ast
import os
from uuid import uuid4

import yaml

from project_path import PROJECT_PATH, TEST_DATA_PATH
import time
import requests

import bcrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

from datetime import datetime
from utils.config_manager import get_config


class CommonTool:
    def get_yaml_data(self, filePath):
        resList = []  # 存放结果 [(请求1，期望响应1),(请求2，期望响应2)...]
        fo = open(filePath, 'r', encoding='utf-8')  # fileObject
        result = yaml.load(fo, Loader=yaml.FullLoader)
        fo.close()
        param = {}
        del result[0]
        for res in result:
            resList.append((res['data'], res['detail'], res['resp']))
        param['data'] = resList
        return param

    def get_yaml_data_for_req(self, filePath):
        resList = []  # 存放结果 [(请求1，期望响应1),(请求2，期望响应2)...]
        fo = open(filePath, 'r', encoding='utf-8')  # fileObject
        result = yaml.load(fo, Loader=yaml.FullLoader)
        fo.close()
        param = {}
        del result[0]



        for res in result:
            if 'submit_data' not in res.keys():
                res['submit_data'] = {}
            if 'yw_verify' not in res.keys():
                res['yw_verify'] = {}
            if 'pm_verify' not in res.keys():
                res['pm_verify'] = {}
            if 'expert_estimate' not in res.keys():
                res['expert_estimate'] = {}
            if 'tech_estimate' not in res.keys():
                res['tech_estimate'] = {}
            if 'dev_admin_estimate' not in res.keys():
                res['dev_admin_estimate'] = {}
            if 'confirm_develop_data' not in res.keys():
                res['confirm_develop_data'] = {}
            if 'process_for_requriement_release' not in res.keys():
                res['process_for_requriement_release'] = {}
            if 'release_acceptance' not in res.keys():
                res['release_acceptance'] = {}
            if 'process_estimate' not in res.keys():
                res['process_estimate'] = {}
            if 'process_enable' not in res.keys():
                res['process_enable'] = {}
            if 'release_to_app_store' not in res.keys():
                res['release_to_app_store'] = {}
            if 'select_robots_for_run_process' not in res.keys():
                res['select_robots_for_run_process'] = {}
            if 'run_process' not in res.keys():
                res['run_process'] = {}

            resList.append((res['create_data'], res['submit_data'], res['yw_verify'], res['pm_verify'], res['expert_estimate'], res['tech_estimate'], res['dev_admin_estimate'],
                            res['confirm_develop_data'],res['process_for_requriement_release'], res['release_acceptance'],
                            res['process_estimate'], res['process_enable'], res['release_to_app_store'],
                            res['select_robots_for_run_process'], res['run_process'], res['detail'], res['resp']))
        param['data'] = resList
        return param


    def get_yaml_data_info(self, filePath):
        with open(filePath, 'r', encoding='utf-8') as fp:
            param = yaml.load(fp, Loader=yaml.FullLoader)
        info = {}
        info['url'] = param[0]['url']
        info['method'] = param[0]['method']
        info['headers'] = param[0]['headers']
        return info

    def get_yaml_data_list(self, filePath):
        resList = []  # 存放结果 [(请求1，期望响应1),(请求2，期望响应2)...]
        fo = open(filePath, 'r', encoding='utf-8')  # fileObject
        result = yaml.load(fo, Loader=yaml.FullLoader)
        fo.close()
        param = {}

        del result[0]
        del result[0]
        del result[0]

        for res in result:
            if 'vzbody' not in res.keys():
                res['vzbody'] = {}
            resList.append((res['zbody'],res['vzbody'],res['dbody'], res['detail']))
        param['data'] = resList
        return param

    def get_yaml_data_info_list(self, filePath):
        with open(filePath, 'r', encoding='utf-8') as fp:
            param = yaml.load(fp, Loader=yaml.FullLoader)
        info = []

        infoA = {}
        infoA['url'] = param[0]['url']
        infoA['method'] = param[0]['method']
        infoA['headers'] = param[0]['headers']
        info.append(infoA)

        infoB = {}
        infoB['url'] = param[1]['url']
        infoB['method'] = param[1]['method']
        infoB['headers'] = param[1]['headers']
        info.append(infoB)

        infoC = {}
        infoC['url'] = param[2]['url']
        infoC['method'] = param[2]['method']
        infoC['headers'] = param[2]['headers']
        info.append(infoC)

        return info

    # def handle_param_to_list(self, param):
    #     sort_list = str.split(param, ",")
    #     param = ''
    #     for i in range(len(sort_list)):
    #         param = param + " ' " + sort_list[i] + " ' "
    #         if i < (len(sort_list) - 1):
    #             param = param + ","
    #     return param


    def handle_param_to_list(self, param, if_int):
        sort_list = str.split(param, ",")
        param = []
        for i in range(len(sort_list)):
            if if_int:
                param.append(int(sort_list[i]))
            else:
                param.append(sort_list[i])
        return param

    def get_robot_temp_label_name(self):
        return "tmplAbeL"+str(uuid4())

    #获取一个mrpax文件名
    def get_mrpax_file(self):
        file_dir = TEST_DATA_PATH + "mrpax/"
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.mrpax':  # 想要保存的文件格式
                    return file.replace(".mrpax","")

    def remove_mrpax_file(self,file_path):
        return os.remove(file_path)


    def get_conditon_str(self, table, params, is_condition_head, default_order_by=None, default_order_type=None, is_order=True, is_limit=True):
        if is_condition_head:
            condition = "WHERE "
        else:
            condition = ""
        for k, v in params.items():
            if k != "order_by" and k != "order_type" and k != "page_size" and k != "page_number":
                if k == "start_time":
                    operation = ">="
                elif k == "end_time":
                    operation = "<="
                elif k == "org_id":
                    operation = " in "
                    v = "(" + params['org_id'] + ")"
                else:
                    operation = "="

                if operation != ' in ':
                    if condition == "WHERE ":
                        condition = condition + table + "." + k + operation + "'" + str(v) + "'"
                    else:
                        condition = condition + " and " + table + "." + k + operation + "'" + str(v) + "'"
                else:
                    if condition == "WHERE ":
                        condition = condition + table + "." + k + operation + str(v)
                    else:
                        condition = condition + " and " + table + "." + k + operation + str(v)

        if is_order:
            if 'order_by' not in params and default_order_by is not None:
                params['order_by'] = default_order_by
                condition = condition + " order by " + table + "." + params['order_by']
            elif 'order_by' in params:
                condition = condition + " order by " + table + "." + params['order_by']

            if 'order_type' not in params and default_order_type is not None:
                params['order_type'] = default_order_type
                condition = condition + " " + params['order_type']
            elif 'order_type' in params:
                condition = condition + " " + params['order_type']
        if is_limit:
            if ('page_size' in params) and ('page_number' in params):
                condition = condition + " limit " + str(int(params['page_size']) * int(params['page_number'])) + "," + str(
                    params['page_size'])
            elif 'page_size' in params:
                condition = condition + " limit " + str(params['page_size'])

        if 'start_time' in params:
            condition = condition.replace(table + "." + "start_time",
                                          "DATE_FORMAT(" + table + "." + "create_at,'%%Y-%%m-%%d')")
            condition = condition.replace("'" + params['start_time'] + "'",
                                          "DATE_FORMAT('" + params['start_time'] + "', '%%Y-%%m-%%d')")
        if 'end_time' in params:
            condition = condition.replace(table + "." + "end_time",
                                          "DATE_FORMAT(" + table + "." + "create_at,'%%Y-%%m-%%d')")
            condition = condition.replace("'" + params['end_time'] + "'",
                                          "DATE_FORMAT('" + params['end_time'] + "', '%%Y-%%m-%%d')")

        return condition

    def handleDefaultOrgForleadCookpit(self,params):
        if params is not None:
            if "is_leadcookpit" in params and params['is_leadcookpit'] == 1:
                if "org_id" in params:
                    del params['org_id']
        return params

    def get_requirement_name(self):
        pre_fix = "YG自动化造数"
        localtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        name = pre_fix + localtime
        return name


    def get_token(self, role):
        env = os.environ['env']
        is_isc = os.environ['isc']
        if ast.literal_eval(is_isc):
            if role=="admin":
                username = get_config().get(env, 'isc_admin_username')
                passwd = get_config().get(env, 'isc_admin_passwd')
                params = {"password": passwd, "username": username}
            elif role=="yewu":
                username = get_config().get(env, 'isc_yw_username')
                passwd = get_config().get(env, 'isc_yw_passwd')
                params = {"password": passwd, "username": username}
            elif role=="kaifa":
                username = get_config().get(env, 'isc_kf_username')
                passwd = get_config().get(env, 'isc_kf_passwd')
                params = {"password": passwd, "username": username}
            else:
                exit("role is not exist")
        else:
            if role=="admin":
                username = get_config().get(env, 'admin_username')
                passwd = get_config().get(env, 'admin_passwd')
                params = {"password": passwd, "username": username}
            elif role=="yewu":
                username = get_config().get(env, 'yw_username')
                passwd = get_config().get(env, 'yw_passwd')
                params = {"password": passwd, "username": username}
            elif role=="yewu_leader":
                username = get_config().get(env, 'yw_leader_username')
                passwd = get_config().get(env, 'yw_leader_passwd')
                params = {"password": passwd, "username": username}
            elif role=="pm":
                username = get_config().get(env, 'pm_username')
                passwd = get_config().get(env, 'pm_passwd')
                params = {"password": passwd, "username": username}
            elif role=="expert":
                username = get_config().get(env, 'expert_username')
                passwd = get_config().get(env, 'expert_passwd')
                params = {"password": passwd, "username": username}
            elif role=="tech_leader":
                username = get_config().get(env, 'tech_l_username')
                passwd = get_config().get(env, 'tech_l_passwd')
                params = {"password": passwd, "username": username}
            elif role=="tech_ceo":
                username = get_config().get(env, 'tech_ceo_username')
                passwd = get_config().get(env, 'tech_ceo_passwd')
                params = {"password": passwd, "username": username}
            elif role=="kaifa_leader":
                username = get_config().get(env, 'dev_admin_username')
                passwd = get_config().get(env, 'dev_admin_passwd')
                params = {"password": passwd, "username": username}
            elif role=="kaifa":
                username = get_config().get(env, 'kf_username')
                passwd = get_config().get(env, 'kf_passwd')
                params = {"password": passwd, "username": username}
            else:
                exit("role is not exist")

        public_key_url = get_config().get(env, 'base_url') + get_config().get(env, 'rsa_public_key_url')
        res = requests.request("GET", public_key_url, stream=True)

        public_pem = res.json().get("data").get("key").encode("utf-8")
        with open("public.pem", "wb") as f:
            f.write(public_pem)

        # 用公钥加密并用base64转字符
        username = params.get("username").encode('utf-8')
        rsakey = RSA.importKey(open("public.pem").read())
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
        cipher_text = base64.b64encode(cipher.encrypt(username)).decode('utf-8')

        # 获取salt
        salt_url = get_config().get(env, 'base_url') + "/gateway/cs/api/public/v1/user/getSalt"
        value = cipher_text

        param = {"value": value}
        res = requests.request("GET", salt_url, params=param, stream=True)

        salt = res.json().get("data").get("salt")

        timeStr = res.json().get("data").get("time")
        tim = str(int(datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%f+08:00").timestamp() * 1000)).encode("utf-8")
        cipher_time_text = base64.b64encode(cipher.encrypt(tim)).decode('utf-8')

        # 获取token
        password = params.get("password").encode("utf-8")
        hashed = bcrypt.hashpw(password, ("$2a$10$" + salt).encode("utf-8")).decode('utf-8')

        value_for_token = cipher_text + "$s~" + hashed + ".$2" + cipher_time_text

        token_url = get_config().get(env, 'base_url') + "/gateway/cs/api/public/v3/authenticate"
        token_param = {
            "authMethod": 0,
            "value": value_for_token
        }

        res = requests.request("POST", token_url, json=token_param, stream=True)
        token = res.json().get("data").get("id_token")
        info = {}
        info['token'] = token
        info['username'] = params['username']
        return info

if __name__ == '__main__':
    # print(CommonTool().get_token("huaweicloud_province", "admin", False))
    # filePath = PROJECT_PATH + "/test_data/create_requirement.yml"
    # print(filePath)
    # print(CommonTool().get_yaml_data_for_req(filePath))
    # print(CommonTool().get_robot_id_list("huaweicloud_master", "YGROBOTNEW,stt"))
    print(CommonTool().get_mrpax_file())