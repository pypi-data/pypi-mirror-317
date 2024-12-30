from .variable import *
import requests
import json

###채팅방기능

class chat:
    def all_chat_list(self,debug=False)->dict:
        ''' all_chat_list 는 모든 채팅방 리스트를 출력합니다.
        :param debug: response 출력 여부
        :return: 채팅방 목록을 최신순으로 딕셔너리 형식으로 return
        '''
        res = requests.get(f"{url}/be/api/v2/chat", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']

    def chat_list(self,limit:int,debug=False)->dict:
        '''채팅방의 리스트를 limit 개수만큼 출력합니다.
        :param limit: 출력할 채팅방의 개수
        :param debug: response 출력 여부
        :return: 채팅방 목록을 최신순으로 딕셔너리 형식으로 return
        '''
        res = requests.get(f"{url}/be/api/v2/chat?type=character&limit={limit}", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']
    def chat_log(self,room_id :str,limit:int,debug=False)->dict:
        '''해당하는 room_id의 채팅방의 채팅내역을 출력합니다.
        :param room_id: 채팅방의 id (ex. 67714607f21ad8d290923bb0)
        :param limit: 출력할 채팅방의 개수
        :param debug: response 출력 여부
        :return: 채팅내역을 최신순으로 limit 개수만큼 불러온후 return
        '''
        res = requests.get(f"{url2}/terry/api/v2/chat-room/{room_id}/messages?limit={limit}", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)['data']
    def send(self,room_id:str,message:str,isSuperMode:bool=False,debug=False)->str:
        ''' 채팅을 보낸후 응답결과를 받습니다
        :param room_id: 채팅방의 id (ex. 67714607f21ad8d290923bb0)
        :param message: 보낼 메시지
        :param isSuperMode: 슈퍼챗 사용여부
        :param debug: response 출력 여부
        :return: 답변 내용을 str로 return
        '''
        try:
            data = {"message":message,"reroll":False,"images":[],"isSuperMode":isSuperMode}
            #채팅 보내기
            res_send = requests.post(f"{url2}/terry/characters/chat/{room_id}/message",headers=self.cookie,json=data)
            if res_send.status_code != 201 and debug is False:
                raise Exception(res_send.status_code)
            json_res = json.loads(res_send.text)
            #채팅 받기
            res_recieve = requests.get(f"{url2}/terry/characters/chat/{room_id}/message/{json_res["data"]}",headers=self.cookie).text.split("\n\n")
            output = ""
            di = []
            for i in res_recieve:
                if i != "":
                    di.append(json.loads(i.replace("data: ", "")))
            for i in di:
                try:
                    output = output + i["chunk"]
                except:
                    pass
        except Exception as e:
            if debug is False:
                print("Char Send Error")
            if debug is True:
                print(e)

        return output
