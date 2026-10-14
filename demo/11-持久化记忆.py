from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
import os

load_dotenv()

#演示智能体创建
def create_email_agent(q,user_id):
    # 1 创建一个大模型
    model = MyModel.get_model()
    # 2 创建一个工具
    tools = [send_email_tool, add_tool]
    # 3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
    """
    url = os.getenv("POSTGRESQL_URL")
    #创建一个数据库链接
    with PostgresSaver.from_conn_string(url) as pg:
        #安装数据库和表
        # pg.setup()   #仅一下情况执行：第一次创建，数据库名称修改，langgraph版本更新
        # 4 创建智能体
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=prompt,
            checkpointer=pg
        )
        human_msg = {"messages": [HumanMessage(content=q)]}
        config = {"configurable": {"thread_id": user_id}}
        rs = agent.invoke(human_msg, config)
        return rs["messages"][-1].content


if __name__ =="__main__":

    #定义问题列表
    q_list =[
        "我叫李四",
        "我今年5岁",
        "我是谁，今年多大"
    ]
    for i in range(len(q_list)):
        print(f"第{i+1}个问题:{q_list[i]}")
        rs =create_email_agent(q_list[i],'yc')
        print(f"第{i + 1}个的答案:{rs}")