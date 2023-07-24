#!/usr/bin/python
# -*- coding: UTF-8 -*-
import allure

from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema

path = TEST_DATA_PATH + r"/total_requirement.yml"
info = CommonTool().get_yaml_data_info_list(path)
zmethod = info[0]['method']
zurl = info[0]['url']
zhead = info[0]['headers']

dmethod = info[2]['method']
durl = info[2]['url']
dhead = info[2]['headers']

param = CommonTool().get_yaml_data_list(path)['data']


@allure.feature('验证需求仪表盘需求总数（与中控需求列表接口返回的待评估、待审批、待开发、待发布、待验收、待上线、已上线的需求总数作对比')
@pytest.mark.datainsight
@pytest.mark.all
@pytest.mark.parametrize('zbody, vzbody, dbody, detail', param)
@allure.title("{detail}")
def test_requirement_count(set_base_url, set_user_header, rpa_platform_token,zbody,vzbody, dbody, detail):
    print("\n================================" + detail + "==================================")
    z_request_url = set_base_url + zurl
    d_request_url = set_base_url + durl

    zbody['data']['sort'] = CommonTool().handle_param_to_list(zbody['data']['sort'],False)
    zbody['data']['stageStatus'] = 1
    zheaders = {"Authorization": rpa_platform_token}
    z_req_collection_count = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    zbody['data']['stageStatus'] = 2
    z_process_dev_count = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    zbody['data']['stageStatus'] = 3
    z_be_or_will_be_online_count = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    z_req_count = z_req_collection_count + z_process_dev_count + z_be_or_will_be_online_count
    dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True)
    d_req_collection_count = dres.json()["data"][0].get("amount")
    d_process_dev_count = dres.json()["data"][1].get("amount")
    d_be_or_will_be_online_count = dres.json()["data"][2].get("amount")
    d_req_count = d_req_collection_count + d_process_dev_count + d_be_or_will_be_online_count

    print("数据概览需求总数：" +str(d_req_count))
    print("中控需求总数：" + str(z_req_count))

    print("数据概览需求收集总数：" +str(d_req_collection_count))
    print("中控需求收集总数：" + str(z_req_collection_count))

    print("数据概览需求流程开发总数：" +str(d_process_dev_count))
    print("中控需求流程开发总数：" + str(z_process_dev_count))

    print("数据概览需求运行上线总数：" +str(d_be_or_will_be_online_count))
    print("中控需求流程运行上线总数：" + str(z_be_or_will_be_online_count))

    assert d_req_collection_count == z_req_collection_count
    assert d_process_dev_count == z_process_dev_count
    assert d_be_or_will_be_online_count == z_be_or_will_be_online_count
    assert d_req_count == z_req_count




# @allure.feature('验证需求仪表盘需求收集、流程开发、运行上线总数（与卓越中心的需求列表对应状态数作对比）')
# @pytest.mark.requirement
# @pytest.mark.all
# @pytest.mark.parametrize('zbody, dbody, detail', param)
# @allure.title("{detail}")
# def test_requirement_count_of_different_type(get_status_type, set_base_url, set_user_header, rpa_platform_token,zbody, dbody, detail):
#     z_request_url = set_base_url + zurl
#     d_request_url = set_base_url + durl
#
#     if not isinstance(zbody['data']['sort'],list):
#         zbody['data']['sort'] = CommonTool().handle_param_to_list(zbody['data']['sort'], False)
#
#     zbody['data']['status'] = get_status_type['需求收集']
#
#     zheaders = {"Authorization": rpa_platform_token}
#     zres = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True)
#
#     z_count = {}
#     z_count['collection_stage_counts'] = zres.json()['page']['totalCount']
#
#     zbody['data']['status'] = get_status_type['流程开发']
#     zres = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True)
#     z_count['dev_stage_counts'] = zres.json()['page']['totalCount']
#
#     zbody['data']['status'] = get_status_type['运行上线']
#     zres = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True)
#     z_count['publish_counts'] = zres.json()['page']['totalCount']
#
#     dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True)
#
#     d_data = dres.json()['data']['content']
#
#     d_count = {}
#     d_count['collection_stage_counts'] = 0
#     d_count['dev_stage_counts'] = 0
#     d_count['publish_counts'] = 0
#     for i in range(len(d_data)):
#         if d_data[i]['status_type'] == '需求收集':
#             d_count['collection_stage_counts'] += 1
#         elif d_data[i]['status_type'] == '流程开发':
#             d_count['dev_stage_counts'] += 1
#         elif d_data[i]['status_type'] == '运行上线':
#             d_count['publish_counts'] += 1
#     assert d_count == z_count
#
#
# @allure.feature('验证需求仪表盘需求进度图数据')
# @pytest.mark.requirement
# @pytest.mark.all
# @pytest.mark.parametrize('zbody, dbody, detail', param)
# @allure.title("{detail}")
# def test_requirement_count(set_base_url, set_user_header, rpa_platform_token,zbody, dbody, detail):
#     z_request_url = set_base_url + zurl
#     d_request_url = set_base_url + durl
#
#     zbody['data']['sort'] = ['created_at', 'desc']
#     zbody['data']['status'] = CommonTool().handle_param_to_list(zbody['data']['status'],True)
#     zbody['data']['size'] = 5
#
#     dbody['data']['order_by'] = 'create_at'
#     dbody['data']['order_type'] = 'desc'
#
#
#     zheaders = {"Authorization": rpa_platform_token}
#     zres = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True)
#     dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True)
#     zdata = zres.json()['data']
#
#     z_latest_5 = {}
#     for i in range(len(zdata)):
#         z_latest_5['name'] = zdata[i]['name']
#         z_latest_5['status'] =
#
#     z_requirement_count=zres.json()['page']['totalCount']
#     d_requirement_count=dres.json()['data']['total']
#     assert z_requirement_count == d_requirement_count



if __name__ == '__main__':
    pytest.main(["-s","test_requirements.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])
