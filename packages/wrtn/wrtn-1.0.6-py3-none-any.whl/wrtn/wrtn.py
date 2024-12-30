#메인 클레스
class wrtn:
    #유저정보클레스
    from functions.user import user as user
    #채팅클레스
    from functions.chat import chat
    #피드클레스
    from functions.feed import feed
    #챗봇제작클레스
    from functions.charmaker import charmaker
    def __init__(self,token:str):
        self.cookie = {f"Authorization": f"Bearer {token}"}