import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

#定义客户端所在的目录
dir =r"C:\Users\nalan\Desktop\Projects\agent-08-31\mcp服务应用程序开发"
#定义你客户端的启动程序
p = "02-基于stdio协议的MCP服务端.py"
#构建命令
c = StdioServerParameters(
    command="python",#编译命令
    cwd= dir,#可选：启动程序所在目录
    args=[p]#启动程序文件
)
#定义异步函数
async  def test():
    async  with stdio_client(c) as (read,write):
        async  with ClientSession(read,write) as session:
            #初始化
            await session.initialize()
            #获取工具列表
            rs = await session.list_tools()
            print('111111111111',rs)
            #执行工具
            # 调用工具
            data = await session.call_tool("send_email_tool",
                                          {"to": "1260171885@qq.com", "subject": "aaa", "content": "123"})
            print('22222222222222',data)

            print('3333333333',data.structuredContent["result"])
            data = await session.call_tool("mysql_tool", {"p": {"sql": "select * from user_info"}}) #必须匹配服务器端的格式
            # data = await session.call_tool("mysql_tool", {"sql": "select * from user_info"})

            print('444444444444444444',data.structuredContent["result"])
if __name__ == "__main__":
    asyncio.run(test())