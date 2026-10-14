from langGraph_demo.demo01.state.email_state01 import EmailState
from tool.mysql_tool import mysql_tool
from langchain_core.messages import ToolMessage
import ast
"""
查询节点
"""
def query_node(state:EmailState):
    #获取用户姓名
    print(44444444444444444,state)
    name = state["name"]
    #调用工具
    rs = mysql_tool.invoke({
        "sql":f"select `email` from user_info where user_name='{name}'"
    })
    print(type(rs))
    print(55555555555555555,rs)
    if rs=="()":
        return {
            "messages":[ToolMessage(content="999用户邮箱不存在",tool_call_id="query_node")],
            "result":"123123用户邮箱不存在",
            "email": ""
        }
    #获取邮件
    email = ast.literal_eval(rs)
    print(type(email))
    print(66666666666666666, email)
    #定义结果
    tool_msg =f"\n99999999999999999999999999查询节点成功\n邮箱是:{email[0][0]}"
    print(77777777777777777, tool_msg)

    step = state.get("step", "start")
    print(f"step={step}")
    return {
        "messages": [ToolMessage(content=tool_msg, tool_call_id="query_node")],
        "result": "\n用户邮箱查询成功\n",
        "email": email[0][0]
    }