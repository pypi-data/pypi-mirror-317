import requests
import json


def 删除所有浏览器():
    """
    删除所有浏览器窗口。

    返回值:
        - int: 删除的浏览器总数。
    """
    # 默认服务地址
    服务地址 = "http://127.0.0.1:54345"
    删除数量 = 0
    当前页 = 0
    每页数量 = 10

    try:
        while True:
            # 获取当前页的浏览器列表
            请求数据 = {"page": 当前页, "pageSize": 每页数量}
            请求头 = {'Content-Type': 'application/json'}
            响应 = requests.post(f"{服务地址}/browser/list",
                               data=json.dumps(请求数据), headers=请求头)

            if 响应.status_code != 200:
                break

            响应数据 = 响应.json()
            if not 响应数据.get('success'):
                break

            浏览器列表 = 响应数据.get('data', {}).get('list', [])
            if not 浏览器列表:
                break

            # 遍历删除每个浏览器
            for 浏览器 in 浏览器列表:
                浏览器ID = 浏览器.get('id')
                if not 浏览器ID:
                    continue

                删除请求数据 = {"id": 浏览器ID}
                删除响应 = requests.post(f"{服务地址}/browser/delete",
                                     data=json.dumps(删除请求数据), headers=请求头)
                if 删除响应.status_code == 200 and 删除响应.json().get('success'):
                    删除数量 += 1

            # 检查是否还有下一页
            if len(浏览器列表) < 每页数量:
                break
            当前页 += 1

    except Exception:
        pass

    return 删除数量