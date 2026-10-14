from langchain.agents.middleware.model_call_limit import ModelCallLimitExceededError
from langgraph.checkpoint.memory import InMemorySaver

from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain.agents.middleware import ModelCallLimitMiddleware
#演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    #2 创建一个工具
    tools=[send_email_tool,add_tool]
    #3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
    """
    try:
        # 限制模型访问次数
        model_limit = ModelCallLimitMiddleware(
            thread_limit=0,  # 限制次数
            exit_behavior="end"#达到限制次数后，结束会话
            # exit_behavior="error"
        # ModelCallLimitMiddleware只提供两种选择：文档明确其exit_behavior只有'end'和'error'两个选项。
        # 'end'的行为被写死为“注入一条人工AI消息”，没有留出让你传入自定义消息或回调的接口。
        )

        memory = InMemorySaver()
        config = {"configurable": {"thread_id": "email_agent_thread"}}
        #4 创建智能体
        agent =create_agent(
            model =model,
            tools =tools,
            system_prompt=prompt,
            debug=True, #可选参数，一般用于调试，生成环境必须设置未false
            middleware=[model_limit],
            # checkpointer = memory
        )
    except Exception as e:
      print("限制模型访问次数失败")
    #5 提问
    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = agent.invoke(human_msg,config)
    print(rs)
    print(rs["messages"][-1].content)

if __name__ =="__main__":

        q_list=['请给123@qq.com 发送一封邮件，通知他来上课'
                "请给125@qq.com 发送一封邮件，通知他来上课"
                '请给1260171885@qq.com 发送一封邮件，通知他来上课',
                '一句话介绍西南交大'
                ]
        [create_email_agent(q) for q in q_list]

        # 限制不起作用的原因：agent被重复创建，解决办法：
        # 需要重新创建一个函数，然后agent=creat_email_agent()，然后agenti.invoke,参考下一页的代码
        # @before_model / @after_model：这是底层装饰器。
        # 你之前用它们来手写自定义的限流逻辑（读写 Redis）。它们是构建工具，让你能自由地在模型调用前后插入任何代码。
        # ModelCallLimitMiddleware：这是一个预构建的中间件类。
        # 它的内部逻辑就是用 before_model 检查计数，用 after_model 增加计数，
        # 只不过它把计数存在了 Agent 的状态（State）里，而不是 Redis