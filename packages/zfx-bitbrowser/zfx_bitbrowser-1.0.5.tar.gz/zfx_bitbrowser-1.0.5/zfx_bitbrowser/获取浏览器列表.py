import requests
import json


def 获取浏览器列表(page=0, pageSize=10):
    """
    获取浏览器窗口列表。

    参数:
        - page (int): 分页页码，从0开始。
        - pageSize (int): 每页数量，最大100。

    返回值:
        - list: 包含当前页浏览器窗口信息的列表。
        - None: 查询失败时返回 None。
    """
    # 默认服务地址
    服务地址 = "http://127.0.0.1:54345"

    try:
        # 构建请求数据
        请求数据 = {
            "page": page,
            "pageSize": pageSize
        }
        请求头 = {'Content-Type': 'application/json'}

        # 发送请求
        响应 = requests.post(f"{服务地址}/browser/list",
                             data=json.dumps(请求数据), headers=请求头)

        # 检查响应状态
        if 响应.status_code == 200:
            响应数据 = 响应.json()
            if 响应数据.get('success'):
                # 确保返回 data.list 的内容
                return 响应数据.get('data', {}).get('list', [])
        return None
    except Exception:
        return None