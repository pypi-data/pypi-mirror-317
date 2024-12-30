import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def 谷歌填表_XPATH等待元素可见(驱动器对象, 定位值, 超时时间=30):
    """
    使用提供的WebDriver等待指定元素可见。默认定位方式为：XPATH

    参数:
        - 驱动器对象: WebDriver对象，用于控制浏览器的行为。
        - 定位值: 元素的定位值。
        - 超时时间: 等待元素可见的最长时间，单位为秒，默认为 30 秒。

    返回:
        - 如果元素可见，则返回该元素对象；如果超时未可见，则返回 None。
    """
    try:
        定位方法常量 = By.XPATH
        元素对象 = WebDriverWait(驱动器对象, 超时时间).until(EC.visibility_of_element_located((定位方法常量, 定位值)))
        time.sleep(1)
        return 元素对象
    except Exception:
        return None