# -*- coding: utf-8 -*-
# @Time : 2022/12/11 13:52
# @Author : hhq
# @File : production_planning.py
# 案例一的代码
# -*- coding: utf-8 -*-
"""
@author: help@gurobi.cn
"""

import gurobipy as gp
from gurobipy import *

###############################   输入   ###################################

# 产品
PRODUCTS = ['A1', 'A2', 'B1', 'B2']

# 产线
LINES = ['L1', 'L2']

# 上一次生产中最后的产品
LAST_PRODUCTION = {
    'L1': 'A1',
    'L2': 'A2',
}

# 产品需求
DEMAND = {
    'A1': 14,
    'A2': 10,
    'B1': 12,
    'B2': 12,
}

# 切换成本
CHANGEOVER_COST = {
    ('A1', 'A1'): 0,
    ('A1', 'A2'): 1,
    ('A1', 'B1'): 4,
    ('A1', 'B2'): 4,
    ('A2', 'A1'): 1,
    ('A2', 'A2'): 0,
    ('A2', 'B1'): 4,
    ('A2', 'B2'): 4,
    ('B1', 'A1'): 4,
    ('B1', 'A2'): 4,
    ('B1', 'B1'): 0,
    ('B1', 'B2'): 1,
    ('B2', 'A1'): 4,
    ('B2', 'A2'): 4,
    ('B2', 'B1'): 1,
    ('B2', 'B2'): 0
}

# 产线产能
LINE_CAPACITY = 24

# 时段数量
SLOTS = range(len(PRODUCTS))

###############################   模型   ###################################

# 创建模型
model = gp.Model('production_scheduling_with_changeover')

# 变量：每个产线每个产品在每个时段的加工数量
quantity = model.addVars(LINES, SLOTS, PRODUCTS, vtype=GRB.INTEGER, name="qty")

# 变量：根据加工数量来判断每个产线的每个产品的每个时段是否被占用
isBusy = model.addVars(LINES, SLOTS, PRODUCTS, vtype=GRB.BINARY, name="isBusy")

# 变量：每个产线每个时段是否被任何一个产品占用
slotBusy = model.addVars(LINES, SLOTS, vtype=GRB.BINARY, name="slotBusy")

# 变量：每个产线每个时段从上时段产品到本时段产品的切换
changeOver = model.addVars(LINES, SLOTS, PRODUCTS, PRODUCTS, vtype=GRB.BINARY, name="changeOver")

# 1. 满足需求
for product in PRODUCTS:
    model.addConstr(((sum(quantity[line, n, product] for line in LINES for n in SLOTS)) == DEMAND[product]),
                    name='meet_demand' + '_' + product)

# 2. 不超过产能
for line in LINES:
    model.addConstr(((sum(quantity[line, n, product] for product in PRODUCTS for n in SLOTS)) <= LINE_CAPACITY),
                    name='line_capacity' + '_' + line)

# 3. 建立 isBusy 和 quantity 之间的标志关系
for line in LINES:
    for product in PRODUCTS:
        for n in SLOTS:
            model.addGenConstrIndicator(isBusy[line, n, product], 0, quantity[line, n, product] == 0)
            model.addGenConstrIndicator(isBusy[line, n, product], 1, quantity[line, n, product] >= 1)

# 4. 每个产线的每个时段只能允许最多一个产品
for line in LINES:
    for n in SLOTS:
        model.addConstr((sum(isBusy[line, n, product] for product in PRODUCTS) <= 1),
                        name='One_Product_Per_Slot' + '_' + line + '_' + str(n))

# 5. 每个产线上每个产品只能出现在最多一个时段里
for line in LINES:
    for product in PRODUCTS:
        model.addConstr((sum(isBusy[line, n, product] for n in SLOTS) <= 1),
                        name='One_Product_Per_line' + '_' + line + '_' + product)

# 6. 统计每个时段被占用情况，不允许出现前面时段没有生产，后面时段有生产的情况
for line in LINES:
    for n in SLOTS:
        model.addConstr(slotBusy[line, n] == max_([isBusy[line, n, product] for product in PRODUCTS]),
                        name='slotbusy' + '_' + line + '_' + str(n))

for line in LINES:
    for n in SLOTS[1:]:
        model.addConstr(slotBusy[line, n - 1] >= slotBusy[line, n], name='slotbusyincrease' + '_' + line + '_' + str(n))

# 7. 统计每个时段的切换情况
for line in LINES:
    for product in PRODUCTS:
        if product == LAST_PRODUCTION[line]:
            model.addConstr(changeOver[line, 0, LAST_PRODUCTION[line], product] == 0,
                            name='changeover' + '_' + line + '_' + LAST_PRODUCTION[line] + '_' + product)
        else:
            model.addConstr(changeOver[line, 0, LAST_PRODUCTION[line], product] == isBusy[line, 0, product],
                            name='changeover' + '_' + line + '_' + LAST_PRODUCTION[line] + '_' + product)

for line in LINES:
    for n in SLOTS[1:]:
        for p1 in PRODUCTS:
            for p2 in PRODUCTS:
                if p1 == p2:
                    model.addConstr(changeOver[line, n, p1, p2] == 0,
                                    name='changeover' + '_' + line + '_' + p1 + '_' + p2)
                else:
                    model.addConstr(changeOver[line, n, p1, p2] == and_([isBusy[line, n - 1, p1], isBusy[line, n, p2]]),
                                    name='changeover' + '_' + line + '_' + p1 + '_' + p2)

# 目标
obj = sum(
    changeOver[line, n, p1, p2] * CHANGEOVER_COST[p1, p2] for p1 in PRODUCTS for p2 in PRODUCTS for line in LINES for n
    in SLOTS)

# 最小化切换成本
model.setObjective(obj, GRB.MINIMIZE)

# 输出到 LP 文件
model.write("changeover.lp")

# 优化
model.optimize()

print('\n\n###############################   输出结果   ######################################\n')
print('总切换成本：' + '%3d' % model.objval)
print('生产计划：')
tableStr = ''
for n in SLOTS:
    tableStr = tableStr + '%18s' % n
print(tableStr)

for line in LINES:
    tableStr1 = line + '%3s' % LAST_PRODUCTION[line] + '    '
    tableStr2 = '         '
    for n in SLOTS:
        for p in PRODUCTS:
            tableStr1 = tableStr1 + '%3s' % p + ' '
            tableStr2 = tableStr2 + '%3d' % quantity[line, n, p].x + ' '
        tableStr1 = tableStr1 + ' | '
        tableStr2 = tableStr2 + ' | '
    print(tableStr1)
    print(tableStr2)

print('切换成本：')
for line in LINES:
    for n in SLOTS:
        for p1 in PRODUCTS:
            for p2 in PRODUCTS:
                if round(changeOver[line, n, p1, p2].x) == 1:
                    print(line + ' ' + p1 + ' ' + p2 + ' ' + str(CHANGEOVER_COST[p1, p2]))


