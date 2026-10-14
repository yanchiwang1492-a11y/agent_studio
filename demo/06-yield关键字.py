def test02():
    print("开始")
    print('啦啦啦')
    yield "hello"
    print("结束")
    yield "梅西是球王"
    print('abc')
    print('def')


if __name__=="__main__":
    # for c in test02():
    #     print(f"返回值是:{c}")
    rs = test02()
    print(rs)
    a=next(rs)
    print(a)
    a=next(rs)
    print(a)
    # next(rs)
    try:
        next(rs)  # 第 3 次：执行 abc、def，然后抛 StopIteration
    except StopIteration as e:
        pass
        # print(e)  # 打印空（多一行）
    # except Exception as e:
    #   pass

