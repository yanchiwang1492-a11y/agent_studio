import asyncio
from fastmcp import Client

#定义异步
async def test():
    #定义客户端
    async with Client("http://localhost:9000/sse",auth="123456") as client:
          #获取工具列表
          rs = await client.list_tools()
          print(rs)
          #调用工具
          data = await client.call_tool("send_email_tool",{"to":"1260171885@qq.com","subject":"测试","content":"这是测试"})
          print(data.structured_content["result"])
          data = await client.call_tool("mysql_tool",{"p": {"sql":"select * from user_info"}})
          print(data.structured_content["result"])

if __name__ =="__main__":
    asyncio.run(test())