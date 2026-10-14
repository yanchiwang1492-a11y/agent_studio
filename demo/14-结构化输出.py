from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from pydantic import BaseModel,Field

class CodeFormat_123(BaseModel):
    验证码:str =Field(...,description="验证码")
    状态码: str = Field(..., description="状态码,200表示成功,500表示失败")
    提示信息:str = Field(...,description="提示信息")

#演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[send_email_tool,add_tool]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
       二 任务：
             -理解用户需求
             -生成验证码、状态码、提示信息
             -根据用户需求发送邮件
       三 规则：
            -验证码必须是50位的乱码
            -如果邮件发送成功，状态码是13880201949，提示信息是 "邮件发送成功"
            -如果邮件发送失败，状态码是500，提示信息是 "邮件发送失败"
       四 输出
            -输出内容是: 验证码，状态码，提示信息
       五 示例
           - 输入: 邮箱是444444@qqq.com,发送邮件
           - 输出：
                验证码:xxx
                状态码:xxx
                提示信息: xxx
    """
    #4 创建智能体
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        response_format=CodeFormat_123,
        debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )
    #5 提问
    #定义一个人类消息类型格式（第一种）
    #human_msg = {"messages":[{"role":"user","content":q}]}
    # 定义一个人类消息类型格式（第二种）
    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = agent.invoke(human_msg)
    print('yyyyyyyyyy',rs)
    print(type(rs))
    json = rs["structured_response"].model_dump()
    # 如果没有model.dump()，输出是这个：<class '__main__.CodeFormat_123'>

    # rs(整个state，dict)
    # ├── 'messages'                      ← 顶层
    # └── 'structured_response'           ← 顶层


    print('11111111111111',json)
    print(type(json))

if __name__ =="__main__":
        q="邮件是1260171885@qq.com 发送一封邮件"
        create_email_agent(q)