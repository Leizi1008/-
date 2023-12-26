# main.py
from src.data_analysis import load_data, analyze_data
from src.monte_carlo_simulation import monte_carlo_simulation, generate_bet

def main(file_path, N):
    """
    主函数，执行数据加载、分析和蒙特卡洛模拟
    参数:
    file_path: 数据文件路径
    N: 蒙特卡洛模拟次数
    """
    # 加载数据
    try:
        data = load_data(file_path)
    except FileNotFoundError:
        print(f"无法找到文件：{file_path}")
        return

    # 数据分析
    analyze_data(data)

    # 蒙特卡洛模拟
    winning_numbers = generate_bet()  # 生成中奖号码
    probability = monte_carlo_simulation(N, winning_numbers)
    print(f"中奖概率：{probability}")

if __name__ == "__main__":
    main('data/history_data.csv', 1000000)