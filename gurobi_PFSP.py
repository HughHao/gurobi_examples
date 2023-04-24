# -*- coding: utf-8 -*-
# @Time : 2023/4/23 17:23
# @Author : hhq
# @File : gurobi_PFSP.py
from gurobipy import *

# 工件数、机器数、车间数、时间段数
n = 3
m = 3
L = 2
T = [[10, 8, 6], [8, 6, 4]]  # 

# 工件的加工时间
p = [[2, 3, 1], [1, 2, 3], [3, 1, 2]]

# 创建模型
model = Model()

# 创建决策变量
x = {}
y = {}
for i in range(n):
    for j in range(m):
        for k in range(T[0][j]):
            for l in range(L):
                x[i, j, k, l] = model.addVar(vtype=GRB.BINARY, name='x[%d,%d,%d,%d]' % (i, j, k, l))
                y[i, j, k, l] = model.addVar(vtype=GRB.BINARY, name='y[%d,%d,%d,%d]' % (i, j, k, l))

# 创建目标函数
C = [0] * n
for i in range(n):
    for j in range(m):
        for k in range(T[0][j]):
            for l in range(L):
                C[i] = max(C[i], (k + p[i][j]) * y[i, j, k, l])
model.setObjective(sum(C), GRB.MINIMIZE)

# 创建约束条件
for i in range(n):
    model.addConstr(sum(x[i, j, k, l] for j in range(m) for k in range(T[0][j]) for l in range(L)) == 1)
for j in range(m):
    for k in range(T[0][j]):
        for l in range(L):
            model.addConstr(sum(x[i, j, k, l] for i in range(n)) <= 1)
            model.addConstr(sum(x[i, j, k, l] * p[i][j] for i in range(n)) <= T[l][j])
for i in range(n):
    for j in range(m):
        for k in range(T[0][j]):
            for l in range(L):
                model.addConstr(y[i, j, k, l] <= x[i, j, k, l])
                model.addConstr(y[i, j, k, l] >= x[i, j, k, l] - sum(x[i, j, t, l] for t in range(k+1, T[0][j])))
                model.addConstr(y[i, j, k, l] >= sum(x[i, j, t, l] for t in range(k+1)))

for i in range(n):
    for j in range(1, m):
        for k in range(T[0][j]):
            for l in range(L):
                model.addConstr(sum(k * y[i, j, k, l] for k in range(T[0][j])) == C[i] - p[i][j])
                model.addConstr(sum(k * y[i, j, k, l] for k in range(T[0][j])) == sum((k + p[i][j-1]) * y[i, j-1, k, l] for k in range(T[0][j-1])))

# 求解模型
model.optimize()

# 输出结果
print('最小完成时间：', model.objVal)
for i in range(n):
    for j in range(m):
        for k in range(T[0][j]):
            for l in range(L):
                if x[i, j, k, l].x > 0.5:
                    print('工件 %d 在机器 %d 上在时间段 %d 在车间 %d 开始加工，完成时间为 %d' % (i, j, k, l, int(C[i])))
