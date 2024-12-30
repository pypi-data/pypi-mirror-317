from wrtn import wrtn

client = wrtn(token='<TOKEN>')

print(client.user.nickname(client))
print(client.user.uid(client))
print(client.user.direct_info(client))
