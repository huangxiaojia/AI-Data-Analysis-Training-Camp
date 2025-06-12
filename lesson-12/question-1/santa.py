#!/usr/bin/env python
# coding: utf-8

# # 前后两天的约束
# 1）在100内, Score = 600万 <br/>
# 2) 在50内，Score = 11万 <br/>
# 3) 在25内，Score = 77570.17 <br/>
# 
# 4) 通过find_better, Score = 76863.2 <br/>

# In[1]:


import pandas as pd
import time

# 数据加载
data = pd.read_csv('./family_data.csv')
data


# ## 数据预处理
# * 1）计算Perference Cost矩阵 pcost_mat
# * 2）计算Accounting Cost矩阵 acost_mat
# * 3）计算每个家庭的人数 FAMILY_SIZE
# * 4）每个家庭的倾向选择（choice_） DESIRED

# In[2]:


# n代表家庭成员的数量， choice代表 santa满足该家庭的第几个choice (0-9)
def get_penalty(n, choice):
    penalty = 0
    if choice==0:
        return penalty
    if choice==1:
        penalty = 50
    if choice==2:
        penalty = 50 + 9*n
    if choice==3:
        penalty = 100 + 9*n
    if choice==4:
        penalty = 200 + 9*n
    if choice==5:
        penalty = 200 + 18*n
    if choice==6:
        penalty = 300 + 18*n
    if choice==7:
        penalty = 300 + 36*n
    if choice==8:
        penalty = 400 + 36*n
    if choice==9:
        penalty = 500 + (36+199)*n
    if choice>9:
        penalty = 500 + (36+398)*n
    return penalty


# In[3]:


## 设置常数
N_DAYS = 100 # 一共安排的天数
N_FAMILY = 5000 # 一共接待的家庭数量
MIN_OCCUPANCY = 125 # 最少接待人数
MAX_OCCUPANCY = 300 # 最大接待人数


# In[4]:


import numpy as np

# 计算pcost_mat，代表某个家庭，在某天接待时的penalty
pcost_mat = np.full(shape=(N_FAMILY, N_DAYS), fill_value=999999)
pcost_mat


# In[5]:


data.loc[1210]


# In[6]:


get_penalty(4, 10)


# In[7]:


#pcost_mat.shape
for f in range(N_FAMILY):
    f_num = data.loc[f, 'n_people']
    # 先按照otherwise进行初始化， 100天内 只有10个是choice，大部分都是otherwise
    pcost_mat[f, :] = get_penalty(f_num, 10)
    for choice in range(10):
        # 先找到家庭f, 在choice时的选择 => temp
        temp = data.loc[f, 'choice_'+str(choice)]
        penalty = get_penalty(f_num, choice)
        # 更新家庭f, 在temp-1天的penalty
        pcost_mat[f, temp-1] = penalty
        
pcost_mat


# In[8]:


pcost_mat


# In[9]:


# 2236对于第一个家庭，是最大的penalty, otherwise
pcost_mat.shape
#4*434+500


# In[10]:


# 计算Accounting Penalty矩阵，参数：当天人数，前一天人数
# 假设最大安排了300人
acost_mat = np.zeros(shape=(MAX_OCCUPANCY, MAX_OCCUPANCY))

for i in range(MAX_OCCUPANCY): # 当天安排的人数-1
    for j in range(MAX_OCCUPANCY): # 前一天安排的人数-1
        diff = abs(i-j)
        acost_mat[i, j] = (i+1-125) / 400 * ((i+1) ** (0.5 + diff/50))
acost_mat


# In[11]:


acost_mat.shape
# 当天接待126人，前一天接待127人的penalty
acost_mat[126-1, 127-1] #0.030912397699621216
# 当天接待126人，前一天接待300人的penalty
acost_mat[126-1, 300-1] # 572024


# In[12]:


#acost_mat[126-1, 206-1] # 445
acost_mat[250-1, 300-1] # 106066


# In[13]:


data


# In[14]:


# 每个家庭的成员数量
FAMILY_SIZE = data['n_people'].values
FAMILY_SIZE


# In[15]:


#DESIRED = data[:, :-1]
DESIRED = data.iloc[:, 1:-1].values-1
DESIRED


# ## 使用LP和MIP求解 规划方案
# * 1）先使用LP 对绝大部分家庭进行规划
# * 2）再使用MIP 对剩余家庭进行规划
# * 3）汇总两边的结果 => 最终规划方案

# ## 使用LP快速求解

# In[16]:


start = time.time()

