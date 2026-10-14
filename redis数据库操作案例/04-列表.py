import redis

client = redis.StrictRedis(host="localhost", port=6379, db=1, password='root')

def test01():
    #左边添加
    left_data = client.lpush("user1","a","b","c")
    print(left_data)
    #查询所有元素
    data =client.lrange("user1",0,-1)
    print(data)
    print("保存成功")
#存入
def test02():
    #左边添加
    left_data = client.rpush("user2","a","b","c")
    #查询所有元素
    data =client.lrange("user2",0,-1)
    print(data)
    print("保存成功")
#获取
def test03():
    #删除一个元素并且弹出一个元素
    data =client.rpop("user1")
    print(data)
#获取
def test04():
    #删除一个元素并且弹出一个元素
    data =client.lpop("user:2")
    print(data)
#截取
def test05():
    client.rpush("user1", "r1", "r2", "r3")
    #截取
    rs = client.ltrim("user1",-2,-1)
    print(rs)
    if rs:
      #获取所有元素
        data =client.lrange("user1",0,-1)
        print(data)


if __name__ =="__main__":
    test05()