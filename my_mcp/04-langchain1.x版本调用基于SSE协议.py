from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
#基于SSE或者http协议配置MCP客户端
client = MultiServerMCPClient(
    {
        "mytool":{
            "transport":"sse",
            "url":"http://localhost:9000/sse",
            "headers": {"Authorization": f"Bearer 123456"}
        }
    }
)
# 基于stido协议配置
client01 = MultiServerMCPClient(
    {
        "mytool":{
             "transport":"stdio",
              "command":"python",
              "args":["02-基于stdio协议的MCP服务端.py"],
              "cwd":r"C:\Users\nalan\Desktop\Projects\agent-08-31\my_mcp"
        }
    }
)

#演示智能体创建
async def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #获取所有工具列表
    tools= await client.get_tools()
    print(tools)
    #2 创建一个工具
    #tools=[send_email_tool,add_tool]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
    """
    #4 创建智能体
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )

    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = await agent.ainvoke(human_msg)

    print(rs["messages"][-1].content)

if __name__ =="__main__":

        q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
        #异步调用
        asyncio.run(create_email_agent(q))