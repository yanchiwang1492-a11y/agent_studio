from langgraph.graph import StateGraph,START,END
from langGraph_demo.demo02_orgin.state.email_state02 import EmailState
from langGraph_demo.demo02_orgin.node.email_node02 import email_node
from langGraph_demo.demo02_orgin.node.query_node02 import query_node
from langGraph_demo.demo02_orgin.node.internet_node02 import internet_node
from langGraph_demo.demo02_orgin.node.condition_node import query_router
"""
创建一个大脑或者智能体
"""
def email_agent():
    #获取图行结构
    graph = StateGraph(EmailState)
    #顺序图添加
    graph.add_node("internet",internet_node)
    graph.add_node("query", query_node)
    graph.add_node("email",email_node)
    #画边
    #新版入口
    graph.add_edge(START, "internet")
    #旧版入门
    #graph.set_entry_point("internet")
    graph.add_edge("internet", "query")
    #添加条件边
    graph.add_conditional_edges(
        "query",query_router,{
            "a":"email",
            "b":END
        }
    )
    graph.add_edge("email", END)
    #编译
    agent = graph.compile(debug=True)
    return agent