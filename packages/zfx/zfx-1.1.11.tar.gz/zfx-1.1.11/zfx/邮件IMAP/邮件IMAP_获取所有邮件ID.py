def 邮件IMAP_获取所有邮件ID(连接对象):
    """
    获取所有邮件的ID。

    参数:
        - 连接对象 (IMAP4_SSL): 已登录并进入INBOX的IMAP连接对象。

    返回:
        - list: 包含所有邮件ID的列表。
    """
    try:
        状态, 邮件数据 = 连接对象.search(None, "ALL")
        if 状态 != 'OK':
            return []
        邮件ID列表 = 邮件数据[0].split()
        return 邮件ID列表
    except Exception:
        return []