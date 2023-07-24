#!/usr/bin/python
# -*- coding: UTF-8 -*-
import allure

from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema

path = TEST_DATA_PATH + r"/total_task.yml"
info = CommonTool().get_yaml_data_info_list(path)
zmethod = info[0]['method']
zurl = info[0]['url']
zhead = info[0]['headers']

vmethod = info[1]['method']
vurl = info[1]['url']
vhead = info[1]['headers']

dmethod = info[2]['method']
durl = info[2]['url']
dhead = info[2]['headers']

param = CommonTool().get_yaml_data_list(path)['data']


@allure.feature('验证需求仪表盘需求总数（与中控需求列表接口返回的待评估、待审批、待开发、待发布、待验收、待上线、已上线的需求总数作对比')
@pytest.mark.datainsight
@pytest.mark.all
@pytest.mark.parametrize('zbody, vzbody, dbody, detail', param)
@allure.title("{detail}")
def test_task_count(set_base_url, set_user_header, rpa_platform_token,zbody, vzbody, dbody, detail):
    print("\n================================" + detail + "==================================")
    is_vc = os.environ['is_vc']
    zurl_list = str.split(zurl,",")
    z_task_queue_url = set_base_url + zurl_list[0]
    z_task_history_url = set_base_url + zurl_list[1]
    vurl_list = str.split(vurl,",")
    vz_task_queue_url = set_base_url + vurl_list[0]
    vz_task_history_url = set_base_url + vurl_list[1]
    d_request_url = set_base_url + durl

    zbody['data']['sort'] = CommonTool().handle_param_to_list(zbody['data']['sort'],False)
    zheaders = {"Authorization": rpa_platform_token}
    z_task_queue_count = requests.request(zmethod, z_task_queue_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    z_task_history_count = requests.request(zmethod, z_task_history_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    v_task_queue_count = 0
    v_task_history_count = 0
    if is_vc == "True":
        v_task_queue_count = requests.request(vmethod, vz_task_queue_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
        v_task_history_count = requests.request(vmethod, vz_task_history_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
    z_task_total_count = z_task_queue_count + z_task_history_count + v_task_queue_count + v_task_history_count
    d_task_count = 0
    dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True).json()['data']

    for i in range(len(dres)):
        d_task_count += dres[i]['amount']


    # dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True)
    #  = dres.json()['data'][0]['task_num']
    print()
    print("数据概览任务总数：" +str(d_task_count))
    print("中控任务总数：" + str(z_task_total_count) + "(中控任务队列任务数：" + str(z_task_queue_count) + "中控历史任务任务数：" + str(z_task_history_count) +"虚拟中控任务队列任务数：" + str(v_task_queue_count) +"虚拟中控历史任务任务数：" + str(v_task_history_count) + ")")

    assert z_task_total_count == d_task_count




if __name__ == '__main__':
    pytest.main(["-s","test_task_num.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])
