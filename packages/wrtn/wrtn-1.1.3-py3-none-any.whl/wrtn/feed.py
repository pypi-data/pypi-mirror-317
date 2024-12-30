from .variable import *
import requests
import json

#피드조회기능

class feed:
    def ranking(self,limit:int,period="daily",debug=False)->dict:
        '''랭킹목록을 가져옴
        :param limit: 가져올 개수
        :param period: 일간랭킹 월간랭킹 지정 (ex. daily,monthly)
        :param debug: response 출력 여부
        :return: 순위를 순위순으로 return
        '''
        res = requests.get(f"{url}/be/characters/ranking?limit={limit}&period={period}", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)