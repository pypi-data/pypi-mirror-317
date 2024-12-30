from wrtn import Wrtn

client = Wrtn(refresh_token='<refresh_TOKEN>')

print(client.user.nickname(client))
print(client.user.uid(client))
print(client.user.direct_info(client))
