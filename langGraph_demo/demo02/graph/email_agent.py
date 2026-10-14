from langgraph.graph import StateGraph,START,END
from langGraph_demo.demo02.state.email_state02 import EmailState
from langGraph_demo.demo02.node.email_node02 import email_node
from langGraph_demo.demo02.node.query_node02 import query_node
from langGraph_demo.demo02.node.internet_node02 import internet_node
from langGraph_demo.demo02.node.condition_node import query_router,router_router,query_for_router
from langGraph_demo.demo02.node.router_node02 import router_node
from langGraph_demo.demo02.node.chat_node import chat_node


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
    graph.add_node("chat",chat_node)
    graph.add_node("router",router_node)
    #画边
    #新版入口
    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",router_router,{
            "email":"internet",
            "chat":"chat"
        }
    )

    graph.add_edge("internet", "query")
    #添加条件边
    graph.add_conditional_edges(
        "query",query_router,{
            "a":"email",
            "b":END
        }
    )
    #添加循环边
    graph.add_conditional_edges(
        "query",query_for_router,{
            "i":"internet",#设置循环的前序点
            "end":END,#设置循环的结束点
            "email":"email",
        }
    )
    graph.add_edge("email", END)
    graph.add_edge("chat", END)
    #编译
    agent = graph.compile()
    return agent


