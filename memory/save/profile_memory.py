import redis

"""
用户画像记忆存储
"""
class ProfileMemory:

    def __init__(self,user_id):
        self.redis = redis.StrictRedis(host="localhost", port=6379, db=3, password='root')
        self.key = str(user_id)
    #保存
    def save(self ,hashkey,value):
        self.redis.hset(self.key, hashkey, value)
    #查询
    def query(self,user_id):
        #查询某个用户的用户画像
        rs = self.redis.hgetall(user_id)
        # data =""
        # if rs:
        #     for hashkey,value in rs.items():
        #         # data +=f"{hashkey.decode()}:{self.redis.hget(self.key,hashkey).decode()}\n"
        #         data += f"{hashkey.decode()}:{value.decode()}\n"
        # return data


        if rs:
            # 把 bytes 解码成 str，返回一个新字典
            return {k.decode(): v.decode() for k, v in rs.items()}
        return {'没找到哦~'}


if __name__ =="__main__":
   p = ProfileMemory(9)
   p.save("name","张三")
   p.save("age",233)
   #查询
   print(p.query(9))