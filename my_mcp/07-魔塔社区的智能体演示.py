from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os

#基于SSE或者http协议配置MCP客户端
client = MultiServerMCPClient(
    {
        "mytool":{
             "transport":"streamable_http",
             "url":"https://mcp.api-inference.modelscope.net/bd53cd5856b645/mcp"
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
       一 角色:  你是一个聊天助手
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

        q="请爬取这个网址：https://www.swpu.edu.cn/，提取通知公告，6月16日的数据"
        q1="请爬取西南石油大学官网，提取通知公告，6月16日的数据"
        q2="2026年9月10日成都到绵阳下午两点以后的火车余票信息"
        #异步调用
        asyncio.run(create_email_agent(q2))