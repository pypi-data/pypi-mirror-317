from wrtn import Wrtn

client = Wrtn(refresh_token='<refresh_TOKEN>')

print(client.chat.all_chat_list(client))
print(client.chat.send(client,message="안녕",room_id="<채팅방id>",isSuperMode=False))
print(client.chat.chat_log(client,room_id="<room_id>",limit=10))

