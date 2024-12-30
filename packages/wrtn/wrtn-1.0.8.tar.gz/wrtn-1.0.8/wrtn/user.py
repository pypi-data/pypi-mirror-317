from variable import *
import requests
import json

class user:
    def direct_info(self,debug=False):
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)
    def nickname(self,debug=False):
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['name']
    def uid(self,debug=False):
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['wrtnUid']
    def _id(self,debug=False):
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['_id']
    def marketingAccountTerm(self,debug=False):
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['marketingTerm']
    def isNewbie(self,debug=False):
        res = requests.put(f"{url}/be/user", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']['isNewbie']
