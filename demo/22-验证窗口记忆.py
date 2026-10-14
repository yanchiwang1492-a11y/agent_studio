from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from memory.manager.session_mananger import SessionManager


# 演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    # 2 创建一个工具
    tools = [send_email_tool, add_tool]
    # 3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个聊天助手
       二 任务:
              - 理解用户问题，回答用户问题
       三 规则：
             -你只需要回答用户问题，不需要每次携带记忆内容

    """
    # 4 创建智能体
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
        # debug=True  # 可选参数，一般用于调试，生成环境必须设置未false
    )

    # 创建会话管理器
    session_manager = SessionManager("001",'002')
    # 添加窗口记忆
    session_manager.save("user", q)
    # 构建记忆的提示词
    memory_prompt = session_manager.build_prompt('002',q)
    human_msg = {"messages": [HumanMessage(content=q), memory_prompt]}
    rs = agent.invoke(human_msg)
    # 添加AI回复的记忆
    session_manager.save("ai", rs["messages"][-1].content)
    print(rs["messages"][-1].content)


if __name__ == "__main__":
    q1 = "我叫张三，今年23岁"
    q2 = "我喜欢打篮球"
    q3 = "我在学习langchain"
    q4 = "我在学习什么"
    q5 = "我是谁，今年多大了"
    for q in [q1, q2, q3, q4, q5]:
        print("---------------------")
        create_email_agent(q)