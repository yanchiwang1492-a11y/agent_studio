import time


def task(name, seconds):
    print(f"任务 {name} 开始，需要 {seconds} 秒")
    time.sleep(seconds)  # 模拟耗时操作（比如读文件、请求网络）
    print(f"任务 {name} 完成")
    return f"{name}"



def main():
    start = time.time()

    # 三个任务依次执行，一个等一个
    result1 = task("A", 2)
    result2 = task("B", 1)
    result3 = task("C", 3)

    print(f" {result1}, {result2}, {result3}全都都完成了")
    print(f"总耗时: {time.time() - start:.2f} 秒")


if __name__ == "__main__":
    main()