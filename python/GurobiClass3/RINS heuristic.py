# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:01:53 2018

@author: help@gurobi.cn
"""

from gurobipy import *
import random

def RINScallback(model, where):
    if where == GRB.Callback.MIPNODE:
        # MIP node callback
        if model.cbGet(GRB.Callback.MIPNODE_NODCNT) % 100 == 0 and \
           model.cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL:
             submodel = model.copy()
             suby = submodel.getVars()
             #获得节点松弛解
             yrelaxation = model.cbGetNodeRel(model._y)
             #固定变量取值
             for i in range(model._N):
                 if abs(yrelaxation[i])<0.01:
                     suby[i].ub = 0
                 elif abs(yrelaxation[i]-1)<0.01:
                     suby[i].lb = 1
             submodel.setParam(GRB.Param.TimeLimit, 30)
             submodel.optimize()
             if submodel.objval > model.cbGet(GRB.Callback.MIPNODE_OBJBST):
                 #将解传递给原模型
                 for i in range(model._N):
                     if abs(suby[i].x)<0.001:
                         model.cbSetSolution(model._y[i], 0.0)
                     elif abs(suby[i].x-1)<0.001: 
                         model.cbSetSolution(model._y[i], 1.0)

           
try:
    random.seed(1)
    N = 10
    #随机产生线段权重
    random.seed(1)
    Cmatrix = {(i,j):random.randint(0,100) for i in range(N) for j in range(N)}
    m = Model('MaximumCut')
    #添加变量
    y = m.addVars(N, vtype=GRB.BINARY, name='y')
    #构造目标函数
    obj = QuadExpr()
    for i in range(N):
        for j in range(N):
            obj = obj+Cmatrix[i,j]*(y[i]+y[j]-2*y[i]*y[j])
    m.setObjective(0.5*obj, -1)
    #设置求解时间
    m.Params.TimeLimit = 600
    #外部变量
    m._y = y
    m._N = N
    #求解
    m.optimize(RINScallback)
    #获得目标值和变量值
    print("Obj = ",m.ObjVal)
    for i in range(N):
        print(y[i].VarName,' = ',y[i].x)
    
except GurobiError:
    print('Error reported')