from .variable import *
import requests
import json

#유저정보기능

class user:
    def direct_info(self,debug=False)->dict:
        '''유저정보를 json그대로 가져옴
        :param debug: response 출력 여부
        :return: 유저 정보를 dict 형태로 return
        '''
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)

    def nickname(self,debug=False)->str:
        '''유저이름을 가져옴
        :param debug: response 출력 여부
        :return: 유저이름을 str로 return
        '''
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['name']

    def uid(self,debug=False)->str:
        '''유저 uid를 가져옴
        :param debug: response 출력 여부
        :return: 유저uid를 str로 return
        '''
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['wrtnUid']

    def _id(self,debug=False)->str:
        '''유저 _id를 가져옴
        :param debug: response 출력 여부
        :return: 유저_id를 str로 return
        '''
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['_id']

    def marketingAccountTerm(self,debug=False)->str:
        '''계정생성날자를 가져옴
        :param debug: response 출력 여부
        :return: 계정생성날자를 str로 return
        '''
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['marketingTerm']

    def isNewbie(self,debug=False)->bool:
        '''뉴비여부를 가져옴
        :param debug: response 출력 여부
        :return: 뉴비여부를 bool로 return
        '''
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['isNewbie']
