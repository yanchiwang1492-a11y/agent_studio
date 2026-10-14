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

    async for c,m in agent.astream(human_msg,stream_mode="messages"):
        #print(m)
        if c.content:
            # print(c.content)
            yield c.content
            # print('1',c.content,end="\n")
            # print('1',c.content, end="~")


# async def main():
#     q = "请给1260171885@qq.com 发送一封邮件，通知他来上课"
#     async for chunk in create_email_agent(q):
#         print('2',chunk, end=",")  # 逐块打印，不换行

async def main():
    qs = [
        "给 1260171885@qq.com 发邮件通知晚上吃面",
        "给 123@qq.com 发邮件通知开会",
        "给 nalan1655@qq.com 发邮件通知看演唱会",
    ]
    qs = [
        '一句话介绍冰岛',
        '一句话介绍不丹',
        # '一句话介绍摩纳哥',
        # '一句话介绍尼泊尔',
        # '一句话介绍马达加斯加',
        # '一句话介绍葡萄牙',
        # '一句话介绍新西兰',
        # '一句话介绍秘鲁',
        # '一句话介绍芬兰',
        # '一句话介绍柬埔寨',
    ]
    async def run_one(q):
        async for chunk in create_email_agent(q):
            print(chunk, end="")
    await asyncio.gather(*[run_one(q) for q in qs])
    # gather 内部把三个协程包装成 Task，交给事件循环。


asyncio.run(main())

#测试大模型的异步流式输出
# async def test_create_model(q):
#     # 1 创建一个大模型
#     model = MyModel.get_local_model()
#     #异步流式
#     async for c in model.astream(input=q):
#         if c.content:
#             yield c.content
# 
#
# if __name__ =="__main__":
#     q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
#
#     async def test():
#         # 运行异步函数
#         async for rs in test_create_model(q):
#             print(rs,end="")
#     asyncio.run(test())

