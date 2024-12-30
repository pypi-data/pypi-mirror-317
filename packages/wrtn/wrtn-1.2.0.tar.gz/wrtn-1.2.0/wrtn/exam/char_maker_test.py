from wrtn import Wrtn

client = Wrtn(refresh_token='<refresh_TOKEN>')

data = {
            "name":"테스트7",
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
            "isCommentBlocked":False,
            "defaultStartingSetName":"기본 설정",
            "startingSets":[],
            "keywordBook":[{
                "keywords":["테스트"],
                "prompt":"테스트5",
                "name":"키워드 노트 1"
            }
            ]
        }

print(client.charmaker.modify_char(client,data,char_id="6761541db6ecfa71fbf8e414"))