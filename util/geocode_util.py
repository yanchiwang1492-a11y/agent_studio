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
    data = rs.json()
    print('11111111111',data)
    location = data["geocodes"][0]["location"]
    print(location)
    return location
if __name__ =="__main__":
    get_code("成都")