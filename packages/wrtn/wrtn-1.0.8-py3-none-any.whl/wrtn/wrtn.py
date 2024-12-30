#메인 클레스
class wrtn:
    # 유저정보클레스
    from user import user
    # 채팅클레스
    from chat import chat
    # 피드클레스
    from feed import feed
    # 챗봇제작클레스
    from charmaker import charmaker
    def __init__(self,token:str):
        self.cookie = {f"Authorization": f"Bearer {token}"}