"""验证 mysql_tool 的 token 权限校验"""
import asyncio
from fastmcp import Client

async def test():
    # 测试 1: 正确 token，有 read 权限
    print("=" * 50)
    print("测试 1: 正确 token (123456) - 应该能调 mysql_tool")
    async with Client("http://localhost:9000/sse", auth="123456") as client:
        tools = await client.list_tools()
        print(f"  工具列表: {[t.name for t in tools]}")
        rs = await client.call_tool("mysql_tool", {"p": {"sql": "select * from user_info limit 1"}})
        print(f"  mysql_tool 返回: {rs.content}")

    print()

    # 测试 2: 错误 token - 应该被拒绝
    print("测试 2: 错误 token (wrong-token) - 应该连不上或被拒绝")
    try:
        async with Client("http://localhost:9000/sse", auth="wrong-token") as client:
            rs = await client.call_tool("mysql_tool", {"p": {"sql": "select 1"}})
            print(f"  mysql_tool 返回: {rs.content}")
    except Exception as e:
        print(f"  连接被拒绝: {e}")

    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test())
