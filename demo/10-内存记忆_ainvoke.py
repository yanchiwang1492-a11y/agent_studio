import asyncio
import time

from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
# 1 创建一个大模型
model = MyModel.get_model()
# 2 创建一个工具
tools = [send_email_tool, add_tool]
# 3 创建提示词,系统提示词
prompt = """
   一 角色:  你是一个回答问题的助手，回答很幽默，总是一句话回答
"""
#创建内存记忆检测点
memory = InMemorySaver()
# 4 创建智能体
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt,
    checkpointer=memory
)
#演示智能体创建
async def create_email_agent(q,user_id):

    #5 提问
    #定义一个人类消息类型格式（第一种）
    #human_msg = {"messages":[{"role":"user","content":q}]}
    # 定义一个人类消息类型格式（第二种）
    human_msg = {"messages": [HumanMessage(content=q)]}
    #构建记忆配置
    config = {"configurable":{"thread_id":user_id}}
    rs = await agent.ainvoke(human_msg,config)
    # return rs
    # return rs["messages"]
    return 'qqq'+rs["messages"][-1].content




    #定义问题列表
async def main():
    q_list = [
        # —— 记忆类：测试 Agent 记不记得住 ——
        "1 我叫张三，请用一句话简单回答",
        "2 我今年22岁，请用一句话简单回答",
        "3 我是谁，今年多大，请用一句话简单回答",
        "4 我最喜欢的颜色是蓝色，请用一句话简单回答",
        "5 我住在成都，请用一句话简单回答",
        "6 我养了一只叫小黑的猫，请用一句话简单回答",
        "7 我的职业是程序员，请用一句话简单回答",
        "8 我平时喜欢跑步，请用一句话简单回答",
        "9 我早餐一般吃包子，请用一句话简单回答",
        "10 我有个弟弟叫张四，请用一句话简单回答",

        # —— 记忆回溯类：让 Agent 复述上面说过的信息 ——
        "11 你还记得我叫什么、多大、住哪吗，请用一句话简单回答",
        "12 你还记得我的猫叫什么名字吗，请用一句话简单回答",
        "13 你还记得我弟弟叫什么吗，请用一句话简单回答",
        "14 你还记得我喜欢什么颜色吗，请用一句话简单回答",

        # —— 工具调用类：测试 add_tool / send_email_tool ——
        "15 1+2等于几，请用一句话简单回答",
        "16 100加200等于几，请用一句话简单回答",
        "17 35加47等于几，请用一句话简单回答",
        "18 帮我给 某人 发一封邮件，内容是'你好'，请用一句话简单回答",

        # —— 常识/闲聊类 ——
        "19 中国的首都是哪里，请用一句话简单回答",
        "20 今天适合出门吗，请用一句话简单回答",
    ]
    # for i in range(len(q_list)):
    #     print(f"第{i+1}个问题:{q_list[i]}")
    #     rs =await create_email_agent(q_list[i],1)
    #     print(f"第{i + 1}个的答案:{rs}")

    tasks = [create_email_agent(q, 1) for q in q_list]
    t = time.time()
    results = await asyncio.gather(*tasks)
    for i, rs in enumerate(results):
        print(f"第{i + 1}个的答案:{rs}")
    print('总时间：',time.time() - t)

    # tasks = [asyncio.create_task(create_email_agent(q, 1)) for q in q_list]
    # t = time.time()
    # for i, task in enumerate(tasks):
    #     rs = await task
    #     print(f"第{i + 1}个的答案:{rs}")
    # print(time.time() - t)

    # 两者真正开跑都要等到 await，而且都是单线程交错并发，不是物理上同时跑

if __name__ == "__main__":
    asyncio.run(main())