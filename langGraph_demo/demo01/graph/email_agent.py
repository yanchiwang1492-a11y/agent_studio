from langgraph.graph import StateGraph,START,END

from langGraph_demo.demo01.node.cancel_node import cancel_node
from langGraph_demo.demo01.state.email_state01 import EmailState
from langGraph_demo.demo01.node.email_node01 import email_node
from langGraph_demo.demo01.node.query_node01 import query_node
from langGraph_demo.demo01.node.internet_node01 import internet_node


def router(state:EmailState):

    step = state.get("step", "start")
    print("router", step)
    if step == "end":
        return "end"
    else:
        return "email"
"""
创建一个大脑或者智能体
"""
# def email_agent():
def email_agent(checkpointer=None):  #因为人工审核而修改
    #获取图行结构
    graph = StateGraph(EmailState)
    #顺序图添加
    graph.add_node("internet1",internet_node)
    graph.add_node("query", query_node)
    graph.add_node("email",email_node)
    graph.add_node("cancel", cancel_node)
    #画边
    graph.add_edge(START, "internet1")
    graph.add_edge("internet1", "query")
    graph.add_conditional_edges("query", router,{
        "email": "email",
        "end": END
    })
    graph.add_edge("email", END)
    #graph.add_edge("cancel", END)
    #编译
    # agent = graph.compile()
    # agent = graph.compile(debug=True)
    agent = graph.compile(debug=True, checkpointer=checkpointer,interrupt_before=["email"] )    ##因为人工审核而修改
    return agent
