from langGraph_demo.demo02.state.email_state02 import EmailState
from tool.mysql_tool import mysql_tool
from langchain_core.messages import ToolMessage
import ast
"""
查询节点
"""
def query_node(state:EmailState):
    print("query_node1111111111",state)
    #获取重试次数
    count = state["count"]+1
    #获取用户姓名
    name = state["name"]
    #调用工具
    rs = mysql_tool.invoke({
        "sql":f"select `email` from user_info where user_name='{name}'"
    })
    if rs=="()":
        return {
            "messages":[ToolMessage(content="用户邮箱不存在",tool_call_id="query_node")],
            "result":"用户邮箱不存在",
            "next_step":"end", #标识结束了
            "count":count
        }
    #获取邮件
    email = ast.literal_eval(rs)
    #定义结果
    tool_msg =f"\n查询节点成功\n邮箱是:{email[0][0]}"
    return {
        "messages": [ToolMessage(content=tool_msg, tool_call_id="query_node")],
        "result": "\n用户邮箱查询成功\n",
        "email": email[0][0],
        "next_step":"email",#标识下一步走邮箱阶段
        "count":3 #跳出循环
    }