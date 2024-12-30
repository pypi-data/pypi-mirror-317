import email


def 邮件IMAP_获取邮件主题_原始(连接对象, 邮件ID):
    """
    通过邮件ID获取邮件的原始主题（不进行解码）。

    参数:
        - 邮箱 (IMAP4_SSL): 已登录并进入INBOX的IMAP连接对象。
        - 邮件ID (str): 邮件ID。

    返回:
        - str 或 None: 成功返回邮件原始主题，失败返回 None。
    """
    try:
        status, data = 连接对象.fetch(邮件ID, "(RFC822)")
        if status != 'OK':
            return None

        邮件 = email.message_from_bytes(data[0][1])
        subject = 邮件["Subject"]
        return subject
    except Exception:
        return None