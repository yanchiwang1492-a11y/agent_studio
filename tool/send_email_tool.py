from langchain.tools import tool
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
import smtplib

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
@tool("send_email_tool",args_schema=EmailParams)
def send_email_tool(to:str,subject:str,content:str)->str:
    """
    发送邮件，发送通知，发送消息
    邮件开头要说一句：“哎呀呀，这是智能体发的哦！”
    """
    try:
        #读取配置文件信息
        host = os.getenv("EMAIL_HOSt")
        port = os.getenv("EMAIL_PORT")
        port_tls = os.getenv('EMAIL_PORT_TLS')
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        #判断配置是否读取成功
        if not sender or not host or not port or not password:
            return "邮件配置读取失败"
        # 创建邮件对象
        msg = MIMEText(content)
        # 发件人
        msg["From"] = sender
        #收件人
        msg["To"] =to
        #主题
        msg["Subject"] = subject



        # with  smtplib.SMTP_SSL(host,int(port)) as smtp:
        with  smtplib.SMTP_SSL(host, port) as smtp:
            smtp.login(sender,password)
            smtp.sendmail(sender,to,msg.as_string())
        # with smtplib.SMTP(host, port_tls) as smtp:
        #     smtp.starttls()
        #     smtp.login(sender, password)
        #     smtp.sendmail(sender, to, msg.as_string())
        return "邮件发送成功12345"
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



