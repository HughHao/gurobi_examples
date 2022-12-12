# -*- coding: utf-8 -*-
"""
Make-To-Order 订单装配 APS

@author: help@gurobi.cn

"""

import gurobipy as gp
from gurobipy import *

 

###############################   输入   ###################################

# 订单
ORDERS = ['O1','O2','O3','O4']

# 工序
STEPS = [1,2,3]

# 设备
RESOURCES = ['R1','R2']

# 模具
MOULDS = ['M1','M2']

# 加工时间,假设为整数
STEP_TIME= {
    ('O1',1): 10,
    ('O1',2): 20,
    ('O1',3): 30,
    ('O2',1): 40,
    ('O2',2): 30,
    ('O2',3): 20,
    ('O3',1): 20,
    ('O3',2): 20,
    ('O3',3): 30,
    ('O4',1): 40,
    ('O4',2): 40,
    ('O4',3): 30,
    }

# 可选设备： 1 为可选， 0 为不可选
STEP_RESOURCES= {
    ('O1',1,'R1'): 1,
    ('O1',1,'R2'): 1,
    ('O1',2,'R1'): 1,
    ('O1',2,'R2'): 0,
    ('O1',3,'R1'): 0,
    ('O1',3,'R2'): 1,
    ('O2',1,'R1'): 1,
    ('O2',1,'R2'): 0,
    ('O2',2,'R1'): 1,
    ('O2',2,'R2'): 0,
    ('O2',3,'R1'): 0,
    ('O2',3,'R2'): 1,
    ('O3',1,'R1'): 0,
    ('O3',1,'R2'): 1,
    ('O3',2,'R1'): 0,
    ('O3',2,'R2'): 1,
    ('O3',3,'R1'): 1,
    ('O3',3,'R2'): 0,
    ('O4',1,'R1'): 1,
    ('O4',1,'R2'): 1,
    ('O4',2,'R1'): 0,
    ('O4',2,'R2'): 1,
    ('O4',3,'R1'): 0,
    ('O4',3,'R2'): 1,

    }

# 可选模具： 1 为可选，0为不可选
STEP_MOULDS = {
    ('O1',1,'M1'): 1,
    ('O1',1,'M2'): 0,
    ('O1',2,'M1'): 1,
    ('O1',2,'M2'): 0,
    ('O1',3,'M1'): 1,
    ('O1',3,'M2'): 0,
    ('O2',1,'M1'): 0,
    ('O2',1,'M2'): 1,
    ('O2',2,'M1'): 0,
    ('O2',2,'M2'): 1,
    ('O2',3,'M1'): 0,
    ('O2',3,'M2'): 1,
    ('O3',1,'M1'): 0,
    ('O3',1,'M2'): 1,
    ('O3',2,'M1'): 0,
    ('O3',2,'M2'): 1,
    ('O3',3,'M1'): 1,
    ('O3',3,'M2'): 0,
    ('O4',1,'M1'): 1,
    ('O4',1,'M2'): 0,
    ('O4',2,'M1'): 0,
    ('O4',2,'M2'): 1,
    ('O4',3,'M1'): 0,
    ('O4',3,'M2'): 1,
    
    }


# 各种统计数据
nORDERS = len(ORDERS)
nSTEPS = len(STEPS)
nRESOURCES= len(RESOURCES)
nMOULDS = len(MOULDS)

M = 1000

# 时段数量
SLOTS = range(nORDERS * nSTEPS)


###############################   模型   ###################################

# 创建模型
model = gp.Model('AssemblyAPS')

# 变量： 每个订单每道工序的起始时间和终止时间
start =  model.addVars(ORDERS, STEPS, vtype = GRB.INTEGER, name="start")
end =  model.addVars(ORDERS, STEPS, vtype = GRB.INTEGER, name="end")

# 变量：每个设备/模具 每个时段上对应的每个产品每道工序起始时间和终止时间
startR =  model.addVars(RESOURCES, SLOTS, ORDERS, STEPS, vtype = GRB.INTEGER, name="startR")
startM =  model.addVars(MOULDS, SLOTS, ORDERS, STEPS, vtype = GRB.INTEGER, name="startM")
endR =  model.addVars(RESOURCES, SLOTS, ORDERS, STEPS, vtype = GRB.INTEGER, name="endR")
endM =  model.addVars(MOULDS, SLOTS, ORDERS, STEPS, vtype = GRB.INTEGER, name="endM")

