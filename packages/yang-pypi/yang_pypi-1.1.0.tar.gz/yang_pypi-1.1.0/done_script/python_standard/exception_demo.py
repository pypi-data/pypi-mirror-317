

"""异常的捕获&处理"""
def exception_handle():
    try:
        print("执行try")
        # raise Exception("引起一个异常")
        print(1 / 0)
    except ZeroDivisionError as e:
        print(e, "捕获零除异常")
    except Exception as e:
        print(e, "多except捕获")
    else:
        print("不出错就会执行else")
    finally:
        print("最终都得执行Finally")



if __name__ == '__main__':
    exception_handle()
    pass
