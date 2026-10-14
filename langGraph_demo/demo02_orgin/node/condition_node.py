from langGraph_demo.demo02_orgin.state.email_state02 import EmailState

#定义query节点条件路由函数
def query_router(state:EmailState):
    print(22222222222222222222,state)
    data = state["next_step"]
    if data =="email":
       return "a"
    else:
       return "b"