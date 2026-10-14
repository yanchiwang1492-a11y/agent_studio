import asyncio
from model.my_model import MyModel


async def main():
    c = MyModel.get_model()
    q = [
        '一句话介绍你是谁',
        '一句话介绍成都',
        '一句话介绍美国',
        '一句话介绍中国的首都',
        '一句话介绍长江',
        '一句话介绍人工智能',
        '一句话介绍Python编程语言',
        '一句话介绍相对论',
        '一句话介绍咖啡',
        '一句话介绍敦煌莫高窟',
    ]

    res = await asyncio.gather(*(c.ainvoke(i) for i in q))
    return res


if __name__ == "__main__":
    res = asyncio.run(main())
    for i in res:
        print(i,end='\n')