import email
from email.utils import parsedate_to_datetime


def 邮件IMAP_获取邮件收件时间(连接对象, 邮件ID):
    """
    通过邮件ID获取邮件的收件时间。

    参数:
        - 连接对象 (IMAP4_SSL): 已登录并进入INBOX的IMAP连接对象。
        - 邮件ID (str): 邮件ID。

    返回:
        - datetime 或 None: 成功返回邮件的收件时间，失败返回 None。
    """
    try:
        状态, 邮件数据 = 连接对象.fetch(邮件ID, "(RFC822)")
        if 状态 != 'OK':
            return None

        邮件 = email.message_from_bytes(邮件数据[0][1])
        邮件日期 = parsedate_to_datetime(邮件["Date"])
        return 邮件日期
    except Exception:
        return None