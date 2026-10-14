import redis

client = redis.StrictRedis(host="localhost",port=6379,db=1, password='root')
print(client.ping)
print(type(client.ping))
if client.ping():
   client.set("a",123)
else:
    print("redis服务没有启动")