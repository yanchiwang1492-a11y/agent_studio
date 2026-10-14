from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
#读取配置文件
load_dotenv()
"""
基于单例模式的模型封装
"""
class MyModel:
    #定义私有属性
    _model = None
    #定义本地模型私有属性
    _local_model=None
    #定义静态函数,在线模型
    @staticmethod
    def get_model():
        #判断_model 是否未空
        if MyModel._model is None:
            #创建模型
            MyModel._model = ChatOpenAI(
                model=os.getenv("MODEL_LINE_NAME"),
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                # 如果你在代码里写了 base_url="..."，那就用代码里写的。
                # 如果你代码里没写，它就会去环境里找 OPENAI_API_BASE 这个环境变量（我写在了.env里）。
                # 如果都没找到，它则使用官方默认的 https://api.openai.com/v1。
                # streaming=True,#开启流式输出，但这个好像可有可无
                extra_body={
                    "enable_thinking": False
                }
            )
        return MyModel._model
    #本地模型创建
    @staticmethod
    def get_local_model():
        #判断_model 是否未空
        if MyModel._local_model is None:
            #创建模型
            MyModel._local_model = ChatOpenAI(
                model= os.getenv("MODEL_LOCAL_NAME"),
                api_key="empty",
                base_url=os.getenv("LOCAL_URL"),
                # streaming=True,#开启流式输出
            )
        return MyModel._local_model
if __name__ =="__main__":
    model = MyModel.get_local_model()
    print("实际请求的 Base URL:", model.openai_api_base)
    rs = model.invoke("你是谁")
    print(rs)