from ortools.linear_solver import pywraplp
# 创建LP求解器
solver = pywraplp.Solver('santa', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
#solver = pywraplp.Solver.CreateSolver('CBC')

# 每一天都有哪些家庭
candidates = [[] for x in range(N_DAYS)]
# 定义决策变量
x = {}
for i in range(N_FAMILY):  # family_id
    for j in DESIRED[i, :]:  # j是该家庭，10个选项 (j的范围 1-100)
        # 第j+1天，都有哪些家庭
        candidates[j].append(i)
        # 定义决策变量 x[i, j]， i代表family_id, j代表第j+1天 参观
        x[i, j] = solver.BoolVar('x[{},{}]'.format(i, j))  # 每个家庭只有10个choice

print(x)

end = time.time()
print("代码运行时间: {:.2f}秒".format(end - start))


# In[17]:


# 统计每天接待的人数, i 代表family_id
daily_occupancy = [solver.Sum( [x[i, j] * FAMILY_SIZE[i] for i in candidates[j]])\
                            for j in range(N_DAYS)]

# 每天运载能力的约束
for j in range(N_DAYS):
    solver.Add(daily_occupancy[j]>=MIN_OCCUPANCY)
    solver.Add(daily_occupancy[j]<=MAX_OCCUPANCY)
   
# 统计每个家庭，在10个choice中出现的情况
family_presence = [solver.Sum([x[i, j] for j in DESIRED[i, :]]) \
                        for i in range(5000)]

# 约束：每个家庭在10个choice中 出现且只出现1次
for i in range(N_FAMILY):  # family_id
    solver.Add(family_presence[i]==1)

# 定义目标函数 pcost, i: family_id, j: desired
preference_cost = solver.Sum([pcost_mat[i, j] * x[i, j] for i in range(5000) for j in DESIRED[i, :]])\
# 先满足preference cost最小
solver.Minimize(preference_cost)

# 对于accounting cost进行简化约束（即前后两天的人数差 不超过25）
for j in range(100-1):
    solver.Add(daily_occupancy[j]-daily_occupancy[j+1] <= 25)
    solver.Add(daily_occupancy[j+1]-daily_occupancy[j] <= 25)

status = solver.Solve()
status


# In[18]:


#if status == pywraplp.Solver.OPTIMAL:
# x[i, j] 决策变量， 第i个family 在第j天是否参观
result = [(i, j, x[i, j].solution_value()) for i in range(5000) for j in DESIRED[i, :]
             if x[i, j].solution_value()>0]
# 得到参观日期的安排
df = pd.DataFrame(result, columns=['family_id', 'day', 'result'])
df


# In[19]:


df[df['result']<0.9]


# In[20]:


df['family_id'].value_counts()
# 设置阈值
THRESHOLD = 0.999
# 已经安排的
assigned_df = df[df['result']>THRESHOLD]
assigned_df


# In[21]:


# 没有安排的
unassigned_df = df[(df['result']<=THRESHOLD) & (df['result']>=1-THRESHOLD)]
unassigned_df


# In[23]:


# 4938个可以直接安排上，还剩余62个家庭 需要调整


# In[22]:


# 添加family_size字段
assigned_df['family_size'] = FAMILY_SIZE[assigned_df['family_id']]
assigned_df


# In[23]:


# 按照day进行聚合
occupancy = assigned_df.groupby('day')['family_size'].sum().values
occupancy


# In[24]:


min_occupancy = np.array([max(0, MIN_OCCUPANCY - x) for x in occupancy])
min_occupancy


# In[25]:


max_occupancy = np.array([MAX_OCCUPANCY - x for x in occupancy])
max_occupancy


# ## IP规划

# In[27]:


# families: 有哪些家庭需要安排，list
def solveIP(families, min_occupancy, max_occupancy):
    # 创建IP求解器
    solver = pywraplp.Solver.CreateSolver('CBC')
    # 需要安排的家庭
    n_families = len(families)

    # 每一天都有哪些家庭
    candidates = [[] for x in range(N_DAYS)]
    # 定义决策变量
    x = {}
    for i in families: # family_id
        for j in DESIRED[i, :]: # j是该家庭，10个选项 (j的范围 1-100)
            # 第j+1天，都有哪些家庭
            candidates[j].append(i)
            # 定义决策变量 x[i, j]， i代表family_id, j代表第j+1天参观
            x[i, j] = solver.BoolVar('x[{},{}]'.format(i, j)) # 每个家庭只有10个choice

    # 统计每天接待的人数, i 代表family_id
    daily_occupancy = [solver.Sum( [x[i, j] * FAMILY_SIZE[i] for i in candidates[j]])
                                for j in range(N_DAYS)]

    # 每天运载能力的约束
    for j in range(N_DAYS):
        solver.Add(daily_occupancy[j]>=min_occupancy[j])
        solver.Add(daily_occupancy[j]<=max_occupancy[j])

    # 统计每个家庭，在10个choice中出现的情况
    family_presence = [solver.Sum([x[i, j] for j in DESIRED[i, :]]) 
                            for i in families]

    # 约束：每个家庭在10个choice中 出现且只出现1次
    for i in range(n_families): # family_id
        solver.Add(family_presence[i]==1)

    # 定义目标函数 pcost
    preference_cost = solver.Sum([pcost_mat[i, j] * x[i, j] for i in families for j in DESIRED[i, :]])
    # 先满足preference cost最小
    solver.Minimize(preference_cost)

    # 对于accounting cost进行简化约束（即前后两天的人数差 不超过100）
    for j in range(100-1):
        solver.Add(daily_occupancy[j]-daily_occupancy[j+1] <= 80)
        solver.Add(daily_occupancy[j+1]-daily_occupancy[j] <= 80)

    status = solver.Solve()
    print('status=', status)
    
    # x[i, j] 决策变量， 第i个family 在第j天是否参观
    result = [(i, j, x[i, j].solution_value()) for i in families for j in DESIRED[i, :]
                 if x[i, j].solution_value()>0]
    # 得到参观日期的安排
    df = pd.DataFrame(result, columns=['family_id', 'day', 'result'])
    return df

families = unassigned_df['family_id'].unique()
result = solveIP(families, min_occupancy, max_occupancy)
result


# In[28]:


res = pd.concat((assigned_df[['family_id', 'day', 'result']], result))
res = res.sort_values(by=['family_id'], ascending=True)[['family_id', 'day']]
res['day'] = res['day'] + 1
res.columns = ['family_id', 'assigned_day']
res.to_csv('./baseline_santa2-1.csv', index=False)
res


# In[29]:


#assigned_df['family_id'].nunique()
assigned_df[assigned_df['result']>0.5]


# * 1) 先把完整的cost计算出来 => 完整的结果评估： metric(pcost + acost)
# * 2) 对于每个family_id，查看choice是否可以切换为其他的choice => 采用新的结果评估 计算，是否小于 当前最优解
# 不断循环2）直至无法更新score

# ## 结果评估

# In[30]:


prediction = res.assigned_day.values
prediction


# In[32]:


"""
prediction[0] = 52
prediction
"""


# In[33]:


"""
prediction = pred2
prediction
"""


# In[34]:


pred2 = prediction.copy()


# In[31]:


from numba import njit
# Python 解释性的编辑器，
# Python C++ 谁的运行速度快？ => C/C++速度更快
# Python具有C++的速度

@njit(fastmath=True)
def pcost(prediction):
    penalty = 0
    daily_occupancy = np.zeros(N_DAYS)
    # 统计总的pcost，以及daily_occupancy
    for (i, p) in enumerate(prediction):
        #print(i, p)
        # 得到家庭的人数
        num = FAMILY_SIZE[i]
        # 第i个家庭，p天访问时的pcost
        penalty += pcost_mat[i, p-1]
        # 计算p天的人数
        daily_occupancy[p-1] += num
    #print('penalty:{}, daily_occupancy:{}'.format(penalty, daily_occupancy))
    return penalty, daily_occupancy

@njit(fastmath=True)
def acost(daily_occupancy):
    accounting_cost = 0
    #daily_occupancy.append(daily_occupancy[99])
    #print(daily_occupancy)
    # 判断是否在 MIN_OCCUPANCY和MAX_OCCUPANCY之间
    check = False # 是否在范围外面
    
    for day in range(N_DAYS): # 1-100
        if day+1==100:
            n1 = int(daily_occupancy[day])
        else:
            # 得到前一天的人数
            n1 = int(daily_occupancy[day+1])
        # 得到当天的人数
        n = int(daily_occupancy[day])   
        if (n > MAX_OCCUPANCY) or (n < MIN_OCCUPANCY) or (n1 > MAX_OCCUPANCY) or (n1 < MIN_OCCUPANCY):
            check = True
            break
        #print(n1, n)
        accounting_cost += acost_mat[n1-1, n-1]
    return accounting_cost, check

@njit(fastmath=True)
def cost_function(prediction):
    # 先统计 pcost，以及daily_occupancy
    penalty, daily_occupancy = pcost(prediction)
    accounting_cost, check = acost(daily_occupancy)
    #print(penalty)
    if check:
        return 999999
    else:
        return penalty + accounting_cost
cost_function(prediction)


# In[32]:


# 替换方法，更换family_id的choice，查找更好的score
def find_better(pred):
    # 得到原始的score
    score = cost_function(pred)
    ori_score = np.inf # 设置为无穷大
    
    # 如果找不到更新，则退出
    while score < ori_score:
        ori_score = score
        
        for family_id in range(5000):
            for pick in range(10):
                # 得到family_id在choice pick的日期
                day = DESIRED[family_id, pick]
                # 记录原来的选择
                oldvalue = pred[family_id]
                # 给family_id 更换选择
                pred[family_id] = day
                # 重新计算分数
                new_score = cost_function(pred) # choice5 =>choice6 不仅影响到 pcost，还会影响到acost
                # 如果比原来分数小，那么更新choice是成功的
                if new_score < score:
                    score = new_score
                else: # 设置为原来的oldvalue
                    pred[family_id] = oldvalue
        print('score=', score)
    return pred
    #print(score)
    
prediction = find_better(prediction)


# In[33]:


DESIRED


# In[34]:


# for i in prediction:
#     print(i)


# In[43]:


DESIRED[1210]


# In[35]:


#prediction
res['assigned_day'] = prediction
res.to_csv('./baseline_santa2-2.csv', index=False)
res

