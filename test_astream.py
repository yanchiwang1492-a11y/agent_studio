import asyncio
from model.my_model import MyModel


async def run_one(c, question):
    async for chunk in c.astream(question):
        print(getattr(chunk, 'content', chunk), end='', flush=True)
    print()  # 每条问题结束后换行


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

    # 让 10 个问题并发流式输出
    await asyncio.gather(*(run_one(c, i) for i in q))


if __name__ == "__main__":
    asyncio.run(main())