from langchain.tools import tool
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
import smtplib

from langgraph.config import get_stream_writer

from tool.schema.send_email_schema import EmailParams

#定义工具参数的检验类
# class EmailParams(BaseModel):
#     #收件人
#     to:str = Field(...,description="收件人邮箱")
#     #邮件主题
#     subject: str = Field(..., description="邮件主题")
#     #正文
#     content: str = Field(..., description="邮件正文")

#读取配置文件
load_dotenv()
#定义工具
@tool("邮件发送工具123",args_schema=EmailParams)
def send_email_tool(to:str,subject:str,content:str)->str:
    # 如果你使用了 @tool("名字")，LangChain 会优先使用这个字符串作为工具名，而忽略函数名。否则，它将使用函数名作为工具名。
    # 如果你只写 @tool，LangChain 是不允许你传 args_schema 参数的，会报错。
    """
    发送邮件，发送通知，发送消息
    邮件开头要说一句：“哎呀呀，我是岳云鹏！”
    """
    try:
        #读取配置文件信息
        host = os.getenv("EMAIL_HOST")
        # port = os.getenv("EMAIL_PORT")
        port = os.getenv('EMAIL_PORT_TLS')
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        #判断配置是否读取成功
        if not sender or not host or not port or not password:
            return "邮件配置读取失败"
        # if not all([sender, host, port, password]):
        #     return "邮件配置读取失败"

        # 创建邮件对象
        msg = MIMEText(content)
        # MIME定义了一套规则，可以把非 ASCII 的内容（如图片、附件、中文）编码成 ASCII 文本，
        # 塞进邮件里传输；收件人的邮件客户端再根据 MIME 规则解码还原。
        # 发件人
        msg["From"] = sender
        #收件人
        msg["To"] =to
        #主题
        msg["Subject"] = subject

        # with  smtplib.SMTP_SSL(host,int(port)) as smtp:
        # with  smtplib.SMTP_SSL(host, port) as smtp:
        #     smtp.login(sender,password)
        #     smtp.sendmail(sender,to,msg.as_string())
        with smtplib.SMTP(host, port) as smtp:
            smtp.starttls()
            # Transport Layer Security
            smtp.login(sender, password)
            smtp.sendmail(sender, to, msg.as_string())

        try:
            writer = get_stream_writer()
            writer("正在连接邮件服务器哦，你知道吗？...")
            writer(f"已发送至 {to}，主题：{subject}，do you understand?")
        except Exception:
            pass

        return "邮件发送成功"
    except Exception as e:
        print(f"邮件发送异常{e}")
        return "邮件发送异常"

if __name__ =="__main__":
    rs = send_email_tool.invoke({
        "to":"1260171885@qq.com",
        "subject":"测试",
        "content":"这是一封测试邮件"
    })
    print(rs)



