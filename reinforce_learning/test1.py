'''
o-F---
-----T

T 就是宝藏的位置, o 是探索者的位置, F是陷阱
'''
import pandas as pd
import random
import time

#########参数
epsilon = 0.8   # 贪婪度 greedy
alpha = 0.1     # 学习率
gamma = 0.8     # 奖励递减值

#####探索者的状态，即其可到达的位置，有6个len('-o---T')。所以定义
states = range(12)           # 状态集。从0到11
actions = ['up','down','left', 'right'] # 动作集。也可添加动作'none'，表示停留
rewards = [0,0,0,-1,0,0,0,0,0,0,0,1]     # 奖励集。

q_table = pd.DataFrame(data=[[0 for _ in actions] for _ in states],
                       index=states, columns=actions)

def update_env(state):
    '''更新环境，并打印'''
    global states #states设置为全局变量

    env = [[]for i in range(2)]     # 环境，就是这样一个字符串(list)！！

    for ii in range(2):
        for jj in range(6):
            env[ii].append('-')
    env[0][3] = 'F'
    env[1][5] = 'T'
    if state < 6:
        if state != states[3]  :
            env[0][state] = 'o'
    elif state < 11:
        if state != states[-1] :
            env[1][state-6] = 'o'
    else:
        pass
    # print('\r{}\n \r{}'.format(''.join(env[0]),''.join(env[1])), end='')
    print('{}\n {}\n'.format(''.join(env[0]),''.join(env[1])), end='')
    time.sleep(0.1)

###那么，在某个状态下执行某个动作之后，到达的下一个状态如何确定呢？
def get_next_state(state, action):
    '''对状态执行动作后，得到下一状态'''
    global states  #states = range(12)           # 状态集。从0到11

    if state == 0:
        if action == 'right' :
            next_state = state + 1
        elif action == 'down'  :
            next_state = state +6
    elif state < 5 and state > 0 :
        if action == 'right' and state != states[3]:
            next_state = state + 1
        elif action == 'left' and state != states[3]:
            next_state = state - 1
        elif action == 'down' and state != states[3] :
            next_state = state +6
        else:
            next_state = state
    elif state == 5:
        if action == 'left' :
            next_state = state - 1
        if action == 'down'  :
            next_state = state +6
    elif state == 6:
        if action == 'right' :
            next_state = state + 1
        elif action == 'up'  :
            next_state = state - 6
    elif state < 11 and state > 6 :
        if action == 'right' :
            next_state = state + 1
        elif action == 'left' :
            next_state = state - 1
        elif action == 'up'  :
            next_state = state - 6
    elif state == 11:
        if action == 'left' :
            next_state = state - 1
        if action == 'up'  :
            next_state = state - 6
    else:
         pass

    return next_state

def get_valid_actions(state):
    '''取当前状态下的合法动作集合，与reward无关！'''
    global actions # [''up','down',left', 'right']

    valid_actions = set(actions)

    if state < 6 :                   # 第一列
        valid_actions -= set(['up']) # 不能向上
        if  state == 0:
            valid_actions -= set(['left'])
        # if  state == 3:
        #     valid_actions -= set(['left','down','right'])
        elif  state == 5:
            valid_actions -= set(['right'])
    else :             # 第二列
        valid_actions -= set(['down']) # 不能向下
        if  state == 6:
            valid_actions -= set(['left'])
        elif  state == 11:
            valid_actions -= set(['right'])
    return list(valid_actions)

for i in range(100):
    #current_state = random.choice(states)
    current_state = 0

    update_env(current_state) # 环境相关
    total_steps = 0           # 环境相关

    while current_state != states[11] and current_state != states[3]:
        if (random.uniform(0,1) > epsilon) or ((q_table.loc[current_state] == 0).all()):  # 探索 设置epsilon是为了在一定几率上产生随机运动，而不是框死运动模式
            current_action = random.choice(get_valid_actions(current_state))
            print(current_action)
        else:
            list_current_action = get_valid_actions(current_state)
            a=[]
            for ii in list_current_action:
                a.append([ii,q_table.loc[current_state,ii]])
            a = dict(a)
            current_action = max(a,key=a.get)


        next_state = get_next_state(current_state, current_action)
        print(current_state,current_action,next_state)
        next_state_q_values = q_table.loc[next_state, get_valid_actions(next_state)]
        q_table.loc[current_state, current_action] += alpha * (rewards[next_state] + gamma * next_state_q_values.max() - q_table.loc[current_state, current_action])
        current_state = next_state
# #########参数
# epsilon = 0.9   # 贪婪度 greedy
# alpha = 0.1     # 学习率
# gamma = 0.8     # 奖励递减值
        update_env(current_state) # 环境相关
        total_steps += 1          # 环境相关
        print(q_table)
    print('Episode {}: total_steps = {}'.format(i, total_steps), end='') # 环境相关
    time.sleep(2)                                                          # 环境相关
    print('                                ', end='')                    # 环境相关

print('\nq_table:')
print(q_table)


# print(q_table.loc[:2]);   #[:4]是全闭区，并不像数组似的半开半闭
# current_action = q_table.loc[4].idxmax(axis=1 ) # 利用（贪婪）
# #print(q_table.loc[4])
# print(current_action)
'''
current_action = q_table.loc[：2].idxmax() 输出：

left     0
right    0
dtype: int64


current_action = q_table.loc[2].idxmax() 输出：left一个方向索引而已

'''