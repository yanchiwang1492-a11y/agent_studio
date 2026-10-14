import asyncio
import time


async def task(name, seconds):
    print(f"任务 {name} 开始，需要 {seconds} 秒")
    await asyncio.sleep(seconds)  # 模拟异步等待（不阻塞）
    print(f"任务 {name} 完成")
    return f"{name}"


async def main():
    start = time.time()

    # # 创建三个任务，同时出发
    # tasks = [
    #     asyncio.create_task(task("A", 2)),
    #     asyncio.create_task(task("B", 1)),
    #     asyncio.create_task(task("C", 3))
    # ]
    # create_task 是多余的，下面的写法更干净

    # results = await asyncio.gather(
    #     task("A", 2),
    #     task("B", 1),
    #     task("C", 3)
    # )
    # #
    # # 等待所有任务完成
    # results = await asyncio.gather(*tasks)


    # 另一种写法
    items = [("A", 2), ("B", 1), ("C", 3)]
    results = await asyncio.gather(*[task(name, sec) for name, sec in items])

    print(f"所有结果: {results}")
    print(f"总耗时: {time.time() - start:.2f} 秒")


if __name__ == "__main__":
    asyncio.run(main())