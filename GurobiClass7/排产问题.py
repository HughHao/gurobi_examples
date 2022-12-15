# -*- coding: utf-8 -*-
"""
@author: help@gurobi.cn
"""

from gurobipy import *
import xlrd, xlsxwriter, datetime, math
from xlrd import xldate_as_datetime
from collections import OrderedDict


def ReadData(DataPath, Production):
    print("ReadData !")
    data = xlrd.open_workbook(DataPath)
    table = data.sheets()[0]  # Matrixdata
    nrows = table.nrows
    for i in range(1, nrows):
        row = table.row_values(i)
        if i not in Production.keys():
            Production[i - 1] = row[:]
    # Production[i][2]是产品i的生产速度，即每小时生产的数量

def BuildModel(Production, workingHours, workingHoursLimt, weighted1, weighted2, weighted3, bestX, bestY, bestE, bestU,
               bestV, bestW):
    xindex = {}  # 第t天生产第i种产品数量1花费的时间
    yindex = {}  # 第t天是否生产第i种产品
    Nindex = {}  # 整数值，保证第t天生产第i种产品数量是材料批量的整数倍
    Eindex = {}  # 第t天生产的第i种产品调用了第j种产品的货架数量
    Uindex = {}  # 第t天单班生产
    Vindex = {}  # 第t天双班生产
    Windex = {}  # 第t天加班时间

    for t in range(7):
        Uindex[t] = 0
        Vindex[t] = 0
        Windex[t] = 0
        for i in range(len(Production)):
            xindex[i, t] = 1 / Production[i][2]  # 产品i在第t天生产数量1花费的时间
            yindex[i, t] = 0
            Nindex[i, t] = 0
            for j in range(len(Production)):
                if i != j and Production[i][1] == Production[j][1]:  # 产品i和产品j是同一种类别的产品
                    Eindex[i, j, t] = 0  # 产品i在第t天调用了产品j的货架数量初始化为0

    try:
        m = Model()
        x = m.addVars(xindex.keys(), vtype=GRB.INTEGER, name='x')  # 变量x_{it}
        y = m.addVars(yindex.keys(), obj=weighted2, vtype=GRB.BINARY, name='y')  # 变量y_{it}
        z = m.addVar(obj=1, vtype=GRB.CONTINUOUS, name='z')  # 变量z
        e = m.addVars(Eindex.keys(), vtype=GRB.INTEGER, name='e')  # 变量e_{ijt}
        n = m.addVars(Nindex.keys(), vtype=GRB.INTEGER, name='n')  # 变量n_{it}
        u = m.addVars(Uindex.keys(), obj=weighted3, vtype=GRB.BINARY, name='u')  # 变量u_{t}
        v = m.addVars(Vindex.keys(), obj=2 * weighted3, vtype=GRB.BINARY, name='v')  # 变量v_{t}
        w = m.addVars(Windex.keys(), obj=weighted1, vtype=GRB.CONTINUOUS, name='w')  # 变量w_{t}

        # (1)	每种产品若生产则其工时大于0.9
        for i in xindex.keys():
            m.addConstr(x[i] >= 0.9 * Production[i[0]][2] * y[i])
            m.addConstr(x[i] <= (workingHoursLimt + 1) * Production[i[0]][2] * y[i])

        # (2)  每天的工时不超过 workingHoursLimt 小时，所有产品每天的花费时间之和小于等于 workingHoursLimt 小时
        for t in range(7):
            m.addConstr(x.prod(xindex, '*', t) <= 0.5 * u[t] * workingHoursLimt + v[t] * workingHoursLimt)

        # (3)  生产产品数量要为原料批量的整数倍
        for i in xindex.keys():
            m.addConstr(x[i] == Production[i[0]][3] * n[i])

        # (4)(5)  每天产品库存数量不超过料架数量，且不得低于安全库存
        for i in xindex.keys():  # 第i种产品调用第j种产品的货架的容量
            expr = LinExpr()
            for j in range(i[1] + 1):  # 第j天的产品i的库存数量累积
                expr += x[i[0], j] - Production[i[0]][6 + j]  # 某一种产品几天的剩余数量=累计几天(每天生产的数量-每天销售的数量)

            m.addConstr(  # 初始库存+累积库存<=该产品自身的料架容量+调用其他产品料架的容量-被调用的容量，该产品自身料架容纳数量=其原料批量*10
                Production[i[0]][5] + expr <= Production[i[0]][3] * 10 + e.sum(i[0], '*', i[1]) - e.sum('*', i[0],
                                                                                                        i[1]))
            m.addConstr(Production[i[0]][5] + expr >= Production[i[0]][7 + j] * Production[i[0]][4])
            # 某天的剩余数量大于后一天的安全库存=第i种产品第 t 天某产品的安全库存 = 第 t + 1 天的需求量*安全库存基准；
        # (6) 某产品j能被调用料架的数量不能超过对应的料架总容量
        for t in range(7):
            for i in range(len(Production)):
                m.addConstr(e.sum('*', i, t) <= Production[i][3] * 10)

        # (7)  Z值表示产品日库存最大值
        for t in range(7):  # 第t天
            expr = LinExpr()  # 初始化表达式为0
            for i in range(len(Production)):
                expr += Production[i][5]  # 第i种产品的初始库存
                # 所有产品的初始库存+产品第t天的库存数量-产品第t天的销售数量
                for j in range(t + 1):
                    expr += x[i, j] - Production[i][6 + j]  # 第i种产品的日库存=第i种产品第t天的生产数量-第i种产品第t天的销售数量
            m.addConstr(z >= expr)

        # (8)(9)(10)
        for t in range(7):  # 第t天
            m.addConstr(y.sum('*', t) >= u[t])  # y_{t}>=u_{t}
            m.addConstr(y.sum('*', t) >= v[t])
            m.addConstr(u[t] + v[t] <= 1)
            m.addConstr(y.sum('*', t) <= 10000 * u[t] + 10000 * v[t])

        # (11)  加班时间
        for t in range(7):
            m.addConstr(x.prod(xindex, '*', t) - workingHours * u[t] - 2 * workingHours * v[t] <= w[t])
        m.write('production.lp')
        m.optimize()

        # 获得优化结果
        for i in xindex.keys():
            bestX[i] = x[i].x  # 优化后的生产数量
            bestY[i] = y[i].x  # 优化后的生产天数

        for i in Uindex.keys():
            bestU[i] = u[i].x  # 优化后单班工作日
            bestV[i] = v[i].x  # 优化后双班工作日
            bestW[i] = w[i].x  # 优化后的加班时间

        for i in Eindex.keys():
            bestE[i] = e[i].x  # 优化后的每个产品七天调用其他产品的料架数量

    except GurobiError as exception:
        print('Error code ' + str(exception.errno) + ": " + str(exception))

    except AttributeError:
        print('Encountered an attribute error')


