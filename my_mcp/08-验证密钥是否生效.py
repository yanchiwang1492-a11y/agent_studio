from fastmcp import FastMCP

from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
import smtplib
import pymysql
from my_mcp.key_verifier import  KeyVerifier
from fastmcp.server.dependencies import get_access_token
#创建应用程序
app = FastMCP(auth=KeyVerifier())

load_dotenv()
#定义mysql工具
@app.tool(name="send_email_tool")
def send_email(to:str,subject:str,content:str)->str:
    """
     描述：发送邮件
    :param to: 收件人
    :param subject:  主题
    :param content:  邮件内容
    :return: 返回成功或者失败
    """
    token =get_access_token()
    print(f"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa当前请求的访问令牌信息:{token}")
    if token.client_id =="68-C6-AC-A2-D1-F0":
        if "write" in token.scopes:
            try:
                # 读取配置文件信息
                sender = os.getenv("EMAIL_SENDER")
                host = os.getenv("EMAIL_HOSt")
                port = os.getenv("EMAIL_PORT")
                password = os.getenv("EMAIL_PASSWORD")
                # 判断配置是否读取成功
                if not to or not host or not port or not password:
                    return "邮件配置读取失败"
                # 创建邮件对象
                msg = MIMEText(content)
                # 收件人
                msg["To"] = to
                # 主题
                msg["Subject"] = subject
                # 发件人
                msg["From"] = sender
                # 创建一个链接邮件服务器的地址
                with  smtplib.SMTP_SSL(host, int(port)) as smtp:
                    # 登录邮件服务器
                    smtp.login(sender, password)
                    # 发邮件
                    smtp.sendmail(sender, to, msg.as_string())

                return "发送成功"
            except Exception as e:
                print(f"邮件发送异常{e}")
                return "邮件发送异常"
        else:
            return "访问邮件工具必须是write权限"
    else:
        return "客户端无权限"

from pydantic import BaseModel,Field
from dotenv import load_dotenv
import os

class MySQLSchema(BaseModel):
    sql:str = Field(description="sql语句")
#定义mysql
@app.tool(description="执行 sql 语句查询 数据库模型：user_info 用户信息表，字段：user_id 用户编号 user_name 用户名 email 邮箱 department 部门 num 限制数量规则:- 禁止生成DELETE,UPDATE,INSERT,DROP,CREATE,ALTER 语句")
def mysql_tool(p:MySQLSchema)->str:
    con = None
    cursor = None
    try:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        if not host or not port or not user or not password or not db_name:
            return "数据库连接参数未配置"

        #兜底操作
        sql = p.sql
        if  "DELETE" in sql.upper() or "UPDATE" in sql.upper() or "INSERT" in sql.upper() or "DROP" in sql.upper() or "CREATE" in sql.upper() or "ALTER" in sql.upper():
            return "禁止执行非法sql语句操作"
        con =pymysql.connect(
            host =host,
            port=int(port),
            user=user,
            password=password,
            db=db_name,
            charset="utf8"#中文编码设置
        )
        cursor =con.cursor()
        #执行sql
        cursor.execute(sql)
        #事务提交，非查询操作
        #con.commit()
        rs = cursor.fetchall()
        return str(rs)
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


if __name__ =="__main__":
    app.run(host="localhost",port=9000,transport="sse")