# 变量：每个订单每道工序使用的设备
useResource = model.addVars(RESOURCES, SLOTS, ORDERS, STEPS, vtype = GRB.BINARY, name="useResource")

# 变量：每个订单每道工序使用的模具
useMould = model.addVars(MOULDS, SLOTS, ORDERS, STEPS, vtype = GRB.BINARY, name="useMould")

# 变量：每个设备/模具在每个时段的起始时间和终止时间
rSlotStartTime = model.addVars(RESOURCES, SLOTS, name="rSlotStartTime")
mSlotStartTime = model.addVars(MOULDS, SLOTS, name="mSlotStartTime")
rSlotEndTime = model.addVars(RESOURCES, SLOTS, name="rSlotEndTime")
mSlotEndTime = model.addVars(MOULDS, SLOTS, name="mSlotEndTime")

# 总时长
timeSpan = model.addVar(vtype = GRB.INTEGER, name="timeSpan")

#1. 订单每道工序起始时间不能早于前道工序结束时间
for step in STEPS:
    for order in ORDERS:
        model.addConstr(end[order, step] == start[order, step] + STEP_TIME[order, step])

for step in STEPS[1:]:
    for order in ORDERS:
        model.addConstr(start[order,step] >= end[order, step-1])
       
#2. 满足设备需求
for order in ORDERS:
    for step in STEPS:
        model.addConstr(sum(useResource[resource, slot, order, step] for resource in RESOURCES for slot in SLOTS) == 1 )
        model.addConstrs(sum(useResource[resource, slot, order, step] for slot in SLOTS) <= STEP_RESOURCES[order, step, resource] for resource in RESOURCES )

#3. 满足模具需求
for order in ORDERS:
    for step in STEPS:
        model.addConstr(sum(useMould[mould, slot, order, step] for mould in MOULDS for slot in SLOTS) == 1 )
        model.addConstrs(sum(useMould[mould, slot, order, step] for slot in SLOTS) <= STEP_MOULDS[order, step, mould] for mould in MOULDS )

#4. 每个设备/模具每个时段中只能分配被一个产品的一道工序占用
model.addConstrs(sum(useResource[resource, slot, order, step] for order in ORDERS for step in STEPS) <= 1 for resource in RESOURCES for slot in SLOTS)
model.addConstrs(sum(useMould[mould, slot, order, step] for order in ORDERS for step in STEPS) <= 1 for mould in MOULDS for slot in SLOTS)


#5. 每个设备每个时段在每个产品和工序的起始时间终止时间
for resource in RESOURCES:
    for slot in SLOTS:
        for order in ORDERS:
            for step in STEPS:
                model.addConstr(startR[resource, slot, order, step] <= start[order, step] + (1-useResource[resource, slot, order, step])* M)       
                model.addConstr(startR[resource, slot, order, step] >= start[order, step] - (1-useResource[resource, slot, order, step])* M)  
                model.addConstr(startR[resource, slot, order, step] <= useResource[resource, slot, order, step]* M)  
                model.addConstr(endR[resource, slot, order, step] <= start[order, step] + STEP_TIME[order, step] + (1-useResource[resource, slot, order, step])* M)       
                model.addConstr(endR[resource, slot, order, step] >= start[order, step] + STEP_TIME[order, step] - (1-useResource[resource, slot, order, step])* M)  
                model.addConstr(endR[resource, slot, order, step] <= useResource[resource, slot, order, step]* M)

#6. 每个设备每个时段的起始时间和终止时间
for resource in RESOURCES:
    for slot in SLOTS:
        model.addConstr(rSlotStartTime[resource, slot] == sum(startR[resource, slot, order, step] for order in ORDERS for step in STEPS))
        model.addConstr(rSlotEndTime[resource, slot] == sum(endR[resource, slot, order, step] for order in ORDERS for step in STEPS))

