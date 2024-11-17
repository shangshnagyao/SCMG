# -*- coding: utf-8 -*-


import gurobipy as gp
import csv

model = gp.Model("model")
model.setParam('MIPGap', 0.01)             # 设置相对间隙为1%
model.setParam('MIPFocus', 1)              # 优先发现可行解
model.setParam('Threads', 4)               # 使用4个线程并行求解
model.setParam('TimeLimit', 7200)           # 设定求解时间上限为7200秒

step = 5
size = 16
                    #0  1  2  3  4  5  6  7  8  9  10 11
cost = gp.tuplelist([1, 1, 1, 2, 1, 1, 1, 3, 3, 2, 2, 2])
m =    gp.tuplelist([0, 1, 2, 3, 2, 1, 0, 0, 0, 0, 0, 0])   #m[] 是第j阶压缩器消耗的j阶input部分和的数量
p =    gp.tuplelist([3, 2, 1, 0, 0, 1, 2, 6, 5, 5, 4, 3])   #p[] 是第j阶压缩器消耗的j阶inter部分和的数量
q =    gp.tuplelist([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2])   #q[] 是第j阶压缩器消耗的j+1阶inter部分和的数量
u =    gp.tuplelist([1] * 12)                         #u[] 是第j阶压缩器生成的j阶inter部分和的数量
v =    gp.tuplelist([1] * 12)                         #v[] 是第j阶压缩器生成的j+1阶inter部分和的数量
z =    gp.tuplelist([0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1])   #z[] 是第j阶压缩器生成的j+2阶inter部分和的数量

Input = model.addVars(step + 1, 2 * size - 4, vtype=gp.GRB.INTEGER, name="input_pin")
Inter = model.addVars(step + 1, 2 * size - 4, vtype=gp.GRB.INTEGER, name="inter_pin")
Compressor = model.addVars(12, step, 2 * size - 4, vtype=gp.GRB.INTEGER, name="compressor")

model.setObjective(gp.quicksum(cost[k] * Compressor[k, i, j] for k in range(12) for i in range(step) for j in
                               range(2 * size - 4)) + 4 + 2 * size - 4)

model.addConstrs((Input[i, j] >= 0 for i in range(step + 1) for j in range(2 * size - 4)), name='input_positive')
model.addConstrs((Inter[i, j] >= 0 for i in range(step + 1) for j in range(2 * size - 4)), name='inter_positive')
model.addConstrs((Compressor[k, i, j] >= 0 for k in range(12) for i in range(step) for j in range(2 * size - 4)),
                 name='compressor_positive')
model.addConstrs((Compressor[k, i, 2 * size - 5] == 0 for k in range(12) for i in range(step)),
                 name='no_compressor_highest_bit')
model.addConstrs((Compressor[k, i, 2 * size - 6] == 0 for k in range(7, 12) for i in range(step)),
                 name='only_partial_compressor_second_highest_bit')

