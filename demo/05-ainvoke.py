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
       角色:  你是一个回答问题小助手，每个问题后，都加一个句懂了吗
    """
    #4 创建智能体
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        # debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )
    #5 提问

    human_msg = {"messages": [HumanMessage(content=q)]}
    #await 等待智能体返回结果
    rs = await agent.ainvoke(human_msg)
#     print(rs["messages"][-1].content)
#
#
# if __name__ =="__main__":
#     q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
#     #运行异步函数
#     asyncio.run(create_email_agent(q))
    print(rs)
    print(rs["messages"][-1].content)
    return rs["messages"][-1].content  # ← 改成 return，不打印

async def main():
    qs = [
        "请给1260171885@qq.com 发送一封邮件，通知他喝酒",
        "请给nalan1655@qq.com 发送一封邮件，通知他吃薯片",
    ]
    qs = [
        '一句话介绍冰岛',
        '一句话介绍不丹',
        '一句话介绍摩纳哥',
        '一句话介绍尼泊尔',
        '一句话介绍马达加斯加',
        '一句话介绍葡萄牙',
        '一句话介绍新西兰',
        '一句话介绍秘鲁',
        '一句话介绍芬兰',
        '一句话介绍柬埔寨',
    ]
    # 并发跑两封，等两封都发完
    results = await asyncio.gather(*[create_email_agent(q) for q in qs])
    for r in results:
        print('123',r)


if __name__ == "__main__":
    asyncio.run(main())

