import asyncio
from fastmcp import Client
import os

api_key = os.getenv("DASHSCOPE_API_KEY")

#定义异步
async def test():
    #定义客户端
    async with Client("https://dashscope.aliyuncs.com/api/v1/mcps/WebFetch/mcp",
                      auth=f"Bearer {api_key}") as client:
          #获取工具列表
          rs = await client.list_tools()
          print('11111111111111',rs)
          data = await  client.call_tool("web_fetch",{"url":"https://www.scthsy.com/"})
          print('222222222',data)
          print('33333333333333333333333333',data.content[0].text)


if __name__ =="__main__":
    asyncio.run(test())