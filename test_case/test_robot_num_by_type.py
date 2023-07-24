#!/usr/bin/python
# -*- coding: UTF-8 -*-
import allure

from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool
from conftest import *
import datetime
# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema

path = TEST_DATA_PATH + r"/total_robot_by_type.yml"
info = CommonTool().get_yaml_data_info_list(path)
zmethod = info[0]['method']
zurl = info[0]['url']
zhead = info[0]['headers']

vzmethod = info[1]['method']
vzurl = info[1]['url']
vzhead = info[1]['headers']

dmethod = info[2]['method']
durl = info[2]['url']
dhead = info[2]['headers']

param = CommonTool().get_yaml_data_list(path)['data']


@allure.feature('验证需求仪表盘需求总数（与中控需求列表接口返回的待评估、待审批、待开发、待发布、待验收、待上线、已上线的需求总数作对比')
@pytest.mark.datainsight
@pytest.mark.all
@pytest.mark.parametrize('zbody, vzbody, dbody, detail', param)
@allure.title("{detail}")
def test_robot_count(set_base_url, set_user_header, rpa_platform_token,zbody, vzbody, dbody, detail):
    print("\n================================" + detail + "==================================")
    is_vc = os.environ['is_vc']
    z_robot_url = set_base_url + zurl
    vz_robot_url = set_base_url + vzurl
    d_robot_url = set_base_url + durl

    zbody['data']['sort'] = CommonTool().handle_param_to_list(zbody['data']['sort'],False)
    zheaders = {"Authorization": rpa_platform_token}
    z_free_robot_count = 0
    z_busy_robot_count = 0
    z_stop_to_be_used_robot_count = 0
    z_offline_robot_count = 0
    z_activating_robot_count = 0
    z_upgrading_robot_count = 0
    z_unavailable_robot_count = 0

    v_free_robot_count = 0
    v_offline_robot_count = 0
    z_res = []
    v_res = []
    z_robot_count = 0
    v_robot_count = 0
    if 'organizationIds' in zbody['data'].keys():
        z_res = requests.request(zmethod, z_robot_url, headers=zheaders, params=zbody['data'], stream=True).json()
        for i in range(len(z_res['data'])):
            if z_res['data'][i]['organizationId'] == zbody['data']['organizationIds']:
                z_robot_count += 1

        if zbody['data']['organizationIds'] == 1  and is_vc == "True":
            v_res = requests.request(vzmethod, vz_robot_url, headers=zheaders, params=vzbody['data'], stream=True).json()
            v_robot_count = v_res['data']['total']
    else:
        if is_vc == "True":
            v_res = requests.request(vzmethod, vz_robot_url, headers=zheaders, params=vzbody['data'], stream=True).json()
            v_robot_count = v_res['data']['total']
        z_res = requests.request(zmethod, z_robot_url, headers=zheaders, params=zbody['data'], stream=True).json()
        z_robot_count = z_res['page']['totalCount']

    for i in range(len(z_res['data'])):
        if 'organizationIds' in zbody['data'].keys():
            if z_res['data'][i]['organizationId'] == zbody['data']['organizationIds']:
                if z_res['data'][i]['status'] == 0:
                    z_free_robot_count += 1
                elif z_res['data'][i]['status'] == 1:
                    z_busy_robot_count += 1
                elif z_res['data'][i]['status'] == 2:
                    z_offline_robot_count += 1
                elif z_res['data'][i]['status'] == 3:
                    z_unavailable_robot_count += 1
                elif z_res['data'][i]['status'] == 77:
                    z_upgrading_robot_count += 1
                elif z_res['data'][i]['status'] == 88:
                    z_stop_to_be_used_robot_count += 1
                elif z_res['data'][i]['status'] == 99:
                    z_activating_robot_count += 1
        else:
            if z_res['data'][i]['status'] == 0:
                z_free_robot_count += 1
            elif z_res['data'][i]['status'] == 1:
                z_busy_robot_count += 1
            elif z_res['data'][i]['status'] == 2:
                z_offline_robot_count += 1
            elif z_res['data'][i]['status'] == 3:
                z_unavailable_robot_count += 1
            elif z_res['data'][i]['status'] == 77:
                z_upgrading_robot_count += 1
            elif z_res['data'][i]['status'] == 88:
                z_stop_to_be_used_robot_count += 1
            elif z_res['data'][i]['status'] == 99:
                z_activating_robot_count += 1

    if v_robot_count != 0:
        for i in range(len(v_res['data']['list'])):
            if 'organizationIds' in vzbody['data'].keys():
                if v_res['data'][i]['organizationId'] == 1:
                    if v_res['data']['list'][i]['connectStatus'] == 1:
                        v_free_robot_count += 1
                    elif v_res['data']['list'][i]['connectStatus'] == 0:
                        v_offline_robot_count += 1
            else:
                if v_res['data']['list'][i]['connectStatus'] == 1:
                    v_free_robot_count += 1
                elif v_res['data']['list'][i]['connectStatus'] == 0:
                    v_offline_robot_count += 1


    z_total_free_robot_count = z_free_robot_count + v_free_robot_count
    z_total_busy_robot_count = z_busy_robot_count
    z_total_stop_to_be_used_robot_count = z_stop_to_be_used_robot_count
    z_total_offline_robot_count = z_offline_robot_count + v_offline_robot_count
    z_total_activating_robot_count = z_activating_robot_count
    z_total_upgrading_robot_count = z_upgrading_robot_count
    z_total_unavailable_robot_count = z_unavailable_robot_count


    z_robot_total_count = z_robot_count + v_robot_count


    d_free_robot_count = 0
    d_busy_robot_count = 0
    d_stop_to_be_used_robot_count = 0
    d_offline_robot_count = 0
    d_activating_robot_count = 0
    d_upgrading_robot_count = 0
    d_unavailable_robot_count = 0

    if 'start_time' in dbody['data'].keys() and dbody['data']['start_time']  =='today':
        dbody['data']['start_time'] = str(datetime.date.today())
    if 'end_time' in dbody['data'].keys()  and dbody['data']['end_time']  =='today':
        dbody['data']['end_time'] = str(datetime.date.today())
    d_res = requests.request(dmethod, d_robot_url, headers=set_user_header, params = dbody['data'], stream=True).json()['data']


    for i in range(len(d_res)):
        if d_res[i]['status'] == 0:
            d_free_robot_count += d_res[i]['amount']
        elif d_res[i]['status'] == 1:
            d_busy_robot_count += d_res[i]['amount']
        elif d_res[i]['status'] == 2:
            d_offline_robot_count += d_res[i]['amount']
        elif d_res[i]['status'] == 3:
            d_unavailable_robot_count += d_res[i]['amount']
        elif d_res[i]['status'] == 77:
            d_upgrading_robot_count += d_res[i]['amount']
        elif d_res[i]['status'] == 88:
            d_stop_to_be_used_robot_count += d_res[i]['amount']
        elif d_res[i]['status'] == 99:
            d_activating_robot_count += d_res[i]['amount']

    d_robot_count = d_free_robot_count + d_busy_robot_count + d_stop_to_be_used_robot_count + d_offline_robot_count + d_activating_robot_count + d_upgrading_robot_count + d_unavailable_robot_count

    print("")
    print("数据概览机器人总数：" + str(d_robot_count))
    print("空闲：" + str(d_free_robot_count) + " 忙碌：" + str(d_busy_robot_count)+ " 离线：" + str(d_offline_robot_count)+ " 不可用：" + str(d_unavailable_robot_count)+ " 升级中：" + str(d_upgrading_robot_count)+ " 停用：" + str(d_stop_to_be_used_robot_count)+ " 激活中：" + str(d_activating_robot_count))
    print("中控机器人总数：" + str(z_robot_total_count) + "(中控：" + str(z_robot_count) + "虚拟中控：" + str(v_robot_count) + ")")
    print("空闲：" + str(z_total_free_robot_count) + " 忙碌：" + str(z_total_busy_robot_count)+ " 离线：" + str(z_total_offline_robot_count)+ " 不可用：" + str(z_total_unavailable_robot_count)+ " 升级中：" + str(z_total_upgrading_robot_count)+ " 停用：" + str(z_total_stop_to_be_used_robot_count)+ " 激活中：" + str(z_total_activating_robot_count))


    assert d_free_robot_count == z_total_free_robot_count
    assert d_busy_robot_count == z_total_busy_robot_count
    assert d_offline_robot_count == z_total_offline_robot_count
    assert d_unavailable_robot_count == z_total_unavailable_robot_count
    assert d_upgrading_robot_count == z_total_upgrading_robot_count
    assert d_stop_to_be_used_robot_count == z_total_stop_to_be_used_robot_count
    assert d_activating_robot_count == z_total_activating_robot_count
    assert z_robot_total_count == d_robot_count




if __name__ == '__main__':
    pytest.main(["-s","test_robot_num_by_type.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])
