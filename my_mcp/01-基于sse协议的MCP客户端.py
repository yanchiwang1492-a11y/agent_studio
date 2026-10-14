import asyncio
from fastmcp import Client

#定义异步
async def test():
    try:
    #定义客户端
        async with Client("http://localhost:9000/sse",auth="123456") as client:
        # 因为这是 FastMCP 框架的约定机制：你写的 verify_token 返回 None，框架就知道「认证失败」，然后自动返回 401。
              #获取工具列表
              rs = await client.list_tools()
              print(rs)
              #调用工具
              data = await client.call_tool("send_email_tool",{"to":"1260171885@qq.com","subject":"测试","content":"这是测试"})
              print('1111111111111111111',data)
              print(data.structured_content["result"])
              data = await client.call_tool("mysql_tool",{"p": {"sql":"select * from user_info"}})
              print(data.structured_content["result"])
    except Exception as e:
        print(type(e))
        print(f"连接失败: {type(e).__name__}: {e}")

if __name__ =="__main__":
    asyncio.run(test())