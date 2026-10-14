import requests
from langchain.tools import tool
from pydantic import BaseModel,Field
from util.geocode_util import get_code
from dotenv import load_dotenv
import os
#读取配置文件
load_dotenv()
"""
参数校验类
"""
class DriverParamer(BaseModel):
    start_location:str = Field(...,description="汽车的起始点,例如：成都，绵阳")
    end_location: str = Field(..., description="汽车的目的地,例如：成都，绵阳")
@tool(args_schema=DriverParamer)
def driver_tool( start_location:str, end_location: str ) ->str:
    """
    查询汽车从起始点到目的地的路线
    """
    try:
       #计算地理编码
       start = get_code(start_location)
       end = get_code(end_location)
       url="https://restapi.amap.com/v5/direction/driving?parameters"
       params ={
           "key":os.getenv("AMAP_KEY"),
           "origin":start,
           "destination":end
       }
       # rs = requests.get(url=url,params=params).json()
       rs1 = requests.get(url=url, params=params)
       # print('55555555555555555555555',rs)
       print('55555555555555555555555',rs1)
       return rs1
       data = rs["route"]["paths"]
       print(data)
       # return data

       # 加不加.json()，agent 都能查出路线，是因为两种返回方式里「路线数据都在」——一个是结构化的，一个是被字符串化的完整响应。
       # 模型都看得懂，不影响它回答，但类型、token 消耗、代码可维护性完全不同。
       # 生产环境里还是老老实实用 .json() 提取需要的字段再返回，这才是规范写法。


    except Exception as e:
        print(f"汽车路线查询异常{e}")
        return "汽车路线查询异常"

if __name__ =="__main__":
    driver_tool.invoke({
        "start_location":"成都",
        "end_location":"南充"
    })