def test02():
    print("开始")
    print('啦啦啦')
    yield "hello"
    print("结束")
    yield "你好"
    print('abc')
    print('def')


if __name__=="__main__":
    for c in test02():
        print(f"返回值是:{c}")
    # rs = test02()
    # print(f"1111111111{rs}")
    # g=next(rs)
    # print(f"22222222222{g}")
    # e = next(rs)
    # print(f"33333333333{e}")
    # d=next(rs)
    # print('333333333333333',d)
