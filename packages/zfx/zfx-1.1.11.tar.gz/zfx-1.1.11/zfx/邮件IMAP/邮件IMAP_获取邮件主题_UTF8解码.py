import email
from email.header import decode_header


def 邮件IMAP_获取邮件主题_UTF8解码(连接对象, 邮件ID):
    """
    通过邮件ID获取邮件的主题。

    参数:
        - 邮箱 (IMAP4_SSL): 已登录并进入INBOX的IMAP连接对象。
        - 邮件ID (str): 邮件ID。

    返回:
        - str 或 None: 成功返回邮件主题，失败返回 None。
    """
    try:
        status, data = 连接对象.fetch(邮件ID, "(RFC822)")
        if status != 'OK':
            return None

        邮件 = email.message_from_bytes(data[0][1])
        subject, encoding = decode_header(邮件["Subject"])[0]
        if isinstance(subject, bytes):
            # 如果subject是字节类型，则解码
            subject = subject.decode(encoding if encoding else "utf-8")
        return subject
    except Exception:
        return None