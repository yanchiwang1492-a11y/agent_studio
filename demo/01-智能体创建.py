from tool.send_email_tool import send_email_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

def create_email_agent(q):
    model = MyModel.get_model()
    tools=[send_email_tool]
    prompt = """
       角色: 你是一个傻逼
       (这里的提示词似乎没有作用，但按理来说，AI也是会看的，帮助更好找到tool)
       
    """
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )

    #human_msg = {"messages":[{"role":"user","content":q}]}
    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = agent.invoke(human_msg)
    print(rs)
    print(rs["messages"][-1].content)

if __name__ =="__main__":
    q="请给1260171885qq邮箱 发送一封邮件，告诉他你中了500万"
    create_email_agent(q)

