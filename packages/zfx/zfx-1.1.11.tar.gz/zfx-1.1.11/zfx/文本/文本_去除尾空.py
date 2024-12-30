def 文本_去除尾空(文本):
    """
    去除文本结尾的空格。

    参数:
        - 文本 (str): 要去除结尾空格的文本。

    返回:
        - str: 去除结尾空格的文本。如果转换失败或出现任何异常，则返回 False。

    示例:
        文本 = "Hello world   "
        结果 = 文本_去除尾空(文本)
        print(结果)  # 输出："Hello world"
    """
    try:
        去除尾空文本 = 文本.rstrip()
        return 去除尾空文本
    except Exception:  # 捕获所有异常
        return False