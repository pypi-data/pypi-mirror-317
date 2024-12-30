import requests


#메인 클레스
class Wrtn:
    # 유저정보클레스
    from .user import user
    # 채팅클레스
    from .chat import chat
    # 피드클레스
    from .feed import feed
    # 챗봇제작클레스
    from .charmaker import charmaker
    def refresh_token(self,refresh_token:str)->str:
        ''' refresh token을 사용해서 access token 와 토큰정지시간을 가져옴
        :param refresh_token: refresh token 타입 str
        :return: access_token, accessTokenExpiredAt 타입 str
        '''
        res = requests.post(url="https://api.wow.wrtn.ai/auth/refresh",headers={"Refresh":refresh_token})
        res_json = res.json()
        if res.status_code != 201:
            raise Exception(res.status_code)
        if res_json['result'] != "SUCCESS":
            raise Exception("Failed to refresh token")
        return res_json['data']['accessToken'],res_json['data']['accessTokenExpiredAt']
    def __init__(self,refresh_token:str)->None:
        '''refresh token 및 쿠키지정
        :param refresh_token: refresh_token 타입 str
        '''
        self.access_Token, self.accessTokenExpiredAt = self.refresh_token(refresh_token)
        self.cookie = {f"Authorization": f"Bearer {self.access_Token}"}