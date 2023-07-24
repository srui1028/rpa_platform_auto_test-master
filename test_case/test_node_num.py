#!/usr/bin/python
# -*- coding: UTF-8 -*-
import allure

from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema

path = TEST_DATA_PATH + r"/total_node.yml"
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
def test_node_count(set_base_url, set_user_header, rpa_platform_token,zbody, vzbody, dbody, detail):
    print("\n================================" + detail + "==================================")
    is_vc = os.environ['is_vc']
    z_node_url = set_base_url + zurl
    vz_node_url = set_base_url + vzurl
    d_node_url = set_base_url + durl

    zbody['data']['sort'] = CommonTool().handle_param_to_list(zbody['data']['sort'],False)
    zheaders = {"Authorization": rpa_platform_token}
    z_node_count = requests.request(zmethod, z_node_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    v_node_count = 0
    if is_vc == "True":
        v_node_count = requests.request(vzmethod, vz_node_url, headers=zheaders, params=vzbody['data'], stream=True).json()['data']['total']
    z_node_total_count = z_node_count + v_node_count
    dres = requests.request(dmethod, d_node_url, headers=set_user_header, params = dbody['data'], stream=True).json()['data']
    d_node_count = 0
    for i in range(len(dres)):
        d_node_count += dres[i]['amount']
    print("数据概览设备总数：" +str(d_node_count))
    print("中控设备总数：" + str(z_node_total_count) + "(中控：" + str(z_node_count) + "虚拟中控：" + str(v_node_count) + ")")
    assert z_node_total_count == d_node_count




if __name__ == '__main__':
    pytest.main(["-s","test_node_num.py"])
    # pytest.main(["-s","test_requirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])
