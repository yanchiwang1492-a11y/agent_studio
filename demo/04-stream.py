from tool.send_email_tool import send_email_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
#演示智能体创建
def create_email_agent(q):
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
        # debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )
    #5 提问

    human_msg = {"messages": [HumanMessage(content=q)]}
    # agent.stream() 的函数签名：...*, stream_mode="values"...)，只能关键字传参，
    # stream_mode="messages" 每次流式返回的数据包里，装的是什么格式的内容？
    # "values"	当前状态的全部值	每次返回整个 agent 状态（包含所有历史消息），数据量大
    for c,m in agent.stream(human_msg,stream_mode="messages"):

        # print("1111111111111111",c)
        # print('2222222222222222',m)
        # print(c)

        if c.content:
            print('333333333333333333333',c.content)




if __name__ =="__main__":
    q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
    create_email_agent(q)

