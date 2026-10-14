from tool.send_email_tool import send_email_tool
from tool.mysql_tool import mysql_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from dotenv import load_dotenv
import os
import asyncio
import sys
load_dotenv()
#演示智能体创建
async def create_email_agent(q,user_id):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[send_email_tool,mysql_tool]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
       二 任务：
               -理解用户需求
               -先去调用工具mysql_tool查询用户的邮箱
               -调用工具send_email_tool发送邮件
    """
    url = os.getenv("POSTGRESQL_URL")

    async with AsyncPostgresSaver.from_conn_string(url) as pg:
        await pg.setup()
        # 4 创建智能体
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=prompt,
            checkpointer=pg,
            debug=True  # 可选参数，一般用于调试，生成环境必须设置未false
        )
        human_msg = {"messages": [HumanMessage(content=q)]}
        config = {"configurable": {"thread_id": user_id}}
        async for event in agent.astream_events(human_msg,config, version="v2"):
            print('11111111111',event)

            # 获取事件内容
            event_name = event["event"]
            if event_name == "on_chain_start":
                yield f"\n邮件智能体开始运行\n"
            elif event_name == "on_chat_model_start":
                yield f"\n大模型开始思考\n"
            elif event_name == "on_chat_model_end":
                yield f"\n大模型思考结束\n"
            elif event_name == "on_chain_stream":
                yield f"\n大模型开始生成答案\n"
            elif event_name == "on_tool_start":
                # 获取工具名称
                tool_name = event["name"]
                if tool_name == "mysql_tool":
                    yield f"\n开始执行mysql工具查询\n"
                if tool_name == "send_email_tool":
                    yield f"\n开始发送邮件\n"
            elif event_name == "on_tool_end":
                # 获取工具返回值
                tool_output = event["data"]["output"].content
                if tool_name == "mysql_tool":
                    yield f"\nmysql工具查询结束\n"
                if tool_name == "send_email_tool":
                    yield f"\n邮件发送结束\n"
            elif event_name == "on_chat_model_stream":
                data = event["data"]["chunk"].content
                if data:
                    yield data
#测试
async def test(q,user_id):
    async for rs in create_email_agent(q,user_id):
        print(rs, end="")

if __name__ =="__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    q="通知张三，明天上午来打dota，选火枪"
    asyncio.run(test(q,3))
# user_id在这里被当作LangGraph的thread_id（线程ID）使用，
# 其核心作用是标识一个独立的会话（Session），从而实现多用户之间的状态隔离和记忆持久化。