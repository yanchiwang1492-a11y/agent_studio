from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain.agents.middleware import ModelCallLimitMiddleware,HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
#演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[send_email_tool,add_tool]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
    """
    try:
        # 定义人工审核中间件
        hum_middleware = HumanInTheLoopMiddleware(
             interrupt_on={ #拦截点，拦截哪些工具
                  "邮件发送工具123":{
                      "allowed_decisions": ["approve", "reject", "edit"],  # 允许的操作：批准、拒绝、编辑
                      # 根据 LangChain 官方文档，HumanInTheLoopMiddleware定义的内置决策类型是固定的，分别是：
                      # approve reject edit respond
                      "description": "11111邮件发送需要人工审核，请确认邮件内容是否正确",  # 自定义提示
                  }

             },
            description_prefix="【人工审核】"  # 公共提示前缀 # 可选

        )
        #定义检测点
        memory = InMemorySaver()
        #4 创建智能体
        agent =create_agent(
            model =model,
            tools =tools,
            system_prompt=prompt,
            debug=True, #可选参数，一般用于调试，生成环境必须设置未false
            checkpointer=memory,#记录Agent运行状体
            middleware=[hum_middleware]
        )
    except Exception as e:
      print("限制模型访问次数失败")
    #5 提问
    #定义一个人类消息类型格式（第一种）
    #human_msg = {"messages":[{"role":"user","content":q}]}
    # 定义一个人类消息类型格式（第二种）
    human_msg = {"messages": [HumanMessage(content=q)]}
    #引入记忆配置
    config = {"configurable": {"thread_id": '1'}}
    rs = agent.invoke(human_msg,config)
    print(rs)
    #模拟界面输入
    d = rs["__interrupt__"]
    # '__interrupt__':是和'messages'平级的
    print(d)
    if d:
        print("请选择操作：")
        print("   1. approve - 批准发送")
        print("   2. edit - 编辑内容后发送")
        print("   3. reject - 拒绝发送")
        choice = input("请输入你的选择：")
        if choice =="1":
            print("批准发送邮件")
            data = agent.invoke(Command(resume={"decisions": [{"type":"approve"}]}), config)
            print(data["messages"][-1].content)
        elif choice =="2":

            print("请输入编辑内容")
            to = input("请输入收件人邮箱：")
            subject = input("请输入标题")
            content = input("请输入内容")
            #构建一个修改后的工具参数对象
            p ={
                "to":to,
                "subject":subject,
                "content":content
            }
            #发送邮件
            data = agent.invoke(Command(
                resume={
                    "decisions": [
                        {"type": "edit","edited_action":{
                            "name":"send_email_tool",
                            "args":p
                        }}
                    ]
                }
            ), config)
            print(data["messages"][-1].content)
        else:
            print("拒绝发送邮件")
            reason = input("请输入拒绝理由")
            data = agent.invoke(Command(
                resume={
                    "decisions": [
                        {"type": "reject","reason":reason}
                    ]
                }
            ), config)
            print(data)
            print(data["messages"][-1].content)

    else:
        print("模型不支持")



if __name__ =="__main__":

        q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
        create_email_agent(q)