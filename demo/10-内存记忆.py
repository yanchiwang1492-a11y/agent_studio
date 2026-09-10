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
def create_email_agent(q,user_id):

    #5 提问
    #定义一个人类消息类型格式（第一种）
    #human_msg = {"messages":[{"role":"user","content":q}]}
    # 定义一个人类消息类型格式（第二种）
    human_msg = {"messages": [HumanMessage(content=q)]}
    #构建记忆配置
    config = {"configurable":{"thread_id":user_id}}
    rs = agent.invoke(human_msg,config)
    # return rs
    return '12333'+rs["messages"][-1].content


if __name__ =="__main__":

    #定义问题列表
    q_list =[
        "我叫张三",
        "我今年22岁",
        "我是谁，今年多大"
    ]
    for i in range(len(q_list)):
        print(f"第{i+1}个问题:{q_list[i]}")
        rs =create_email_agent(q_list[i],1)
        print(f"第{i + 1}个的答案:{rs}")