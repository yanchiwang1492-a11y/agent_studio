from langchain.agents.middleware import before_model, AgentState, after_model

from langgraph.runtime import  Runtime
import re
from langchain_core.messages import AIMessage
import redis

#链接redis服务
client = redis.StrictRedis(host='localhost', port=6379, db=3, password='root')



@before_model
def model_limit_before_middleware(state:AgentState,time:Runtime):
    print('pppppppppppppp',state)
    print('5555555555555',time)
    user_id = time.execution_info.thread_id
    print(f"用户id:{user_id}")
    num =2
    #自定义键名
    # key = f"limit:{user_id}"
    key = user_id
    #获取值
    data = client.get(key)
    print('11111111111111111111',data)
    # key 不存在时，当前计数视为 0
    current = 0 if data is None else int(data.decode())

    print(f"用户id:{user_id}, 当前计数:{current}, 上限:{num}")

    if current >= num:
        raise ValueError("用户模型使用次数超过限制")

    # if data is None:
    #   return {}
    # else:
    #   data = int(data.decode())
    #   if data >= num:
    #       raise ValueError("'###############,'用户模型使用次数超过限制")
@after_model
def model_limit_after_middleware(state: AgentState, time: Runtime):
    user_id = time.execution_info.thread_id
    print(f"用户id:{user_id}")
    #自定义键名
    # key = f"limit:{user_id}"
    key = user_id

    new_value = client.incr(key, 1)  # 直接拿到自增后的整数
    if new_value == 1:
        client.expire(key, 120)

    # #设置自增,相当于i++
    # client.incr(key, 1)
    # data = client.get(key)
    # data = int(data.decode())
    # if data == 1:
    # #设置失效时间,单位是秒，2分钟
    #     client.expire(key, 120)

    print(f"(&&&&&&&&&&&&&&&&&&&用户{user_id}模型使用次数增加1")
    return {}
# 在 after_model 里，你只是做了 Redis 计数，没有修改 Agent 状态，return {} 是可有可无的
# 返回 None：表示不修改状态，等同于“无更新”。
# 返回 {}：同样表示没有要更新的字段。
# 返回 {"messages": [...]}：表示要把这些字段合并到 AgentState 中。