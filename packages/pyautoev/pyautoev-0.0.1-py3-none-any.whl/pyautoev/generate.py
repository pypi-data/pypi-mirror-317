# -*- coding: utf-8 -*-
def generate_sequence(r, n):
    """
        r: Str
        n: sequence num
        eg: generate_sequence('XXX001', 2)
            out: ['XXX001', 'XXX002']
    """
    if n == 1:
        return [r]
    # 提取前缀（不包含最后两个字符的其余部分）
    prefix = r[:-2]
    # 提取最后两位数字并转换为整数
    last_two_digits = int(r[-2:])
    # 生成范围内的序列列表
    sequence = [f"{prefix}{str(i).zfill(2)}" for i in range(last_two_digits, n+1)]
    # 生成最终的字符串，格式为 '开始-结束'
    # return f"{r}-{sequence[-1]}"
    return sequence


def sql_column_get(column):
    column_list = column.split('.')
    if len(column_list) == 1:
        return column_list[0]
    else:
        return column_list[1]