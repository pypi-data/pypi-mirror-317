import requests
import json


def 删除浏览器(浏览器ID):
    """
    删除指定的比特浏览器窗口。

    参数:
        - 浏览器ID (str): 要删除的浏览器窗口ID。

    返回值:
        - bool: 删除成功返回 True，删除失败返回 False。

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

        # 发送删除请求
        响应 = requests.post(f"{服务地址}/browser/delete",
                             data=json.dumps(请求数据), headers=请求头)

        # 检查响应状态
        if 响应.status_code == 200:
            响应数据 = 响应.json()
            if 响应数据.get('success'):
                return True
        return False

    except Exception:
        return False