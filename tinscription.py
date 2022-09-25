import random
from collections import Counter


black = ['R','I','I','M','M','M']
green = ['RR', 'RR', 'R', 'R', 'R', 'R']
blue = ['II', 'II', 'I', 'I', 'I', 'I']
red = ['MM', 'MM', 'M', 'M', 'M', 'M']

s1_b = ['II', 'MMM']
s1_bl = ['MIR']
s2_4_bl = ['R', 'II', 'MMM']
s2_4_b = ['Council', 'War', 'Production']
s5_b = ['Special', 'War']
s5_bl = ['II', 'MMM']

nav_goal = 6
ind_goal = 6
mec_goal = 5
exp_goal = 6
war_goal = 7

stg_q = {
    2:[1,2,3,4,5,6,7],
    3:[2,3,4,5,7],
    4:[2,4,5,7,9],
    5:[4,6,8,10]
}

vot_q = {
    2:[0,1,2,2,3,4,5],
    3:[1,2,3,4,5],
    4:[3,4,5,6,8]
}

vot_die = [0,0,0,1,1,2]


def roll():
    bl1 = random.choice(black)
    bl2 = random.choice(black)
    bl3 = random.choice(black)
    bl = Counter(bl1 + bl2 + bl3)
    g = random.choice(green)
    b = random.choice(blue)
    r = random.choice(red)
    f = Counter(g + b + r)

    # print(f'Black 1: {bl1}')
    # print(f'Black 2: {bl2}')
    # print(f'Black 3: {bl3}')
    # print(f'Green: {g}')
    # print(f'Blue: {b}')
    # print(f'Red: {r}')
    # print('')
    print(f"Basic: {bl['M']}M {bl['I']}I {bl['R']}R")
    print(f"Focus: {f['M']}M {f['I']}I {f['R']}R")
    return f


def build_stage(b_in, bl_in):
    deck = []
    b = b_in.copy()
    bl = bl_in.copy()
    c = len(b + bl)
    random.shuffle(b)
    random.shuffle(bl)
    for i in range(c):
        if i % 2 == 0:
            deck.append(b.pop())
        else:
            deck.append(bl.pop())
    return deck[::-1]


if __name__ == '__main__':
    stage = 1
    round = 1
    stage_round = 1
    nav = 0
    ind = 0
    mec = 0
    war = 0
    exp = 0
    stg = {}
    vot = {}
    stg[2] = stg_q[2].pop(0)
    stg[3] = stg_q[3].pop(0)
    stg[4] = stg_q[4].pop(0)
    stg[5] = stg_q[5].pop(0)
    vot[2] = vot_q[2].pop(0)
    vot[3] = vot_q[3].pop(0)
    vot[4] = vot_q[4].pop(0)
    stg_st = 2
    vot_st = 2

    s1 = build_stage(s1_b, s1_bl)
    s2 = build_stage(s2_4_b, s2_4_bl)
    s3 = build_stage(s2_4_b, s2_4_bl)
    s4 = build_stage(s2_4_b, s2_4_bl)
    s5 = build_stage(s5_b, s5_bl)
    deck = s1 + s2 + s3 + s4 + s5
    round_type = 'Strategy'
    while True:
        round_type = deck.pop(0)
        if round_type not in ['War', 'Special', 'Council', 'Production']:
            res = Counter(round_type)
            round_type = 'Strategy'
        print(f'-----Stage {stage} Round {stage_round} ({round}): {round_type}-----')
        if round_type == 'Strategy':
            print(f"Strategy Resources: {res['M']}M {res['I']}I {res['R']}R")
            input('')
            f = roll()
            if f['M'] == 2:
                if nav >= 8:
                    for i in range(2,6):
                        if len(stg_q[i]) > 0:
                            stg[i] = stg_q[i].pop(0)
                            break
                if nav < 8:
                    nav += 1
            if f['M'] == 1:
                for i in range(2,6):
                    if len(stg_q[i]) > 0:
                        stg[i] = stg_q[i].pop(0)
                        break

            if f['I'] == 2:
                if ind >= 8:
                    for i in range(2,5):
                        if len(vot_q[i]) > 0:
                            vot[i] = vot_q[i].pop(0)
                            break
                if ind < 8:
                    ind += 1
            if f['I'] == 1:
                for i in range(2,5):
                    if len(vot_q[i]) > 0:
                        vot[i] = vot_q[i].pop(0)
                        break

            if f['R'] == 2:
                if exp >= 8 and war < 7:
                    mec += 1
                    war += 1
                if exp < 8:
                    exp += 1
            if f['R'] == 1:
                if war >= 7 and exp < 8:
                    exp += 1
                if war < 7:
                    mec += 1
                    war += 1

            if vot_st == 5:
                print(f'AI Values: Str {stg[stg_st]}')
            else:
                print(f'AI Values: Str {stg[stg_st]} Vot {vot[vot_st]}-{vot[vot_st] + 2}')
            print(f'AI Goals: Mec ({mec}/{mec_goal}) Nav ({nav}/{nav_goal}) Exp ({exp}/{exp_goal}) Ind ({ind}/{ind_goal}) War ({war}/{war_goal})')
        if round_type == 'War':
            print(f'AI Strength: {stg[stage]}')
            stg_q[stg_st] = []
            stg_st += 1
        if round_type == 'Council':
            print(f'AI Potential Votes: {vot[stage]}-{vot[stage] + 2}')
            input('')
            print(f'AI Actual Votes: {vot[stage] + random.choice(vot_die)}')
            vot_q[vot_st] = []
            vot_st += 1
        round += 1
        stage_round += 1
        if round in [4, 10, 16, 22]:
            stage += 1
            stage_round = 1
        input('')
        if round_type == 'War' and stage == 5:
            print('GAME OVER')
            break