import requests
from dotenv import load_dotenv
import os
#读取配置文件
load_dotenv()
#根据地面获取地理编码
def get_code(address):
    url ="https://restapi.amap.com/v3/geocode/geo?parameters"
    params ={
        "key":os.getenv("AMAP_KEY"),
        "address":address
    }
    rs = requests.get(url=url,params=params)
    print(rs)
    print(rs.text)
    data = rs.json()
    # rs.json()  ≈  json.loads(rs.text)
    # rs.json() 做的事就是"把 rs.text 这个字符串，用 json.loads 解析成 Python 字典"。
    print(data)
    location = data["geocodes"][0]["location"]
    print(location)
    return location
if __name__ =="__main__":
    get_code("邛崃")