import operator
import random


def main(r: int, discount: float):
    moves = ['U', 'R', 'D', 'L']
    rewards = init_rewards(r)
    iterations, v = policy_iteration(rewards, moves, discount)
    vals, pols = get_val_pol_mat(v)
    print(iterations, 'iterations')
    print('Values:')
    print(vals)
    print('======================================================')
    print('Policies:')
    print(pols)


def value_iteration(r: dict, moves: list, discount: float) -> [int, dict]:
    old = ''
    cur = ''
    iterations = 1
    old_v = init_mem(moves)
    new_v = init_mem(moves)

    for i in range(4 * 9):
        old += '0.0'

    while True:
        for i in range(3):
            for j in range(3):
                for m in old_v[i][j].keys():
                    new_v[i][j][m] = calc_q(i, j, m, r, old_v, moves, discount)
                cur += str(get_value(new_v, i, j))
        iterations += 1
        if cur == old:
            return iterations, new_v
        else:
            old = cur
            cur = ''
            old_v = new_v
            new_v = init_mem(moves)


def policy_iteration(r: dict, moves: list, discount: float) -> [int, dict]:
    old = ''
    cur = ''
    iterations = 1
    old_v = init_mem(moves)
    new_v = init_mem(moves)

    for i in range(9):
        old += moves[random.randint(0, 3)]

    while True:
        for i in range(len(old)):
            old_v[i // 3][i % 3][old[i]] = calc_q(i // 3, i % 3, old[i], r, old_v, moves, discount)
        for i in range(3):
            for j in range(3):
                for m in old_v[i][j].keys():
                    new_v[i][j][m] = calc_q(i, j, m, r, old_v, moves, discount)
                cur += get_policy(new_v, i, j)
        iterations += 1
        if cur == old:
            return iterations, new_v
        else:
            old = cur
            cur = ''
            old_v = new_v
            new_v = init_mem(moves)


def calc_q(i: int, j: int, action: str, reward: dict, old_v: dict, moves: list, discount: float) -> float:
    tot = 0.0
    for move in moves:
        p = get_probability(i, j, action, move)
        nxt = get_next(i, j, move)
        r = get_reward(reward, nxt[0], nxt[1])
        v = get_value(old_v, nxt[0], nxt[1])
        tot += p * (r + (discount * v))
    return round(tot, 3)


def get_val_pol_mat(values) -> (list, list):
    vals = []
    pols = []
    for i in range(3):
        v_row = []
        p_row = []
        for j in range(3):
            k, v = max(values[i][j].items(), key=operator.itemgetter(1))
            v_row.append(v)
            p_row.append(k if v != 0.0 else '-')
        vals.append(v_row)
        pols.append(p_row)
    return vals, pols


def get_next(i: int, j: int, move: str) -> [int, int]:
    if move == 'U':
        return i - 1, j
    if move == 'R':
        return i, j + 1
    if move == 'D':
        return i + 1, j
    else:
        return i, j - 1


def get_probability(i: int, j: int, choice: str, direction: str) -> float:
    if (i == 0 and j == 0) or (i == 0 and j == 2):
        return 0.0
    if choice == direction:
        return 0.8
    if (choice == 'U' and direction == 'D') or (choice == 'R' and direction == 'L') or \
            (choice == 'D' and direction == 'U') or (choice == 'L' and direction == 'R'):
        return 0.0
    return 0.1


def get_value(v: dict, i: int, j: int) -> int:
    if -1 < i < 3 and -1 < j < 3:
        return max(v[i][j].values())
    return 0


def get_policy(v: dict, i: int, j: int) -> str:
    if -1 < i < 3 and -1 < j < 3:
        return max(v[i][j].items(), key=operator.itemgetter(1))[0]
    return 'None'


def get_reward(r: dict, i: int, j: int) -> int:
    if -1 < i < 3 and -1 < j < 3:
        return r[i][j]
    return 0


def init_rewards(r: int) -> dict:
    rew = {}
    for i in range(3):
        rew[i] = {}
        for j in range(3):
            rew[i][j] = -1
    rew[0][0] = r
    rew[0][2] = 10
    return rew


def init_mem(moves: list) -> dict:
    dp = {}
    for i in range(3):
        dp[i] = {}
        for j in range(3):
            dp[i][j] = {}
            for m in moves:
                dp[i][j][m] = 0
    return dp


if __name__ == '__main__':
    main(3, 0.99)