#7. 每个模具每个时段在每个产品和工序的起始时间终止时间
for mould in MOULDS:
    for slot in SLOTS:
        for order in ORDERS:
            for step in STEPS:
                model.addConstr(startM[mould, slot, order, step] <= start[order, step] + (1-useMould[mould, slot, order, step])* M)       
                model.addConstr(startM[mould, slot, order, step] >= start[order, step] - (1-useMould[mould, slot, order, step])* M)  
                model.addConstr(startM[mould, slot, order, step] <= useMould[mould, slot, order, step]* M) 
                model.addConstr(endM[mould, slot, order, step] <= start[order, step] + STEP_TIME[order, step] + (1-useMould[mould, slot, order, step])* M)       
                model.addConstr(endM[mould, slot, order, step] >= start[order, step] + STEP_TIME[order, step] - (1-useMould[mould, slot, order, step])* M)  
                model.addConstr(endM[mould, slot, order, step] <= useMould[mould, slot, order, step]* M) 

#8. 每个模具每个时段的起始时间和终止时间 
for mould in MOULDS:
    for slot in SLOTS:
        model.addConstr(mSlotStartTime[mould, slot] == sum(startM[mould, slot, order, step] for order in ORDERS for step in STEPS))
        model.addConstr(mSlotEndTime[mould, slot] == sum(endM[mould, slot, order, step] for order in ORDERS for step in STEPS))
        
#9，起点时间限制为0 
for resource in RESOURCES:
    model.addConstr(rSlotStartTime[resource, 0] == 0)
    
for mould in MOULDS:
    model.addConstr(mSlotStartTime[mould, 0] == 0)


#10. 设备和模具的每个时段的起始时间不能早于前个时段的终止时间
for resource in RESOURCES:
    for slot in SLOTS[1:]:
          model.addConstr(rSlotEndTime[resource, slot-1] <= rSlotStartTime[resource, slot])

for mould in MOULDS:
    for slot in SLOTS[1:]:
          model.addConstr(mSlotEndTime[mould, slot-1] <= mSlotStartTime[mould, slot])                         
    

#11. 定义 timespan 为最晚完成订单的终止时间
model.addConstr(timeSpan == max_([end[order, step] for order in ORDERS for step in STEPS]))

# 最小化完成时间
model.setObjective(timeSpan, GRB.MINIMIZE)

# 输出到 LP 文件
model.write("assemblyAPS.lp")

# 优化
model.optimize()



print('\n\n###############################   输出结果   ######################################\n')
print('总时长：'+ '%3d' % model.objval)

print('订单工序计划：')
for order in ORDERS:
    for step in STEPS:
        string = order + '\t' + str(step) + '%10s'% str(start[order,step].x) +'%10s'% str(end[order,step].x) +'\t'
        stop = 0
        for resource in RESOURCES:
            for slot in SLOTS:
                if abs(useResource[resource, slot, order, step].x -1) <= 0.01:
                    string = string + resource + '\t'
                    stop = 1
                    break
            if stop == 1:
                break
        stop = 0
        for mould in MOULDS:
            for slot in SLOTS:
                if abs(useMould[mould, slot, order, step].x -1) <= 0.01:
                    string = string + mould + '\t'
                    stop = 1
                    break
            if stop == 1:
                break
        
        print(string)            
        
print('\n')

print('设备使用计划:')

for resource in RESOURCES:
    for slot in SLOTS:
        string= ''
        if rSlotEndTime[resource, slot].x > rSlotStartTime[resource, slot].x:
            string = resource + '%10s'% str(rSlotStartTime[resource, slot].x) + '%10s'% str(rSlotEndTime[resource, slot].x) + '\t'
            stop = 0
            for order in ORDERS:
                for step in STEPS:
                    if abs(useResource[resource, slot, order, step].x -1) <= 0.01:
                        string = string + order + '\t' + str(step)
                        stop = 1
                        break
                if stop == 1:
                    break
            print(string)
        
print('\n')
print('模具使用计划:')

for mould in MOULDS:
    for slot in SLOTS:
        string= ''
        if mSlotEndTime[mould, slot].x > mSlotStartTime[mould, slot].x:
            string = mould + '%10s'% str(mSlotStartTime[mould, slot].x) + '%10s'% str(mSlotEndTime[mould, slot].x) + '\t'
            stop = 0
            for order in ORDERS:
                for step in STEPS:
                    if abs(useMould[mould, slot, order, step].x -1) <= 0.01:
                        string = string + order + '\t' + str(step)
                        stop = 1
                        break
                if stop == 1:
                    break
            print(string)

