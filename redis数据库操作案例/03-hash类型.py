import redis

client = redis.StrictRedis(host="localhost", port=6379, db=1,password='root')
#保存
def test01():
    #存取
    client.hset("user:6","name","李四1")
    client.hset("user:1", "email", "1111@qq.com")
    client.hset("user:1", "department", "部门")
    client.hset("user:1", "num", 10)
    client.set("user:6", '李四')
    client.set("user123", 10)
    client.set("user123",0 )
    client.set("user1234", 'a','111')
    #设置失效时间
    client.expire("user:1", 150)
    print("保持成功")
#获取
def test02():
    rs = client.hgetall("user:1")
    if rs:
      name = client.hget("user:1","name").decode()
      email = client.hget("user:1", "email").decode()
      department = client.hget("user:1", "department").decode()
      num = client.hget("user:1", "num").decode()
      print(name, email, department, num)
if __name__ =="__main__":
    test01()