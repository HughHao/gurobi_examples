from gurobipy import *

# 输入数据
n = 3
m = 3
T = [2, 3, 1]
proc_time = [
    [1, 2, 1],
    [2, 1, 3],
    [3, 2, 1]
]

# 创建模型
model = Model("Permutation flowshop scheduling problem")

# 创建变量
X = [[model.addVar(vtype=GRB.BINARY, name=f"X_{i}_{j}") for j in range(m)] for i in range(n)]
C = [[model.addVar(vtype=GRB.CONTINUOUS, name=f"C_{i}_{j}") for j in range(m)] for i in range(n)]
T_j = [model.addVar(vtype=GRB.CONTINUOUS, name=f"T_{j}") for j in range(m)]

# 设置目标函数
model.setObjective(C[n-1][m-1], GRB.MINIMIZE)

# 添加约束
for i in range(n):
    model.addConstr(quicksum(X[i]) == 1)
for j in range(m):
    model.addConstr(quicksum(X[i][j] for i in range(n)) == 1)
for i in range(1, n):
    for j in range(1, m):
        model.addConstr(C[i][j] >= C[i-1][j] + C[i][j-1] - T_j[j])
        model.addConstr(C[i][j] >= C[i][j-1] + C[i-1][j] - T_j[j])
for i in range(n):
    model.addConstr(C[i][0] == quicksum(X[k][0]*T[0] for k in range(i+1)))
for j in range(m):
    model.addConstr(C[0][j] == quicksum(X[0][k]*T[k] for k in range(j+1)))
for j in range(m):
    model.addConstr(T_j[j] >= C[n-1][j] + proc_time[n-1][j] - T[j])

# 求解模型
model.optimize()

# 输出结果
print("Optimal objective value: %.2f" % model.ObjVal)
for i in range(n):
    for j in range(m):
        if X[i][j].x > 0.5:
            print(f"Job {i+1} processed on machine {j+1} with completion time {C[i][j].x:.2f}")