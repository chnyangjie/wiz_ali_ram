import json
import logging

from aliyunsdkcore.client import AcsClient
from aliyunsdkram.request.v20150501.GetUserRequest import GetUserRequest
from aliyunsdkram.request.v20150501.ListAccessKeysRequest import ListAccessKeysRequest
from aliyunsdkram.request.v20150501.ListUsersRequest import ListUsersRequest


class AliRamClient(object):

    def __init__(self, access_key_id, access_key, region):
        self.access_key_id = access_key_id
        self.access_key = access_key
        self.region = region

    def __enter__(self):
        self.client = AcsClient(self.access_key_id, self.access_key, self.region)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def query_access_key_list(self, user_name: str):
        request = ListAccessKeysRequest()
        request.set_UserName(user_name)
        response = self.client.do_action_with_exception(request).decode()
        response = json.loads(response)
        return response['AccessKeys']['AccessKey']

    def query_ram_user_info(self, user_name: str):
        request = GetUserRequest()
        request.set_UserName(user_name)
        response = self.client.do_action_with_exception(request).decode()
        response = json.loads(response)
        return response

    def query_ram_user_list(self):
        logging.info("query for instance list")
        user_list = []
        is_truncated = True
        marker = None
        max_num = 100

        while is_truncated:
            request = ListUsersRequest()
            logging.debug("request for userList")
            request.set_MaxItems(max_num)
            if marker:
                request.set_Marker(marker)
            response = self.client.do_action_with_exception(request).decode()
            response = json.loads(response)
            is_truncated = response['IsTruncated']
            if is_truncated and 'Marker' in response:
                marker = response['Marker']
                is_truncated = True
            users = response['Users']['User']
            user_list += users
        return user_list
