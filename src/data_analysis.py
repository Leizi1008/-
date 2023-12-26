# src/data_analysis.py
import pandas as pd
import numpy as np
from collections import Counter

def load_data(file_path):
    # 加载数据
    try:
        data = pd.read_csv(file_path, sep='\t', encoding='gbk')
    except FileNotFoundError:
        print(f"无法找到文件：{file_path}")
        return None
    return data

def calculate_sum(data):
    # 计算红球和蓝球的和值
    red_sum = data.loc[:, '红球1':'红球6'].sum(axis=1)
    blue_sum = data['蓝球']
    return red_sum, blue_sum

def calculate_span(data):
    # 计算红球的跨度
    red_max = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].max(axis=1)
    red_min = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].min(axis=1)
    return red_max - red_min

def calculate_ac(data):
    # 计算AC值
    ac_values = []
    for index, row in data.iterrows():
        numbers = sorted(row[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']])
        diff = np.diff(numbers)
        ac = max(0, len(set(diff)) - 5)  # 避免AC值为负数
        ac_values.append(ac)
    return ac_values

def calculate_zone_ratio(data):
    # 计算区间比
    zone1 = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].apply(lambda x: (x >= 1) & (x <= 11)).sum(axis=1)
    zone2 = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].apply(lambda x: (x >= 12) & (x <= 22)).sum(axis=1)
    zone3 = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].apply(lambda x: (x >= 23) & (x <= 33)).sum(axis=1)
    return zone1, zone2, zone3

def calculate_odd_even_ratio(data):
    # 计算奇偶比
    odd = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].apply(lambda x: x % 2 != 0).sum(axis=1)
    even = 6 - odd
    return odd / even

def calculate_cold_hot_ratio(data):
    # 计算冷热比
    all_numbers = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].values.flatten()
    counter = Counter(all_numbers)
    hot_numbers = [number for number, count in counter.items() if count > np.median(list(counter.values()))]
    cold_numbers = [number for number, count in counter.items() if count <= np.median(list(counter.values()))]
    return len(hot_numbers) / len(cold_numbers) if len(cold_numbers) > 0 else 0  # 避免除以零的错误

def calculate_repeat_number(data):
    # 计算重号
    repeat_number = (data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].shift() == data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']]).sum(axis=1)
    return repeat_number

def calculate_consecutive_number(data):
    # 计算连号
    sorted_data = data[['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']].apply(sorted, axis=1, result_type='broadcast')
    consecutive_number = (sorted_data.diff(axis=1) == 1).sum(axis=1)
    return consecutive_number

def analyze_data(data):
    # 数据分析
    if data is None:
        print("数据加载失败，无法进行分析")
        return None

    red_sum, blue_sum = calculate_sum(data)
    red_span = calculate_span(data)
    ac_values = calculate_ac(data)
    zone1, zone2, zone3 = calculate_zone_ratio(data)
    odd_even_ratio = calculate_odd_even_ratio(data)
    cold_hot_ratio = calculate_cold_hot_ratio(data)
    repeat_number = calculate_repeat_number(data)
    consecutive_number = calculate_consecutive_number(data)

    # 将所有的结果组合成一个字典并返回
    result = {
        'red_sum': red_sum,
        'blue_sum': blue_sum,
        'red_span': red_span,
        'ac_values': ac_values,
        'zone_ratios': (zone1, zone2, zone3),
        'odd_even_ratio': odd_even_ratio,
        'cold_hot_ratio': cold_hot_ratio,
        'repeat_number': repeat_number,
        'consecutive_number': consecutive_number
    }

    return result