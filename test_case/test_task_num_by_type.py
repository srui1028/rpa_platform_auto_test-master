#!/usr/bin/python
# -*- coding: UTF-8 -*-
import allure

from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool
from conftest import *
import datetime

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema

path = TEST_DATA_PATH + r"/total_task_by_type.yml"
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

    query = ''
    if 'organizationIds' in zbody['data'].keys():
        query = query + "organizationIds:[+"+ str(zbody['data']['organizationIds']) + "]"
    # if 'createdAt' in zbody['data'].keys():
    #     date = str(datetime.date.today())
    #     time = "createdAt:[" + date + "T00:00:00+08:00 TO " + date + "T23:59:59+08:00]"
    #     if query != '':
    #         query = query + " AND "
    #     query = query + time
    if query != '':
        query = query + " AND "
    zbody['data']['query']= query +'status:[0]'
    z_will_be_run_task_count = requests.request(zmethod, z_task_queue_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    zbody['data']['query'] = query + 'status:[1]'
    z_running_task_count = requests.request(zmethod, z_task_queue_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    zbody['data']['query']= query + 'status:[2]'
    z_success_task_count = requests.request(zmethod, z_task_history_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    zbody['data']['query'] = query + 'status:[3]'
    z_error_task_count = requests.request(zmethod, z_task_history_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    zbody['data']['query'] = query + 'status:[4]'
    z_be_stop_task_count = requests.request(zmethod, z_task_history_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    z_finishied_task_count = z_success_task_count + z_error_task_count + z_be_stop_task_count
    z_unfinishied_task_count = z_will_be_run_task_count + z_running_task_count


    # if 'startTriggeredAt' in vzbody['data'].keys() and 'endTriggeredAt' in vzbody['data'].keys():
    #     date = str(datetime.date.today())
    #     vzbody['data']['startTriggeredAt'] = date + " 00:00:00"
    #     vzbody['data']['endTriggeredAt'] = date + " 23:59:59"

    vz_will_be_run_task_count = 0
    vz_running_task_count = 0
    vz_success_task_count = 0
    vz_error_task_count = 0
    vz_be_stop_task_count = 0

    if is_vc == "True":
        vzbody['data']['statusList'] = 0
        vz_will_be_run_task_count = requests.request(vmethod, vz_task_queue_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
        vzbody['data']['statusList'] = 1
        vz_running_task_count = requests.request(vmethod, vz_task_queue_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
        vzbody['data']['statusList'] = 2
        vz_success_task_count = requests.request(vmethod, vz_task_history_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
        vzbody['data']['statusList'] = 3
        vz_error_task_count = requests.request(vmethod, vz_task_history_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
        vzbody['data']['statusList'] = 4
        vz_be_stop_task_count = requests.request(vmethod, vz_task_history_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
    vz_finishied_task_count = vz_success_task_count + vz_error_task_count + vz_be_stop_task_count
    vz_unfinishied_task_count = vz_will_be_run_task_count + vz_running_task_count


    z_total_running_task_count = z_running_task_count + vz_running_task_count
    z_total_will_be_run_task_count = z_will_be_run_task_count + vz_will_be_run_task_count
    z_total_success_task_count = z_success_task_count + vz_success_task_count
    z_total_be_stop_task_count = z_be_stop_task_count + vz_be_stop_task_count
    z_total_error_task_count = z_error_task_count + vz_error_task_count
    z_total_finishied_task_count = z_finishied_task_count + vz_finishied_task_count
    z_total_unfinishied_task_count = z_unfinishied_task_count + vz_unfinishied_task_count

    z_task_total_count = z_total_unfinishied_task_count +  z_total_finishied_task_count
    z_task_queue_count = z_total_unfinishied_task_count
    z_task_history_count = z_total_unfinishied_task_count

    vz_task_queue_count = vz_unfinishied_task_count
    vz_task_history_count = vz_finishied_task_count

    d_task_count = 0
    d_running_task_count = 0  #status=1
    d_will_be_run_task_count = 0  #status=0
    d_success_task_count = 0 #status=2
    d_be_stop_task_count = 0 #status=4
    d_error_task_count = 0 #status=3
    d_finishied_task_count = 0
    d_unfinishied_task_count = 0

    dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True).json()['data']
    for i in range(len(dres)):
        d_task_count += dres[i]['amount']
        if dres[i]['status'] == 0:
            d_will_be_run_task_count += dres[i]['amount']
            d_unfinishied_task_count += dres[i]['amount']
        if dres[i]['status'] == 1:
            d_running_task_count += dres[i]['amount']
            d_unfinishied_task_count += dres[i]['amount']
        if dres[i]['status'] == 2:
            d_success_task_count += dres[i]['amount']
            d_finishied_task_count += dres[i]['amount']
        if dres[i]['status'] == 3:
            d_error_task_count += dres[i]['amount']
            d_finishied_task_count += dres[i]['amount']
        if dres[i]['status'] == 4:
            d_be_stop_task_count += dres[i]['amount']
            d_finishied_task_count += dres[i]['amount']
    # dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True)
    #  = dres.json()['data'][0]['task_num']
    print()
    print("数据概览任务总数：" +str(d_task_count))
    print("中控任务总数：" + str(z_task_total_count) + "(中控任务队列任务数：" + str(z_task_queue_count) + "中控历史任务任务数：" + str(z_task_history_count) +"虚拟中控任务队列任务数：" + str(vz_task_queue_count) +"虚拟中控历史任务任务数：" + str(vz_task_history_count) + ")")

    print("数据概览：")
    print("待运行：" + str(d_will_be_run_task_count)  + " 运行中：" + str(d_running_task_count)  + " 成功：" + str(d_success_task_count) + " 异常：" + str(d_error_task_count) + " 手动取消：" + str(d_be_stop_task_count) + " 已完成：" + str(d_finishied_task_count) + " 未完成：" + str(d_unfinishied_task_count))
    print("中控：")
    print("待运行：" + str(z_will_be_run_task_count)  + " 运行中：" + str(z_total_running_task_count)  + " 成功：" + str(z_total_success_task_count) + " 异常：" + str(z_total_error_task_count) + " 手动取消：" + str(z_total_be_stop_task_count) + " 已完成：" + str(z_total_finishied_task_count) + " 未完成：" + str(z_total_unfinishied_task_count))

    assert z_task_total_count == d_task_count
    assert z_total_will_be_run_task_count == d_will_be_run_task_count
    assert z_total_success_task_count == d_success_task_count
    assert z_total_be_stop_task_count == d_be_stop_task_count
    assert z_total_error_task_count == d_error_task_count
    assert z_total_finishied_task_count == d_finishied_task_count
    assert z_total_unfinishied_task_count == d_unfinishied_task_count




if __name__ == '__main__':
    pytest.main(["-s","test_task_num_by_type.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])
