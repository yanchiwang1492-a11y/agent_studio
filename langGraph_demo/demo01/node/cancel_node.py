
from langgraph.constants import END
from langgraph.types import Command
from langGraph_demo.demo01.state.email_state01 import EmailState

def cancel_node(state: EmailState):
    print("11111111111邮件发送已取消")
    return {
        "step": "end"
    }