for i in range(step + 1):
    if i == 0:
        model.addConstrs((Input[0, j] == gp.min_(j + 4, 2 * size - j - 4) for j in range(2 * size - 4)),
                         name='input_init')
        model.addConstrs((Inter[0, j] == 0 for j in range(2 * size - 4)), name='inter_init')
    if i == step:
        model.addConstrs(((Input[step, j] + Inter[step, j] <= 2) for j in range(2 * size - 4)),
                         name='output_con1')
        model.addConstrs(((Input[step, j] + Input[step, j - 1] <= 1) for j in range(2, (2 * size - 4))),
                         name='output_con2')
    if i > 0:
        model.addConstrs(
            (Input[i, j] == (Input[i - 1, j] - gp.quicksum(m[k] * Compressor[k, i - 1, j] for k in range(12))) for j in
             range(2 * size - 4)), name='input_iteration')
        for j in range(2 * size - 4):
            if j == 0:
                model.addConstr(
                    (Inter[i, j] == (Inter[i - 1, j] - gp.quicksum(p[k] * Compressor[k, i - 1, j] for k in range(12)) \
                                     + gp.quicksum(u[k] * Compressor[k, i - 1, j] for k in range(12)))),
                    name='inter_iter_j0')
                model.addConstr(
                    (0 <= (Inter[i - 1, j] - gp.quicksum(p[k] * Compressor[k, i - 1, j] for k in range(12)))),
                    name='inter_PIN_j0')
            elif j == 1:
                model.addConstr(
                    (Inter[i, j] == (Inter[i - 1, j] - gp.quicksum(p[k] * Compressor[k, i - 1, j] for k in range(12)) \
                                     + gp.quicksum(u[k] * Compressor[k, i - 1, j] for k in range(12)) \
                                     - gp.quicksum(q[k] * Compressor[k, i - 1, j - 1] for k in range(12)) \
                                     + gp.quicksum(v[k] * Compressor[k, i - 1, j - 1] for k in range(12)))),
                    name='inter_iter_j1')
                model.addConstr((0 <= (Inter[i - 1, j] - gp.quicksum(p[k] * Compressor[k, i - 1, j] for k in range(12)) \
                                       - gp.quicksum(q[k] * Compressor[k, i - 1, j - 1] for k in range(12)))),
                                name='inter_PIN_j')
            else:
                model.addConstr(
                    (Inter[i, j] == (Inter[i - 1, j] - gp.quicksum(p[k] * Compressor[k, i - 1, j] for k in range(12)) \
                                     + gp.quicksum(u[k] * Compressor[k, i - 1, j] for k in range(12)) \
                                     - gp.quicksum(q[k] * Compressor[k, i - 1, j - 1] for k in range(12)) \
                                     + gp.quicksum(v[k] * Compressor[k, i - 1, j - 1] for k in range(12)) \
                                     + gp.quicksum(z[k] * Compressor[k, i - 1, j - 2] for k in range(12)))),
                    name='inter_iter_j2')
                model.addConstr((0 <= (Inter[i - 1, j] - gp.quicksum(p[k] * Compressor[k, i - 1, j] for k in range(12)) \
                                       - gp.quicksum(q[k] * Compressor[k, i - 1, j - 1] for k in range(12)))),
                                name='inter_PIN_j')
model.update()
model.optimize()

# 打印目标值
# print(f'Target value: {round(model.objVal)}\n')

with open('parameter.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([step, size, round(model.objVal)])

# 打印在 i == step 时的 Input 和 Inter 变量值
# print(f'\nValues of Input and Inter at i == step (i = {step}):')
for j in range(2 * size - 4):
    input_value = Input[step, j].x
    inter_value = Inter[step, j].x
#    print(f'Input[{step},{j}] = {input_value}, Inter[{step},{j}] = {inter_value}')

# 创建并写入CSV文件
with open('input_inter_values_at_step.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Index", "Input Value", "Inter Value"])

    # 保存在 i == step 时的 Input 和 Inter 变量值
    for j in range(2 * size - 4):
        input_value = Input[step, j].x
        inter_value = Inter[step, j].x
        writer.writerow([j, input_value, inter_value])

# 提取并打印压缩器变量值
compressor_values = []
for v in model.getVars():
    if v.varName.startswith("compressor") and v.x > 0.1:
        #print(f'vars:{v.varName}, value:{round(v.x)}')
        var_parts = v.varName.split('[')[1].split(']')[0].split(',')
        compressor_index = int(var_parts[0])
        value = round(v.x)
        compressor_values.append((compressor_index, int(var_parts[1]), int(var_parts[2]), value, cost[compressor_index]))

# 按第二维度（i）对压缩器值进行排序
compressor_values.sort(key=lambda x: x[1])

# 将压缩器值保存到CSV文件中
with open('compressor_values.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Dimension 1", "Dimension 2", "Dimension 3", "Value", "Cost"])
    writer.writerows(compressor_values)

print('*****************************************************************')
print(f'The multiplier of {size}-bit size within {step} steps consumes {round(model.objVal) + 1 if size > 4 else round(model.objVal)} LUTs!')