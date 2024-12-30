from variable import *
import requests
import json

class feed:
    def ranking(self,limit:int,period="daily",debug=False)->dict:
        res = requests.get(f"{url}/be/characters/ranking?limit={limit}&period={period}", headers=self.cookie)
        if res.status_code != 200 and debug is False:
            raise Exception(res.status_code)
        return json.loads(res.text)