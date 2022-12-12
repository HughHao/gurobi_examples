# -*- coding: utf-8 -*-
"""
@author: help@gurobi.cn
"""

from gurobipy import *
TypesDemand = [3, 7, 9, 16]           		# 需求长度
QuantityDemand = [25, 30, 14, 8]      		# 需求的量
LengthUsable = 20                    		# 钢管长度
try:
    MainProbRelax = Model()                 # 松弛后的列生成主问题
    SubProb = Model()                       # 子问题

    # 构造主问题模型，选择的初始切割方案 每根钢管只切一种长度 
    # 添加变量
    Zp = MainProbRelax.addVars(len(TypesDemand), obj=1.0, vtype=GRB.CONTINUOUS, name = 'z')
    # 添加约束    
    ColumnIndex = MainProbRelax.addConstrs(quicksum(Zp[p] * (LengthUsable//TypesDemand[i]) \
    for p in range(len(TypesDemand)) if p==i) >= QuantityDemand[i] for i in range(len(TypesDemand)))  
    MainProbRelax.optimize()                # 求解


    # 构造子问题模型
    # 获得对偶值
    Dualsolution = MainProbRelax.getAttr(GRB.Attr.Pi, MainProbRelax.getConstrs())
    # 添加变量
    Ci = SubProb.addVars(len(TypesDemand), obj=Dualsolution, vtype=GRB.INTEGER, name = 'c')
    # 添加约束
    SubProb.addConstr(quicksum(Ci[i] * TypesDemand[i] for i in range(len(TypesDemand))) <= LengthUsable)
    SubProb.setAttr(GRB.Attr.ModelSense, -1) 	    # 设定优化方向             
    SubProb.optimize()                       		# 求解
    
    # 判断Reduced Cost是否小于零
    while SubProb.objval > 1:
           # 获取变量取值
           columnCoeff = SubProb.getAttr("X", SubProb.getVars())
           column = Column(columnCoeff, MainProbRelax.getConstrs())
           # 添加变量
           MainProbRelax.addVar(obj=1.0, vtype=GRB.CONTINUOUS, name="CG", column=column)
           MainProbRelax.optimize() 		# 求解
           # 修改子问题目标函数系数
           for i in range(len(TypesDemand)):
                Ci[i].obj = ColumnIndex[i].pi
           SubProb.optimize()
        
    # 将CG后的模型转为整数，并求解
    for v in MainProbRelax.getVars():
         v.setAttr("VType", GRB.INTEGER)
    MainProbRelax.optimize()
    for v in MainProbRelax.getVars():
         if v.X != 0.0:
              print('%s %g' % (v.VarName, v.X))

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')     
