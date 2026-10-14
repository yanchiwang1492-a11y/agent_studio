from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
import json

from model.my_model import MyModel
from tool.add_tool import add_tool
from tool.send_email_tool import send_email_tool


# 演示智能体创建
def create_email_agent(q):
    # 1 创建一个大模型
    model = MyModel.get_model()
    # 2 创建一个工具
    tools = [send_email_tool, add_tool]
    # 3 创建提示词,系统提示词
    prompt = """
       一 角色:  你是一个邮件发送助手
       二 任务：
             -理解用户需求
             -生成一个不规则的4位数的数字作为验证码
             - 根据用户需求发送邮件
       三 规则：
            -验证码必须是4位
            -如果邮件发送成功，状态码是200，提示信息是 "啦啦啦，邮件发送成功"
            -如果邮件发送失败，状态码是500，提示信息是 "呱呱呱，邮件发送失败"
            - 只输出 JSON

            - 不允许输出解释说明

            - 不允许输出任何额外文字
            - JSON 必须能够被 `json.loads()` 正确解析
       四 输出
            -输出的数据格式必须是：
              {
                "data":"验证码",
                "code":"状态码",
                "msg":"提示信息"
              }
       五 示例
           - 输入: 邮箱是444444@qqq.com,发送邮件
           - 输出： {
                "data":"验证码",
                "code":"状态码",
                "msg":"提示信息"
              }
    """
    # 4 创建智能体
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompt,
        debug=True  # 可选参数，一般用于调试，生成环境必须设置未false
    )
    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = agent.invoke(human_msg)
    print(rs["messages"][-1].content)
    data = rs["messages"][-1].content
    data = get_json(data)
    print(f"兜底后的:{data}")
    # 转换为json
    data = json.loads(data)
    print(type(data))


# 提示词兜底
def get_json(text):
    if "```json" in text:
        data = text.replace("```json", "").replace("```", "")
        return data
    else:
        return text
# ```json只是有很小的几率会出现，所以这是兜底操作


if __name__ == "__main__":
    q = "发送一封邮件给1260171885@qq.com 告他说要下冰雹了"
    create_email_agent(q)