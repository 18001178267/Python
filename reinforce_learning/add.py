import pandas as pd
import random
import time
import numpy as np

#########参数
epsilon = 0.8   # 贪婪度 greedy
alpha = 0.1     # 学习率
gamma = 0.8     # 奖励递减值
def get_valid_actions(state):
    '''取当前状态下的合法动作集合，与reward无关！'''
    global actions # [''up','down',left', 'right']

    valid_actions = set(actions)

    if state < 6 :             # 第一列
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

#####探索者的状态，即其可到达的位置，有6个len('-o---T')。所以定义
states = range(12)           # 状态集。从0到11
actions = ['up','down','left', 'right'] # 动作集。也可添加动作'none'，表示停留
rewards = [0,0,0,-1,0,0,0,0,0,0,0,1]     # 奖励集。

q_table = pd.DataFrame(data=[[0 for _ in actions] for _ in states],
                       index=states, columns=actions)
q_table.loc[2,'right'] = -0.1
print(q_table)
# current_action = q_table.loc[3].idxmax(axis=1) # 利用（贪婪）

list_current_action = get_valid_actions(2)
print(list_current_action)
lens = len(list_current_action)
a=[]
for i in list_current_action:
    a.append([i,q_table.loc[2,i]])
a = dict(a)
max_value =max(a.values())
print(max_value)
max_keys = [k for k, v in a.items() if v == max_value]
print (max_keys)
#print(min(a,key=a.get))
# current_action = q_table.loc[3,list_current_action[0]]
# current_action = max (1,2,3)

# print(q_table,type(current_action),type(list_current_action))
# env = [[]for i in range(2)]     # 环境，就是这样一个字符串(list)！！
#
# for ii in range(2):
#     for jj in range(6):
#         env[ii].append('-')
# env[0][2] = 'F'
# env[1][5] = 'T'
# for iii in range (10):
#     # print('\r{}'.format(''.join(env[0])))
#     # print('\r{}'.format(''.join(env[1])), end='')
#     print('{}\n {}\n'.format(''.join(env[0]),''.join(env[1])), end='')
#
#

# valid_actions = set(actions)
#
# print(valid_actions,type(valid_actions))
# print(q_table.loc[0, ['right','left']].max())

# list=get_valid_actions(2)
# print(list)