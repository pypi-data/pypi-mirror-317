from .variable import *
import requests
import json

#피드조회기능

class feed:
    def ranking(self,limit:int,period="daily",debug=False)->dict:
        '''랭킹목록을 가져옴
        :param limit: 가져올 개수
        :param period: 일간랭킹 월간랭킹 지정 (ex. daily,weekly,monthly)
        :param debug: response 출력 여부
        :return: 순위를 순위순으로 return
        '''
        res = requests.get(f"{url}/be/characters/ranking?limit={limit}&period={period}", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']

    def characters_sorted_by_likeCount(self,limit:int,debug=False)->dict:
        '''좋아요 순으로 캐릭터 가져옴
        :param limit: 가져올 캐릭터 개수
        :param debug: response 출력 여부
        :return: 종아요순으로 return
        '''
        res = requests.get(f"{url}/be/characters?limit={limit}&sort=likeCount", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']

    def characters_me_liked(self,limit:int,debug=False)->dict:
        '''내가 좋아요를 누른 캐릭터를 가져옴
        :param limit: 가져올 캐릭터 개수
        :param debug: response 출력 여부
        :return: 최신순으로 return
        '''
        res = requests.get(f"{url}/be/characters/me/liked?limit={limit}", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']