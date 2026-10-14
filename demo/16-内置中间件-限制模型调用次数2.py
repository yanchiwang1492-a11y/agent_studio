from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel


def build_agent():
    """创建 agent（只创建一次，供多次 invoke 复用）"""
    model = MyModel.get_model()

    tools = [send_email_tool, add_tool]

    prompt = """
       一 角色: 你是一个邮件发送助手
       二 任务:
            - 理解用户需求
            - 根据用户需求发送邮件
    """

    # 线程级限制：同一 thread_id 累计最多 2 次模型调用
    model_limit = ModelCallLimitMiddleware(
        thread_limit=2,
        # 如果设置为3，则只能用2次，第3次就不能用了
        # 如果设置为0，一次都不能用，如果设置为1，只能用1次，如果设置为2，也是只能用1次
        exit_behavior="end"      # 超限后注入一条 AIMessage 并结束
    )

    # 关键 1：checkpointer，持久化计数
    memory = InMemorySaver()

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
        debug=True,              # 调试用，生产改 False
        middleware=[model_limit],
        checkpointer=memory      # ← 必须
    )
    return agent


def main():
    agent = build_agent()        # 关键 3：agent 只创建一次

    # 关键 2：同一个 thread_id，让多次调用共享计数
    config = {"configurable": {"thread_id": 5}}

    q_list = [
        '请给123@qq.com 发送一封邮件，通知他来上课',
        '一句话介绍沙特',
        '请给1260171885@qq.com 发送一封邮件，通知他来上课',
        '一句话介绍西南交大',
    ]

    for i, q in enumerate(q_list, 1):
        print(f"\n========== 第 {i} 次提问 ==========")
        print(f"问题: {q}")
        try:
            rs = agent.invoke(
                {"messages": [HumanMessage(content=q)]},
                config              # ← 必须传，且 thread_id 保持一致
            )
            print("回复:", rs["messages"][-1].content)
        except Exception as e:
            print("异常:", e)


if __name__ == "__main__":
    main()