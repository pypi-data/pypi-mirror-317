import requests
import json


def 启动浏览器(浏览器ID):
    """
    启动指定的比特浏览器窗口。

    参数:
        - 浏览器ID (str): 要启动的浏览器窗口ID。

    返回值:
        - dict: 返回启动后的浏览器信息，包括 WebSocket 和 HTTP 连接地址。
        - None: 如果启动失败，则返回 None。

    注意:
        - 服务地址已默认设置为 'http://127.0.0.1:54345'。
        - 浏览器ID 必须是有效的窗口ID。
    """

    # 默认服务地址
    服务地址 = "http://127.0.0.1:54345"

    try:
        # 默认请求头
        请求头 = {'Content-Type': 'application/json'}

        # 构建请求数据
        请求数据 = {"id": 浏览器ID}

        # 发送启动请求
        响应 = requests.post(f"{服务地址}/browser/open",
                             data=json.dumps(请求数据), headers=请求头)

        # 检查响应状态
        if 响应.status_code == 200:
            响应数据 = 响应.json()
            if 响应数据.get('success'):
                return 响应数据['data']
        return None

    except Exception:
        return None
