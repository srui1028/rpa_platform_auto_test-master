from uuid import uuid4

import requests

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