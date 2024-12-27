from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def 填表_初始化(驱动器路径, 远程调试地址):
    """
    初始化 Selenium WebDriver，连接指定的比特浏览器窗口。

    参数:
        - 驱动器路径 (str): ChromeDriver 的文件路径。
        - 远程调试地址 (str): Selenium 使用的 HTTP 地址。

    返回值:
        - WebDriver 实例: 如果初始化成功，返回 WebDriver 对象。
        - None: 如果初始化失败。

    示例:
        driver = 填表_初始化("C:\\path\\to\\chromedriver.exe", "127.0.0.1:9222")
        if driver:
            print("Selenium 初始化成功")
        else:
            print("Selenium 初始化失败")
    """
    try:
        # 配置 ChromeOptions
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", 远程调试地址)

        # 初始化 Selenium WebDriver
        chrome_service = Service(驱动器路径)
        return webdriver.Chrome(service=chrome_service, options=chrome_options)

    except Exception:
        return None