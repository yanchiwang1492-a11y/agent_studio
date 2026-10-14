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
   一 角色:  你是一个邮件发送助手
"""

# 创建内存记忆检测点
memory = InMemorySaver()

# 4 创建智能体
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt,
    checkpointer=memory
)

# 5 单个异步调用
async def create_email_agent(q, user_id):
    human_msg = {"messages": [HumanMessage(content=q)]}
    config = {"configurable": {"thread_id": user_id}}
    rs = await agent.ainvoke(human_msg, config)
    return 'qqq' + rs["messages"][-1].content


async def main():
    q_list = [
        # —— 记忆类：测试 Agent 记不记得住 ——
        "我叫张三，请用一句话简单回答",
        "我今年22岁，请用一句话简单回答",
        "我是谁，今年多大，请用一句话简单回答",
        "我最喜欢的颜色是蓝色，请用一句话简单回答",
        "我住在成都，请用一句话简单回答",
        "我养了一只叫小黑的猫，请用一句话简单回答",
        "我的职业是程序员，请用一句话简单回答",
        "我平时喜欢跑步，请用一句话简单回答",
        "我早餐一般吃包子，请用一句话简单回答",
        "我有个弟弟叫张四，请用一句话简单回答",

        # —— 记忆回溯类：让 Agent 复述上面说过的信息 ——
        "你还记得我叫什么、多大、住哪吗，请用一句话简单回答",
        "你还记得我的猫叫什么名字吗，请用一句话简单回答",
        "你还记得我弟弟叫什么吗，请用一句话简单回答",
        "你还记得我喜欢什么颜色吗，请用一句话简单回答",

        # —— 工具调用类：测试 add_tool / send_email_tool ——
        "1+2等于几，请用一句话简单回答",
        "100加200等于几，请用一句话简单回答",
        "35加47等于几，请用一句话简单回答",
        "帮我给 某人 发一封邮件，内容是'你好'，请用一句话简单回答",

        # —— 常识/闲聊类 ——
        "中国的首都是哪里，请用一句话简单回答",
        "今天适合出门吗，请用一句话简单回答",
    ]

    start = time.time()

    # 关键：每个问题一个独立 thread_id，gather 一次性全部并发
    tasks = [
        create_email_agent(q, f"thread_{i}")
        for i, q in enumerate(q_list)
    ]
    results = await asyncio.gather(*tasks)

    end = time.time()

    for i, (q, r) in enumerate(zip(q_list, results), 1):
        print(f"第{i}个问题: {q}")
        print(f"第{i}个的答案: {r}\n")

    print(f"【总耗时】{end - start:.2f} 秒")


if __name__ == "__main__":
    asyncio.run(main())