from .variable import *
import requests
import json

class charmaker:
    #챗봇제작
    def make_char(self,data :dict,debug=False)->dict:
        '''
        :param data:
        {
            "name":"테스트4",
            "description":"테스트4",
            "profileImageUrl":"<이미지url>",
            "model":"sonnet",
            "initialMessages":["테스트4"],
            "characterDetails":"테스트4",
            "situationImages":[],
            "categoryIds":["65e809f21a9eea7b2f660937"],
            "tags":[],"visibility":"public",
            "promptTemplate":"simulation",
            "isCommentBlocked":false,
            "defaultStartingSetName":"기본 설정",
            "keywordBook":[
            {
                "keywords":["테스트"],
                "prompt":"테스트4",
                "name":"키워드 노트 1"
            }
            ],
            "isAdult":false
        }
        '''
        res = requests.post(f"{url}/be/characters",headers=self.cookie,json=data)
        if res.status_code != 201 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)
    #챗봇수정
    def modify_char(self,data :dict,char_id :str,debug=False)->dict:
        '''
        :param data:
        {
            "name":"테스트6",
            "description":"테스트5",
            "profileImageUrl":"<이미지url>",
            "model":"sonnet",
            "initialMessages":["테스트5"],
            "characterDetails":"테스트5",
            "replySuggestions":["안녕 테스트5! 어떻게 지내?","테스트5, 여기서 뭐하고 있었어? 뭔가 재밌는 일이 생겼어?","오, 테스트5! 요즘 어떤 일들이 있었는지 이야기 좀 해줘, 궁금해!"],
            "chatExamples":[],
            "situationImages":[],
            "categoryIds":["65e809f21a9eea7b2f660937"],
            "tags":[],
            "visibility":"public",
            "promptTemplate":"simulation",
            "isCommentBlocked":false,
            "defaultStartingSetName":"기본 설정",
            "startingSets":[],
            "keywordBook":[{
                "keywords":["테스트"],
                "prompt":"테스트5",
                "name":"키워드 노트 1"
            }
            ]
        }
        '''
        res = requests.patch(f"{url}/be/characters/{char_id}", headers=self.cookie, json=data)
        if res.status_code != 201 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)