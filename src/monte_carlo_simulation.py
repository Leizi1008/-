# src/monte_carlo_simulation.py
import random

def generate_bet():
    # 生成一注随机的双色球投注
    red_balls = random.sample(range(1, 34), 6)
    blue_ball = random.randint(1, 16)
    return red_balls, blue_ball

def is_winning_bet(bet, winning_numbers):
    # 判断一注投注是否中奖
    red_balls, blue_ball = bet
    winning_red_balls, winning_blue_ball = winning_numbers
    return set(red_balls) == set(winning_red_balls) and blue_ball == winning_blue_ball

def monte_carlo_simulation(N, winning_numbers):
    # 蒙特卡洛模拟
    winning_count = 0  # 中奖次数
    for _ in range(N):
        bet = generate_bet()
        if is_winning_bet(bet, winning_numbers):
            winning_count += 1
    return winning_count / N