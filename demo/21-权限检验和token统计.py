from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from middleware.power_limit_middleware import power_limit_middleware,count_token_middleware,count_token_redis_middleware

#演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个聊天助手
    """
    try:
        # 4 创建智能体
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=prompt,
            debug=True,  # 可选参数，一般用于调试，生成环境必须设置未false
            middleware=[power_limit_middleware,count_token_redis_middleware]
        )
        human_msg = {"messages": [HumanMessage(content=q)]}

        config = {"configurable": {"thread_id": '2'}}
        rs = agent.invoke(human_msg,config)
        print('11111111111111111',rs["messages"][-1].content)
    except Exception as e:
        print(e)

if __name__ =="__main__":
        q="介绍美国"
        create_email_agent(q)