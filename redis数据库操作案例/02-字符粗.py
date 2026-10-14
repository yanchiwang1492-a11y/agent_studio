import redis

client = redis.StrictRedis(host="localhost", port=6379, db=1, password='root')
def test():

    #初始化自增变量
    client.set("count", 0)
    if client.ping():
        client.set("name", "李四")
        client.set("age", 23)
        client.set("sex", "男")
        print("数据保存成功")
        client.set("name", "张三")
        client.set("age", 22)
        client.set("sex", "女")
        # 设置过期时间，作为数据缓存使用
        client.set("address", "成都", ex=60)

        # 获取值
        if client.get("name"):
            name = client.get("name").decode()
            age = client.get("age")
            sex = client.get("sex").decode()
            print(name, age, sex)
        else:
            print("键名不存在")


    else:
        print("redis服务没有启动")
def test01():
    #自增
    client.incr("count",3)
    if client.get("count"):
        num = client.get("count").decode()
        print(f"num={num}")
def test02():
    #自减
    client.decr("count",1)
    if client.get("count"):
        num = client.get("count").decode()
        print(f"num={num}")

if __name__ =="__main__":
    test02()