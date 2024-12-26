import datetime

def format_date_in_dict(input_dict):
    """
    递归遍历字典，将字典中值为datetime类型的日期属性格式化为字符串。

    参数:
    input_dict (dict): 需要处理的字典

    返回:
    dict: 处理后的字典，其中日期属性已格式化为字符串
    """
    for key, value in input_dict.items():
        if isinstance(value, dict):
            # 如果值是字典，则递归调用本函数继续处理
            input_dict[key] = format_date_in_dict(value)
        elif isinstance(value, datetime.date):
            # 如果值是datetime类型，将其格式化为字符串
            input_dict[key] = value.strftime('%Y-%m-%d')
        elif isinstance(value, datetime.datetime):
            # 如果值是datetime类型，将其格式化为字符串
            input_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    return input_dict