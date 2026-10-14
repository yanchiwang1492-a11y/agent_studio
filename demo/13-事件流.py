from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio
#演示智能体创建
async def create_email_agent(q):
    model = MyModel.get_model()
    tools=[send_email_tool,add_tool]
    prompt = """
       一 角色:  你是一个邮件发送助手
    """
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
    )

    human_msg = {"messages": [HumanMessage(content=q)]}
    async for event in agent.astream_events(human_msg,version="v2"):
        # yield "\n"
        # yield event
        #获取事件内容
        # print('11111111111',event)
        event_name = event["event"]
        if event_name =="on_chain_start":
            yield f"\n邮件智能体开始运行\n"
        elif event_name == "on_chat_model_start":
            yield f"\n大模型开始思考\n"
        elif event_name == "on_chat_model_end":
            yield f"\n大模型思考结束\n"
        elif event_name == "on_chain_stream":
            yield f"\n大模型开始生成答案\n"
        elif event_name == "on_tool_start":
            #获取工具名称
            tool_name = event["name"]
            if tool_name =="send_email_tool":
                yield f"\n开始发送邮件\n"
        elif event_name == "on_tool_end":
            #获取工具返回值
            tool_output =event["data"]["output"].content
            yield f"\n邮件工具执行完毕，返回值为：{tool_output}\n"
        elif event_name == "on_chat_model_stream":
             data = event["data"]["chunk"].content
             if data:
                 yield data


#创建一个迭代器
async def test(q):
    async for rs in create_email_agent(q):
        print(rs,end="")

if __name__ =="__main__":
        q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
        asyncio.run(test(q))