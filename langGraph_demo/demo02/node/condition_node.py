from langGraph_demo.demo02.state.email_state02 import EmailState
from langgraph.graph import END
#定义query节点条件路由函数
def query_router(state:EmailState):
   data = state["next_step"]
   if data =="email":
       return "a"
   else:
       return "b"

#定义router节点条件路由函数
def router_router(state:EmailState):
   data = state["agent_name"]
   if data =="email_agent":
       return "email"
   else:
       return "chat"

#定义query节点循环路由
def query_for_router(state:EmailState):
   count = state["count"]
   next_step = state["next_step"]
   if count < 3:
          return "i"
   else:
       # 判断是否识别出来
       if next_step == "email":
           return "email"
       else:
           return "end"

