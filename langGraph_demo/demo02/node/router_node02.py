from langGraph_demo.demo02.state.email_state02 import EmailState
from pydantic import BaseModel,Field
from langchain.agents import create_agent
from model.my_model import MyModel
from langchain_core.messages import AIMessage
#响应参数
class RouterResponse(BaseModel):
    agent_name:str = Field(...,description="智能名称,只有 chat_agent和 email_agent 两个可选")
    confiance: float = Field(..., description="置信度")
"""
路由节点
"""
def router_node(state:EmailState):
    model = MyModel.get_model()
    prompt ="""
         一 角色 你是一个路由助手
         二 任务 
                - 理解用户需求,根据用户问题，返回智能体名称和置信度
        三 规则
                - 你只能在以下智能体中选择一个：chat_agent, email_agent
                - 聊天智能体 chat_agent 包含业务：普通问候，闲聊内容,创造诗句
                - 邮件智能体 email_agent 包含业务：邮件发送，发送通知，发送消息
                - 置信度范围是0到1，越接近1表示置信度越高
              
        四 输出
                 - 输出以下内容:{"agent_name": "xx", "confiance": xx}
        五 示例
                 -用户输入：给张三发邮件，说今晚开会
                 -输出:{"agent_name": "email_agent", "confiance": 0.99}  
                  -用户输入：你好
                 -输出:{"agent_name": "chat_agent", "confiance": 0.99}         
    """
    agent = create_agent(
        model =model,
        tools=[],
        system_prompt=prompt,
        debug=True,
        response_format=RouterResponse
    )
    msg ={"messages":[{"role":"user","content":state["messages"][0].content}]}
    #获取结果
    rs = agent.invoke(msg)
    print(f"路由结果:{rs}")
    #把响应结果转换成字典
    json = rs["structured_response"].model_dump()
    print(f"转换结果:{json}")
    #定义AI返回的内容
    ai_msg =f"\n路由节点识别成功:\n 智能体名称:{json["agent_name"]}\n置信度:{json["confiance"]}\n"

    #只返回当前节点修改的状态信息
    return {
        "messages":[AIMessage(content=ai_msg)],
        "agent_name":json["agent_name"],
        "confiance":json["confiance"],
        "result":"路由节点识别成功"
    }

