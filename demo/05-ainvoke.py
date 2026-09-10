from tool.send_email_tool import send_email_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio #异步执行库
#演示智能体创建
async def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[send_email_tool]
    #3 创建提示词,系统提示词
    prompt = """
       角色:  你是一个邮件发送助手
    """
    #4 创建智能体
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        #debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )
    #5 提问

    human_msg = {"messages": [HumanMessage(content=q)]}
    #await 等待智能体返回结果
    rs = await agent.ainvoke(human_msg)
    print(rs["messages"][-1].content)

if __name__ =="__main__":
    q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
    #运行异步函数
    asyncio.run(create_email_agent(q))

