from langchain_core.messages import HumanMessage
from langGraph_demo.demo01.graph.email_agent import email_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langgraph.graph import END
import asyncio

memory = InMemorySaver()
graph = email_agent(memory)
# 添加记忆配置
config = {"configurable": {"thread_id": 1}}
async def test1():
    input = {"messages": [HumanMessage(content="给张三你发个邮件，说今晚开会")]}
    async for chunk, metadata in graph.astream(input,config, stream_mode="messages",):
        print('qq1111111111111111',chunk)
        print('qq2222222222222222',metadata)
        yield chunk.content

#人工审核-修改
def test01():
    async def test():
        async for rs in test1():
            print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu2111' + rs,end="")
    asyncio.run(test())
    #获取拦截的节点信息
    state = graph.get_state(config)
    print('kkkkkkkkkk',state)
    info = input("请输入修改的邮件内容")
    graph.update_state(config,{"content": info})
    #继续执行
    rs = graph.invoke(None, config)
    print('111111111',rs)
    print(rs['messages'][-1].content)
#人工审核-批准
def test02():
    async def test():
        async for rs in test1():
            print(rs,end="")
    asyncio.run(test())
    #获取拦截的节点信息
    state = graph.get_state(config)
    print(state)
    info = input("请输入批准或者拒绝:y/n")
    if info =="y":
        # 继续执行
        rs = graph.invoke(None, config)
        # 这个None是LangGraph里“从断点继续执行”的标准写法。它表示：“我没有新的输入，请从上次停下的地方继续跑。”
        print(rs)
        print(rs['messages'][-1].content)
    else:
        graph.update_state(config,{"step": "end"})
        print(f"更新的state:{state}")
        print(f"更新的state:{graph.get_state(config)}")
        #拒绝
        graph.invoke(
            Command(goto="END"),config)
        print("邮件发送取消")
        # 你问的这个问题，触及了LangGraph一个很核心的概念：invoke不只是“启动”，它还是“驱动器”。
        # graph.invoke(...)里的invoke，意思是“驱动这个图去执行”。
        # 不管是第一次启动，还是中途跳转，你都得用invoke（或astream）来“推”它一把。



if __name__=="__main__":
    test02()


# 修改了email_agent的两部分