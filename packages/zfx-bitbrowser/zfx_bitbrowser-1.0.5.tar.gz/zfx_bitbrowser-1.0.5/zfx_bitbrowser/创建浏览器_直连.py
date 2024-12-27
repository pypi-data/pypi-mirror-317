import requests
import json
import random
import time  # 用于引入延时


def 创建浏览器_直连(浏览器名称):
    """
    创建比特浏览器窗口。

    参数:
        - 浏览器名称 (str): 创建的浏览器窗口名称。

    返回值:
        - str: 返回新创建的浏览器窗口ID（成功时）。
        - None: 如果创建失败，则返回 None。

    注意:
        - 服务地址已默认设置为 'http://127.0.0.1:54345'。
        - 内核版本会随机从指定列表中选择。
        - 每次启动时会随机生成指纹，默认为 True。
    """
    # 默认服务地址
    服务地址 = "http://127.0.0.1:54345"

    # 可用内核版本列表
    内核版本列表 = ["130", "128", "126", "124", "122", "118", "112"]

    # 随机选择一个内核版本
    随机内核版本 = random.choice(内核版本列表)

    try:
        # 默认请求头
        请求头 = {'Content-Type': 'application/json'}

        # 构建请求数据
        请求数据 = {
            'name': 浏览器名称,
            'proxyMethod': 2,  # 默认自定义代理
            'proxyType': 'noproxy',  # 默认无代理
            'ostype': 'PC',  # 操作系统平台 PC|Android|IOS
            'randomFingerprint': True,  # 默认随机指纹
            "isIpCreateLanguage": True,  # 是否基于IP生成对应国家的浏览器语言
            "browserFingerPrint": {
                "coreVersion": 随机内核版本,  # 随机选择的内核版本
                "userAgent": ""  # 留空让浏览器自动生成 User-Agent
            }
        }

        # 发送创建浏览器窗口的请求
        响应 = requests.post(f"{服务地址}/browser/update",
                             data=json.dumps(请求数据), headers=请求头)

        # 检查响应状态
        if 响应.status_code == 200:
            响应数据 = 响应.json()
            if 响应数据.get('success'):
                time.sleep(1)  # 创建成功后延时 1 秒
                return 响应数据['data']['id']
        return None

    except Exception:
        return None
