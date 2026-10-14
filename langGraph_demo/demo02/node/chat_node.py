from langGraph_demo.demo02.state.email_state02 import EmailState
from model.my_model import MyModel
from langchain_core.messages import AIMessage
def chat_node(state:EmailState):
    print(f"{state}")
    model = MyModel.get_model()
    rs = model.invoke(input=state["messages"][0].content)
    #ai_msg = rs.content
    ai_msg = rs.content
    return {}
