from langchain_core.messages import HumanMessage

from langGraph_demo.demo02.graph.email_agent import email_agent

import asyncio
async def test1():

    graph = email_agent()
    input = {"messages": [HumanMessage(content="给张三发个邮件，通知他开会")],"count":0}
    async for chunk, metadata in graph.astream(input, stream_mode="messages",):
            yield chunk.content

#画流程图
def draw_graph():
    agent = email_agent()
    #画图
    data = agent.get_graph().draw_mermaid_png()
    #
    with open("循环图.png","wb") as f:
        f.write(data)
    print("循环图.png")

if __name__=="__main__":
   # draw_graph()
    async def test():
        async for rs in test1():
            print('~' + rs,end="")
    asyncio.run(test())
# asyncio.run()的作用是：创建一个事件循环，运行传入的协程直到完成，关闭事件循环
# 它是同步代码进入异步世界的入口。async for 需要一个正在运行的事件循环才能工作。