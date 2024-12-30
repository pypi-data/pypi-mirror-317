import json
from jsonpath_ng import parse


def json_精准_键_删除(数据对象, 父路径, 目标键):
    """
    在指定的父路径下删除 JSON 对象中的指定键。

    参数:
        数据对象 (dict 或 str): Python 字典对象或 JSON 字符串。
        父路径 (str): 要查找的父路径(部分或全部，不确定部分也可以用 * 代替)，例如 '*.address.[0].details'。
        目标键 (str): 要删除的键。

    返回:
        dict: 删除后的 JSON 数据对象。
    """
    try:
        if isinstance(数据对象, str):
            数据对象 = json.loads(数据对象)

        jsonpath_expr = parse(f'$.{父路径}..{目标键}')
        matches = jsonpath_expr.find(数据对象)

        for match in matches:
            parent = match.context.value
            if isinstance(parent, dict):
                del parent[目标键]

        return 数据对象
    except Exception as e:
        return {}