from prompt.prompt_builder import PromptBuilder
from tool.send_email_tool import send_email_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
#演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools = [send_email_tool]
    #3 创建提示词,系统提示词
    # prompt = """
    #    一 角色:  你是一个邮件发送助手
    #    二 任务：
    #             1 根据用户输入问题，发送邮件
    #    三 规则：
    #            1 你只能根据用户输入问题，发送邮件
    #            2 如果不是发送邮件的问题，告知用户：只能发送邮件
    #            3 如果邮件内容为空，告知用户：邮件内容为空
    #            4 如有邮箱格式不正确。告知用户：邮箱格式不正确
    #            5 每封邮件后面都加一句 ‘你个小瘪三’
    #    四：输出：
    #           1 只能输出json格式，不能输出其他格式
    #           2 json 格式如下： {"output":"xxx"}
    #    五：示例：
    #          输入：请解释一下什么是python
    #          输出：只能发送邮件
    #          输入：请给1260171885@qq.com 发送一封邮件
    #          输出：邮件内容为空
    #
    # """
    prompt = PromptBuilder("email.yaml").build()

    #4 创建智能体
    agent = create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        debug=True #可选参数，一般用于调试，生成环境必须设置未false
    )
    #5 提问
    #定义一个人类消息类型格式（第一种）
    #human_msg = {"messages":[{"role":"user","content":q}]}
    # 定义一个人类消息类型格式（第二种）
    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = agent.invoke(human_msg)
    print(rs["messages"][-1].content)

if __name__ =="__main__":
    q="请给1260171885@qq.com 发送一封邮件，通知他来上课"
    q1="你是谁，你是干什么"
    q2="请解释一下什么是python"
    q3="请给1260171885at qq.com 发送一封邮件，通知他来上课"
    create_email_agent(q3)

