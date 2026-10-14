import asyncio
from fastmcp import Client
import os

api_key = os.getenv("DASHSCOPE_API_KEY")

#定义异步
async def test():
    #定义客户端
    async with Client("https://mcp.api-inference.modelscope.net/bd53cd5856b645/mcp") as client:
          #获取工具列表
          rs = await client.list_tools()
          print(rs)
          data = await  client.call_tool("web_fetch",{"url":"https://www.swpu.edu.cn/"})
          print(data)
          print(data.content[0].text)


if __name__ =="__main__":
    asyncio.run(test())