def OutputResult(Production, workingHours, bestX, bestY, bestE, bestU, bestV, bestW):
    hours = [0] * 7  # 每天的工作时间
    overtime = [0] * 7  # 每天的加班时间
    inventory = [0] * 7  # 每天的库存
    week = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    workbook = xlsxwriter.Workbook('案例1 结果.xls')

    #####################################
    worksheet = workbook.add_worksheet('排产方案')
    worksheet.write(0, 0, '产品编号')
    for t in range(7):
        if bestU[t] == 1:
            week[t] += '（单班）'
            worksheet.write(0, t + 1, week[t])
            overtime[t] = workingHours
        elif bestV[t] == 1:
            week[t] += '（双班）'
            worksheet.write(0, t + 1, week[t])
            overtime[t] = 2 * workingHours
        else:
            week[t] += '（---）'
            worksheet.write(0, t + 1, week[t])

    rows = 1
    for i in range(len(Production)):
        worksheet.write(rows, 0, Production[i][0])
        for t in range(7):
            worksheet.write(rows, t + 1, bestX[i, t])  # 产品i在第t天的生产数量
        rows += 1

    #####################################
    worksheet = workbook.add_worksheet('生产工时')
    worksheet.write(0, 0, '产品编号')
    for t in range(7):
        worksheet.write(0, t + 1, week[t])

    rows = 1
    for i in range(len(Production)):
        worksheet.write(rows, 0, Production[i][0])
        for t in range(7):
            worksheet.write(rows, t + 1, bestX[i, t] / Production[i][2])  # 产品i在第t天的生产工时
            hours[t] += bestX[i, t] / Production[i][2]  # 所有产品第t天的生产工时
        rows += 1

    worksheet.write(rows, 0, '工作时间')  # 紧接一行写入工作时间
    worksheet.write(rows + 1, 0, '加班时间')
    for t in range(7):
        worksheet.write(rows, t + 1, hours[t])  # 所有产品第t天的生产工时之和
        if overtime[t] < hours[t]:  # 如果可以工作的时间小于需要的工作时间，说明有产品没有按时完成
            worksheet.write(rows + 1, t + 1, hours[t] - overtime[t])  # 加班时间
        else:
            worksheet.write(rows + 1, t + 1, 0)  # 加班时间0

            #####################################
    worksheet = workbook.add_worksheet('产品库存')
    worksheet.write(0, 0, '产品编号')
    for t in range(7):
        worksheet.write(0, t + 1, week[t])  # 第一行写入周一到周日

    rows = 1  # 从第二行开始写入
    for i in range(len(Production)):
        sumInventory = Production[i][5]  # 产品i的库存初始化为产品i的初始库存
        worksheet.write(rows, 0, Production[i][0])  # 第一列写入产品编号
        for t in range(7):
            sumInventory += bestX[i, t] - Production[i][6 + t]  # 产品i的库存=上一天的库存+当天生产-当天销售
            inventory[t] += sumInventory  # 所有产品第t天的库存之和
            worksheet.write(rows, t + 1, sumInventory)  # 产品i的库存
        rows += 1

    worksheet.write(rows, 0, '库存合计')
    for t in range(7):
        worksheet.write(rows, t + 1, inventory[t])

    workbook.close()


try:
    DataPath = '案例1 数据.xls'  # 数据
    Production = OrderedDict()
    bestX = {}  # 第i个产品在第t天的生产量,大小为len(Production)*7=182
    bestY = {}  # 第i个产品在第t天是否生产
    bestZ = {}  # 计划期内最大库存
    bestE = {}  # 第i个产品在第t天的调用第j种料架的容量
    bestU = {}  # 第t天是否单班
    bestV = {}  # 第t天是否双班
    bestW = {}  # 第t天的加班时间

    weighted1 = 1  # 加班所占权重
    weighted2 = 1  # 更换模具次数所占的权重
    weighted3 = 1  # 班次所占的权重
    workingHours = 8  # 工作时长
    workingHoursLimt = 20  # 最长工作时间

    ReadData(DataPath, Production)
    BuildModel(Production, workingHours, workingHoursLimt, weighted1, weighted2, weighted3, bestX, bestY, bestE, bestU,
               bestV, bestW)
    OutputResult(Production, workingHours, bestX, bestY, bestE, bestU, bestV, bestW)
    print('Over.')

except GurobiError as exception:
    print('Error code ' + str(exception.errno) + ": " + str(exception))

except AttributeError:
    print('Encountered an attribute error')
