#!/usr/bin/python
# -*- coding: UTF-8 -*-
import allure

from project_path import TEST_DATA_PATH
from utils.common_tools import CommonTool
from conftest import *

# from utils.data_compare import assert_diff
# from utils.validate_json_schema import validate_json_schema

path = TEST_DATA_PATH + r"/total_application.yml"
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
def test_application_count(set_base_url, set_user_header, rpa_platform_token,zbody,vzbody, dbody, detail):
    print("\n================================" + detail + "==================================")
    z_request_url = set_base_url + zurl
    d_request_url = set_base_url + durl

    if zbody['data']['statusList'] == 0:
        type = "上架"
    elif zbody['data']['statusList'] == 2:
        type = "驳回"
    elif zbody['data']['statusList'] == 1:
        type = "下架"

    zbody['data']['sort'] = CommonTool().handle_param_to_list(zbody['data']['sort'],False)
    zheaders = {"Authorization": rpa_platform_token}
    z_online_application_count = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    dres = requests.request(dmethod, d_request_url, headers=set_user_header, params = dbody['data'], stream=True).json()['data']
    d_application_count = 0
    d_total = 0


    for i in range(len(dres)):
        d_total += dres[i]['amount']
        if zbody['data']['statusList'] == 2:
            dres[i]['status'] = 3
        if zbody['data']['statusList'] == 3:
            dres[i]['status'] = 2
        if dres[i]['status'] == zbody['data']['statusList']:
            d_application_count += dres[i]['amount']

    zbody['data']['statusList']=''
    z_total = requests.request(zmethod, z_request_url, headers=zheaders, params=zbody['data'], stream=True).json()['page']['totalCount']
    z_put_on_shavles_rate = round((z_online_application_count / z_total) * 100, 2)

    d_put_on_shavles_rate = round((d_application_count / d_total) * 100, 2)

    print("")
    print("数据概览应用" + type + "总数：" +str(d_application_count) + "  " + type + "率： " + str(d_put_on_shavles_rate))
    print("中控应用" + type + "总数：" + str(z_online_application_count) + "    " + type + "率： " + str(z_put_on_shavles_rate))
    assert d_application_count == z_online_application_count
    assert d_put_on_shavles_rate == z_put_on_shavles_rate




if __name__ == '__main__':
    # pytest.main(["-s", "test_application_num.py"])
    pytest.main(["-m","datainsight"])
    # pytest.main(["-s","test_req
    # uirement.py", "--env ali_master","-sq", "--alluredir", "./outputs/reports/raw"])
    # # os.system("allure generate ../reports/ -o ./outputs/reports/html --clean ")
    # pass
    # pytest.main(["-s","--env ali_master", "-v", "-q", 'test_requirement.py'])
