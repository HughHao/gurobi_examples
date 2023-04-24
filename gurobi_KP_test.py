# -*- coding: utf-8 -*-
# @Time : 2023/4/18 17:29
# @Author : hhq
# @File : gurobi_KP_test.py
import gurobipy as gp

# 定义物品的重量
weights = [[10, 20, 30], [15, 20, 18]]

# 定义背包的容量
capacity = [50, 10]

values = [60, 100, 120]
# 创建模型
model = gp.Model("knapsack")

# 创建变量x，表示是否选择该物品
x = model.addVars(len(weights[0]), vtype=gp.GRB.BINARY, name="x")

# 创建目标函数，即最大化价值
model.setObjective(x.prod(values), gp.GRB.MAXIMIZE)

# 添加约束条件，即背包容量不能超过capacity
for i in range(len(weights)):
    model.addConstr(x.prod(weights[i]) <= capacity[i], name="c")

# 求解模型
model.optimize()
a = 1
# 打印结果
if model.status == gp.GRB.OPTIMAL:
    print("最大价值为：", model.objVal)
    print("选择的物品为：")
    for i in range(len(weights[0])):
        if x[i].x > 0.5:  # .x表示变量的值.x[i]表示第i个变量的值，是一个变量
            # 在进行线性规划求解时，Gurobi 会计算得到每个变量，然后将这些解值保存在相应变量的 .x 属性中。
            print("物品", i+1)
            a *= 0
if a == 1:
    print("无解")
