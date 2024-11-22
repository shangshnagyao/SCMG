'''
Author:       xxx
Affiliation:  xxx University  

2024-08-08 Create file
2024-08-12 Determine the value of LUT_INIT_VAL
2024-08-17 complete the initial version of the code
2024-08-19 Still has some bugs in CLA part
2024-08-21 Fix the existing bugs
2024-08-26 Add odd-number multiplication
2024-08-30 fix the bug in Compressor 9 INIT parameter
2024-09-04 Regression validation
2024-09-11 Generation for synthesis
'''
from datetime import datetime
import csv

LUT_INIT_VAL = [['E8E8E8E896969696', 'error',            'error'           ],  # 0
                ['F880F88087788778', 'error',            'error'           ],  # 1
                ['F888800087777888', 'error',            'error'           ],  # 2
                ['8777788878887888', 'F888800080008000', 'error'           ],  # 3
                ['8000800078887888', 'error',            'error'           ],  # 4
                ['8080808078787878', 'error',            'error'           ],  # 5
                ['8888888866666666', 'error',            'error'           ],  # 6
                ['6996966996696996', '8117177E177E7EE8', 'FEE8E880E8808000'],  # 7
                ['9669699696696996', 'E8818117177E7EE8', 'FFFEFEE8E8808000'],  # 8
                ['177E7EE896696996', 'E8808000E8808000', 'error'           ],  # 9
                ['81177EE869966996', 'FEE88000FEE88000', 'error'           ],  # 10
                ['E81717E896969696', 'FFE8E800FFE8E800', 'error'           ],  # 11
                ]
                # inter-inter         #input-inter      #inter-input
CLUT_INIT_VAL = ['9666966660006000', '8778787878000000', '9666666660000000']


# Function to read the CSV file and store its contents in an array
def read_csv_to_array(file_path, start_row=0):
    array = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i >= start_row:
                array.append(row)
    return array

def count_csv_rows(file_path):
    row_count = 0
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            row_count += 1
    return row_count

def find_and_write_signal(file, lines, s, o, step, size, i_signal):
    find = 0
    for d in range(1, step + 1):
        for e in range(size):
            for b in range(len(lines)):
                if (f'p_s{s - d}_o{o}_{e}' == lines[b]):
                    lines.pop(b)
                    if (i_signal != 'I5'):
                        file.write(f'.{i_signal}(p_s{s - d}_o{o}_{e}),\n')
                    else:
                        file.write(f'.{i_signal}(p_s{s - d}_o{o}_{e}));\n')
                    find = 1
                    break
            if (find == 1):
                break
        if (find == 1):
            break

def find_and_write_signal_rtn0(file, lines, s, o, step, size, i_signal):
    for d in range(1, step + 1):
        for e in range(size):
            for b in range(len(lines)):
                if (f'p_s{s - d}_o{o}_{e}' == lines[b]):
                    lines.pop(b)
                    if (i_signal != 'I5'):
                        file.write(f'.{i_signal}(p_s{s - d}_o{o}_{e}),\n')
                    else:
                        file.write(f'.{i_signal}(p_s{s - d}_o{o}_{e}));\n')
                    return s - d, o, e
    return None

def find_and_write_signal_rtn(file, lines, s, o, step, size, i_signal):
    for d in range(step):
        for e in range(size):
            for b in range(len(lines)):
                if f'p_s{s - d}_o{o}_{e}' == lines[b]:
                    lines.pop(b)
                    if (i_signal != 'I5'):
                        file.write(f'.{i_signal}(p_s{s - d}_o{o}_{e}),\n')
                    else:
                        file.write(f'.{i_signal}(p_s{s - d}_o{o}_{e}));\n')
                    return s - d, o, e
    return None

# Example usage
file_path = 'compressor_values.csv'  # Replace with your file path
start_row = 1  # Replace with the row number you want to start reading from
csv_array = read_csv_to_array(file_path, start_row)
res_vec = read_csv_to_array('input_inter_values_at_step.csv', 1)
para_pack= read_csv_to_array('parameter.csv', 0)
step, size, target_value= map(int, para_pack[0])
col_order = 2 * size - 4
total_rows = count_csv_rows(file_path) - 1

with open('temp.txt', 'w') as file:
    g_nxt_cnt = 0
    g_nnxt_cnt = 0
    # INTER PP PART
    for s in range(step):
        for o in range(col_order):
            c_cur_cnt0 = 0
            c_cur_cnt = 0
            c_nxt_cnt = 0
            g_cur_cnt = g_nxt_cnt
            g_nxt_cnt = g_nnxt_cnt
            g_nnxt_cnt = 0

            hit = 0
            for t in range(total_rows):
                k = int(csv_array[t][0])
                if ((int(csv_array[t][1]) == s) & (int(csv_array[t][2]) == o)):
                    hit = 1
                    for v in range(int(csv_array[t][3])):
                        for z in range(int(csv_array[t][4])):
                            if (k == 0):
                                file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                g_cur_cnt += 1
                                g_nxt_cnt += 1
                            if (k == 1):
                                file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                g_cur_cnt += 1
                                g_nxt_cnt += 1
                            if (k == 2):
                                file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                g_cur_cnt += 1
                                g_nxt_cnt += 1
                            if (k == 3):
                                if (z == 1):
                                    file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                    g_nxt_cnt += 1
                                if (z == 0):
                                    file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                    g_cur_cnt += 1
                            if (k == 4):
                                file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                g_cur_cnt += 1
                                g_nxt_cnt += 1
                            if (k == 5):
                                file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                g_cur_cnt += 1
                                g_nxt_cnt += 1
                            if (k == 6):
                                file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                g_cur_cnt += 1
                                g_nxt_cnt += 1
                            if (k == 7):
                                if (z == 2):
                                    file.write(f"p_s{s}_o{o + 2}_{g_nnxt_cnt}\n")
                                    g_nnxt_cnt += 1
                                if (z == 1):
                                    file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                    g_nxt_cnt += 1
                                if (z == 0):
                                    file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                    g_cur_cnt += 1
                            if (k == 8):
                                if (z == 2):
                                    file.write(f"p_s{s}_o{o + 2}_{g_nnxt_cnt}\n")
                                    g_nnxt_cnt += 1
                                if (z == 1):
                                    file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                    g_nxt_cnt += 1
                                if (z == 0):
                                    file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                    g_cur_cnt += 1
                            if (k == 9):
                                if (z == 1):
                                    file.write(f"p_s{s}_o{o + 2}_{g_nnxt_cnt}\n")
                                    g_nnxt_cnt += 1
                                if (z == 0):
                                    file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                    g_nxt_cnt += 1
                                    file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                    g_cur_cnt += 1
                            if (k == 10):
                                if (z == 1):
                                    file.write(f"p_s{s}_o{o + 2}_{g_nnxt_cnt}\n")
                                    g_nnxt_cnt += 1
                                if (z == 0):
                                    file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                    g_nxt_cnt += 1
                                    file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                    g_cur_cnt += 1
                            if (k == 11):
                                if (z == 1):
                                    file.write(f"p_s{s}_o{o + 2}_{g_nnxt_cnt}\n")
                                    g_nnxt_cnt += 1
                                if (z == 0):
                                    file.write(f"p_s{s}_o{o + 1}_{g_nxt_cnt}\n")
                                    g_nxt_cnt += 1
                                    file.write(f"p_s{s}_o{o}_{g_cur_cnt}\n")
                                    g_cur_cnt += 1


lines = []
c_cur_cnt0_ary = []


with open('temp.txt', 'r') as file:
    for line in file:
        lines.append(line.strip())

d = 1

with open(f'mult_{size}b_{step}s.v', 'w') as file:
    
    file.write(f'module mult_{size}b_{step}s ( \n')
    file.write(f'input [{size}-1:0] a,\n')
    file.write(f'input [{size}-1:0] b,\n')
    file.write(f'output [2*{size}-1:0] r\n')
    file.write(');\n')
    file.write('\n')
    file.write(f'// Target value:{target_value}\n')
    file.write(f'wire [{2 * size - 5}:0] P;\n')
    file.write(f'wire [{2 * size - 5}:0] G;\n')
    file.write('\n')
    file.write('// 4 normal LUT\n')
    file.write('LUT6_2 #(\n')
    file.write(".INIT(64'h78887888C0C0C0C0)\n")
    file.write(') LUT6_2_inst_f0 (\n')
    file.write('.O6(r[1]),\n')
    file.write('.O5(r[0]),\n')
    file.write('.I0(b[1]),\n')
    file.write('.I1(a[0]),\n')
    file.write('.I2(b[0]),\n')
    file.write('.I3(a[1]),\n')
    file.write(".I4(1'b1),\n")
    file.write(".I5(1'b1));\n")
    file.write('\n')
    file.write('LUT6_2 #(\n')
    file.write(".INIT(64'h47777888B8887888)\n")
    file.write(') LUT6_2_inst_f1 (\n')
    file.write('.O6(r[2]),\n')
    file.write('.O5(),\n')
    file.write('.I0(b[2]),\n')
    file.write('.I1(a[0]),\n')
    file.write('.I2(b[1]),\n')
    file.write('.I3(a[1]),\n')
    file.write('.I4(b[0]),\n')
    file.write('.I5(a[2]));\n')
    file.write('\n')
    file.write('LUT6_2 #(\n')
    file.write(".INIT(64'hF8888000C0008000)\n")
    file.write(') LUT6_2_inst_f2 (\n')
    file.write('.O6(C1),\n')
    file.write('.O5(),\n')
    file.write('.I0(b[2]),\n')
    file.write('.I1(a[0]),\n')
    file.write('.I2(b[1]),\n')
    file.write('.I3(a[1]),\n')
    file.write('.I4(b[0]),\n')
    file.write('.I5(a[2]));\n')
    file.write('\n')
    file.write('LUT6_2 #(\n')
    file.write(".INIT(64'h8000000000000000)\n")
    file.write(') LUT6_2_inst_f3 (\n')
    file.write('.O6(C0),\n')
    file.write('.O5(),\n')
    file.write('.I0(b[2]),\n')
    file.write('.I1(a[0]),\n')
    file.write('.I2(b[1]),\n')
    file.write('.I3(a[1]),\n')
    file.write('.I4(b[0]),\n')
    file.write('.I5(a[2]));\n')
    file.write('\n')

    g_nxt_cnt = 0
    buf0 = 0
    buf1 = 0
    buf2 = 0
    ps = 0
    # INTER PP PART
    for s in range(step):
        for o in range(col_order):
            file.write(f'/////////STEP{s}----ORDER{o}////////////\n')
            file.write('\n')
            if (s == 0):
                if (o + 3 <= size - 1):
                    c_cur_cnt0 = 0
                else:
                    c_cur_cnt0 = o - size + 4
            else:
                c_cur_cnt0 = c_cur_cnt0_ary.pop(0)
            c_cur_cnt = 0
            c_nxt_cnt = 0
            g_cur_cnt = g_nxt_cnt
            g_nxt_cnt = g_nnxt_cnt
            g_nnxt_cnt = 0

            hit = 0
            for t in range(total_rows):
                k = int(csv_array[t][0])
                if ((int(csv_array[t][1]) == s) & (int(csv_array[t][2]) == o)):
                    hit = 1
                    for v in range(int(csv_array[t][3])):
                        for z in range(int(csv_array[t][4])):
                            if (k == 0):
                                file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                find_and_write_signal(file, lines, s, o, step, size, "I0")
                                find_and_write_signal(file, lines, s, o, step, size, "I1")
                                find_and_write_signal(file, lines, s, o, step, size, "I2")
                                file.write(f".I3(1'b0),\n")
                                file.write(f".I4(1'b0),\n")
                                file.write(f".I5(1'b1));\n")

                            if (k == 1):
                                file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                file.write(f'.I0(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I1(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                find_and_write_signal(file, lines, s, o, step, size, "I2")
                                find_and_write_signal(file, lines, s, o, step, size, "I3")
                                file.write(f".I4(1'b0),\n")
                                file.write(f".I5(1'b1));\n")

                            if (k == 2):
                                file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                file.write(f'.I0(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I1(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                file.write(f'.I2(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I3(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                find_and_write_signal(file, lines, s, o, step, size, "I4")
                                file.write(f".I5(1'b1));\n")

                            if (k == 3):
                                if (z == 1):
                                    file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                if (z == 0):
                                    file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                if (z == 1):
                                    file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                    g_cur_cnt -= 1
                                if (z == 0):
                                    file.write(f'.O6(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                    g_nxt_cnt -= 1
                                file.write(f'.O5(),\n')
                                file.write(f'.I0(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I1(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                file.write(f'.I2(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I3(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                file.write(f'.I4(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I5(b[{c_cur_cnt0}]));\n')
                                c_cur_cnt0 += 1
                                if (z != (int(csv_array[t][4]) - 1)):
                                    c_cur_cnt0 -= 3

                            if (k == 4):
                                file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                file.write(f'.I0(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I1(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                file.write(f'.I2(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I3(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                file.write(f".I4(1'b0),\n")
                                file.write(f".I5(1'b1));\n")

                            if (k == 5):
                                file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                file.write(f'.I0(a[{(o + 3) - c_cur_cnt0}]),\n')
                                file.write(f'.I1(b[{c_cur_cnt0}]),\n')
                                c_cur_cnt0 += 1
                                find_and_write_signal(file, lines, s, o, step, size, "I2")
                                file.write(f".I3(1'b0),\n")
                                file.write(f".I4(1'b0),\n")
                                file.write(f".I5(1'b1));\n")

                            if (k == 6):
                                file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                find_and_write_signal(file, lines, s, o, step, size, "I0")
                                find_and_write_signal(file, lines, s, o, step, size, "I1")
                                file.write(f".I2(1'b0),\n")
                                file.write(f".I3(1'b0),\n")
                                file.write(f".I4(1'b0),\n")
                                file.write(f".I5(1'b1));\n")

                            if (k == 7):
                                if (z == 2):
                                    file.write(f"wire p_s{s}_o{o + 2}_{g_nnxt_cnt};\n")
                                if (z == 1):
                                    file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                if (z == 0):
                                    file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                if (z == 2):
                                    file.write(f'.O6(p_s{s}_o{o + 2}_{g_nnxt_cnt}),\n')
                                    g_nxt_cnt -= 1
                                    g_cur_cnt -= 1
                                if (z == 1):
                                    file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                    g_cur_cnt -= 1
                                    g_nnxt_cnt -= 1
                                if (z == 0):
                                    file.write(f'.O6(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                    g_nxt_cnt -= 1
                                    g_nnxt_cnt -= 1
                                file.write(f'.O5(),\n')

                                if (z == 0):
                                    first_pop = True
                                else:
                                    first_pop = False

                                if first_pop:
                                    c_s0, c_o0, c_e0 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I0")
                                    c_s1, c_o1, c_e1 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I1")
                                    c_s2, c_o2, c_e2 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I2")
                                    c_s3, c_o3, c_e3 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I3")
                                    c_s4, c_o4, c_e4 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I4")
                                    c_s5, c_o5, c_e5 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I5")
                                else:
                                    file.write(f".I0(p_s{c_s0}_o{c_o0}_{c_e0}),\n")
                                    file.write(f'.I1(p_s{c_s1}_o{c_o1}_{c_e1}),\n')
                                    file.write(f'.I2(p_s{c_s2}_o{c_o2}_{c_e2}),\n')
                                    file.write(f'.I3(p_s{c_s3}_o{c_o3}_{c_e3}),\n')
                                    file.write(f'.I4(p_s{c_s4}_o{c_o4}_{c_e4}),\n')
                                    file.write(f'.I5(p_s{c_s5}_o{c_o5}_{c_e5}));\n')

                            if (k == 8):
                                if (z == 2):
                                    file.write(f"wire p_s{s}_o{o + 2}_{g_nnxt_cnt};\n")
                                if (z == 1):
                                    file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                if (z == 0):
                                    file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                if (z == 2):
                                    file.write(f'.O6(p_s{s}_o{o + 2}_{g_nnxt_cnt}),\n')
                                    g_nxt_cnt -= 1
                                    g_cur_cnt -= 1
                                if (z == 1):
                                    file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                    g_cur_cnt -= 1
                                    g_nnxt_cnt -= 1
                                if (z == 0):
                                    file.write(f'.O6(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                    g_nxt_cnt -= 1
                                    g_nnxt_cnt -= 1
                                file.write(f'.O5(),\n')

                                if (z == 0):
                                    first_pop = True
                                else:
                                    first_pop = False

                                if first_pop:
                                    c_s0, c_o0, c_e0 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I0")
                                    c_s1, c_o1, c_e1 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I1")
                                    c_s2, c_o2, c_e2 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I2")
                                    c_s3, c_o3, c_e3 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I3")
                                    c_s4, c_o4, c_e4 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I4")
                                    c_s5, c_o5, c_e5 = find_and_write_signal_rtn0(file, lines, s, o+1, step, size, "I5")
                                else:
                                    file.write(f".I0(p_s{c_s0}_o{c_o0}_{c_e0}),\n")
                                    file.write(f'.I1(p_s{c_s1}_o{c_o1}_{c_e1}),\n')
                                    file.write(f'.I2(p_s{c_s2}_o{c_o2}_{c_e2}),\n')
                                    file.write(f'.I3(p_s{c_s3}_o{c_o3}_{c_e3}),\n')
                                    file.write(f'.I4(p_s{c_s4}_o{c_o4}_{c_e4}),\n')
                                    file.write(f'.I5(p_s{c_s5}_o{c_o5}_{c_e5}));\n')

                            if (k == 9):
                                if (z == 1):
                                    file.write(f"wire p_s{s}_o{o + 2}_{g_nnxt_cnt};\n")
                                if (z == 0):
                                    file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                    file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                if (z == 1):
                                    file.write(f'.O6(p_s{s}_o{o + 2}_{g_nnxt_cnt}),\n')
                                    file.write(f'.O5(),\n')
                                    g_cur_cnt -= 1
                                    g_nxt_cnt -= 1
                                if (z == 0):
                                    file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                    file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                    g_nnxt_cnt -= 1
                                if (z == 0):
                                    first_pop = True
                                else:
                                    first_pop = False

                                if first_pop:
                                    c_s0, c_o0, c_e0 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I0")
                                    c_s1, c_o1, c_e1 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I1")
                                    c_s2, c_o2, c_e2 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I2")
                                    c_s3, c_o3, c_e3 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I3")
                                    c_s4, c_o4, c_e4 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I4")
                                else:
                                    file.write(f".I0(p_s{c_s0}_o{c_o0}_{c_e0}),\n")
                                    file.write(f'.I1(p_s{c_s1}_o{c_o1}_{c_e1}),\n')
                                    file.write(f'.I2(p_s{c_s2}_o{c_o2}_{c_e2}),\n')
                                    file.write(f'.I3(p_s{c_s3}_o{c_o3}_{c_e3}),\n')
                                    file.write(f'.I4(p_s{c_s4}_o{c_o4}_{c_e4}),\n')
                                file.write(f".I5(1'b1));\n")

                            if (k == 10):
                                if (z == 1):
                                    file.write(f"wire p_s{s}_o{o + 2}_{g_nnxt_cnt};\n")
                                if (z == 0):
                                    file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                    file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                if (z == 1):
                                    file.write(f'.O6(p_s{s}_o{o + 2}_{g_nnxt_cnt}),\n')
                                    file.write(f'.O5(),\n')
                                    g_cur_cnt -= 1
                                    g_nxt_cnt -= 1
                                if (z == 0):
                                    file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                    file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                    g_nnxt_cnt -= 1
                                if (z == 0):
                                    first_pop = True
                                else:
                                    first_pop = False

                                if first_pop:
                                    c_s0, c_o0, c_e0 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I0")
                                    c_s1, c_o1, c_e1 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I1")
                                    c_s2, c_o2, c_e2 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I2")
                                    c_s3, c_o3, c_e3 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I3")
                                    c_s4, c_o4, c_e4 = find_and_write_signal_rtn0(file, lines, s, o + 1, step, size, "I4")
                                else:
                                    file.write(f".I0(p_s{c_s0}_o{c_o0}_{c_e0}),\n")
                                    file.write(f'.I1(p_s{c_s1}_o{c_o1}_{c_e1}),\n')
                                    file.write(f'.I2(p_s{c_s2}_o{c_o2}_{c_e2}),\n')
                                    file.write(f'.I3(p_s{c_s3}_o{c_o3}_{c_e3}),\n')
                                    file.write(f'.I4(p_s{c_s4}_o{c_o4}_{c_e4}),\n')
                                file.write(f".I5(1'b1));\n")

                            if (k == 11):
                                if (z == 1):
                                    file.write(f"wire p_s{s}_o{o + 2}_{g_nnxt_cnt};\n")
                                if (z == 0):
                                    file.write(f"wire p_s{s}_o{o + 1}_{g_nxt_cnt};\n")
                                    file.write(f"wire p_s{s}_o{o}_{g_cur_cnt};\n")
                                file.write('LUT6_2 #(\n')
                                file.write(f".INIT(64'h{LUT_INIT_VAL[int(csv_array[t][0])][z]})\n")
                                file.write(f') LUT6_2_inst_s{s}_o{o}_t{t}_z{z}_v{v} (\n')
                                if (z == 1):
                                    file.write(f'.O6(p_s{s}_o{o + 2}_{g_nnxt_cnt}),\n')
                                    file.write(f'.O5(),\n')
                                    g_cur_cnt -= 1
                                    g_nxt_cnt -= 1
                                if (z == 0):
                                    file.write(f'.O6(p_s{s}_o{o + 1}_{g_nxt_cnt}),\n')
                                    file.write(f'.O5(p_s{s}_o{o}_{g_cur_cnt}),\n')
                                    g_nnxt_cnt -= 1
                                if (z == 0):
                                    first_pop = True
                                else:
                                    first_pop = False

                                if first_pop:
                                    c_s0, c_o0, c_e0 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I0")
                                    c_s1, c_o1, c_e1 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I1")
                                    c_s2, c_o2, c_e2 = find_and_write_signal_rtn0(file, lines, s, o, step, size, "I2")
                                    c_s3, c_o3, c_e3 = find_and_write_signal_rtn0(file, lines, s, o + 1, step, size, "I3")
                                    c_s4, c_o4, c_e4 = find_and_write_signal_rtn0(file, lines, s, o + 1, step, size, "I4")
                                else:
                                    file.write(f".I0(p_s{c_s0}_o{c_o0}_{c_e0}),\n")
                                    file.write(f'.I1(p_s{c_s1}_o{c_o1}_{c_e1}),\n')
                                    file.write(f'.I2(p_s{c_s2}_o{c_o2}_{c_e2}),\n')
                                    file.write(f'.I3(p_s{c_s3}_o{c_o3}_{c_e3}),\n')
                                    file.write(f'.I4(p_s{c_s4}_o{c_o4}_{c_e4}),\n')
                                file.write(f".I5(1'b1));\n")

                            file.write('\n')
                            g_cur_cnt += 1
                            g_nxt_cnt += 1
                            if (k in range(7, 12)):
                                g_nnxt_cnt += 1

            c_cur_cnt0_ary.append(c_cur_cnt0)
            if (s == step - 1):
                if (o == 0):
                    if (round(float(res_vec[o][1])) == 1):
                        file.write('LUT6_2 #(\n')
                        file.write(".INIT(64'h8778877808800880)\n")
                        file.write(f') LUT6_2_inst_oo{o} (\n')
                        file.write(f'.O6(P[{o}]),\n')
                        file.write(f'.O5(G[{o}]),\n')
                        file.write(f'.I0(a[0]),\n')
                        file.write(f'.I1(b[3]),\n')
                        file.write(f'.I2(C0),\n')
                        s0,o0,e0 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I3")
                        file.write(f".I4(1'b1),\n")
                        file.write(f".I5(1'b1));\n")
                        file.write('\n')
                        buf0 = f'C0'
                        buf1 = f'p_s{s0}_o{o0}_{e0}'
                        buf2 = f'error!'
                    else:
                        file.write('LUT6_2 #(\n')
                        file.write(".INIT(64'h8778877808800880)\n")
                        file.write(f') LUT6_2_inst_oo{o} (\n')
                        file.write(f'.O6(P[{o}]),\n')
                        file.write(f'.O5(G[{o}]),\n')
                        file.write(f'.I0(C0),\n')
                        s0,o0,e0 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I1")
                        find_and_write_signal(file, lines, s, o, step, size, "I2")
                        file.write(f".I3(1'b1),\n")
                        file.write(f".I4(1'b1),\n")
                        file.write(f".I5(1'b1));\n")
                        file.write('\n')

                        buf0 = f'C0'
                        buf1 = f'p_s{s0}_o{o0}_{e0}'
                        buf2 = f'error!'
                elif (o < 2 * size - 5):
                    if (round(float(res_vec[o][1])) == 1):
                        file.write('LUT6_2 #(\n')
                        file.write(f".INIT(64'h{CLUT_INIT_VAL[1]})\n")
                        file.write(f') LUT6_2_inst_oo{o} (\n')
                        file.write(f'.O6(P[{o}]),\n')
                        file.write(f'.O5(G[{o}]),\n')
                        if (o+3<=size-1):
                            file.write(f'.I0(a[0]),\n')
                            file.write(f'.I1(b[{o+3}]),\n')
                        else:
                            file.write(f'.I0(a[{o-size+4}]),\n')
                            file.write(f'.I1(b[{size-1}]),\n')
                        s0,o0,e0 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I2")
                        file.write(f'.I3({buf0}),\n')
                        file.write(f'.I4({buf1}),\n')
                        file.write(f".I5(1'b1));\n")
                        file.write('\n')
                        if (o + 3 <= size - 1):
                            buf0 = f'a[0]'
                            buf1 = f'b[{o + 3}]'
                        else:
                            buf0 = f'a[{o - size + 4}]'
                            buf1 = f'b[{size - 1}]'
                        buf2 = f'p_s{s0}_o{o0}_{e0}'
                    elif (round(float(res_vec[o - 1][1])) == 1):
                        if (o == 1):
                            file.write('LUT6_2 #(\n')
                            file.write(f".INIT(64'h{CLUT_INIT_VAL[2]})\n")
                            file.write(f') LUT6_2_inst_oo{o} (\n')
                            file.write(f'.O6(P[{o}]),\n')
                            file.write(f'.O5(G[{o}]),\n')
                            s0,o0,e0 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I0")
                            s1,o1,e1 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I1")
                            file.write(f'.I2({buf0}),\n')
                            file.write(f'.I3({buf1}),\n')
                            file.write(f".I4(1'b1),\n")
                            file.write(f".I5(1'b1));\n")
                            file.write('\n')

                            buf0 = f'p_s{s0}_o{o0}_{e0}'
                            buf1 = f'p_s{s1}_o{o1}_{e1}'
                            buf2 = f'error!'
                        else:
                            file.write('LUT6_2 #(\n')
                            file.write(f".INIT(64'h{CLUT_INIT_VAL[2]})\n")
                            file.write(f') LUT6_2_inst_oo{o} (\n')
                            file.write(f'.O6(P[{o}]),\n')
                            file.write(f'.O5(G[{o}]),\n')
                            s0, o0, e0 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I0")
                            s1, o1, e1 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I1")
                            file.write(f'.I2({buf0}),\n')
                            file.write(f'.I3({buf1}),\n')
                            file.write(f".I4({buf2}),\n")
                            file.write(f".I5(1'b1));\n")
                            file.write('\n')

                            buf0 = f'p_s{s0}_o{o0}_{e0}'
                            buf1 = f'p_s{s1}_o{o1}_{e1}'
                            buf2 = f'error!'
                    else:
                        file.write('LUT6_2 #(\n')
                        file.write(f".INIT(64'h{CLUT_INIT_VAL[0]})\n")
                        file.write(f') LUT6_2_inst_oo{o} (\n')
                        file.write(f'.O6(P[{o}]),\n')
                        file.write(f'.O5(G[{o}]),\n')

                        s0, o0, e0 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I0")
                        if (round(float(res_vec[o][2])) > 1):
                            s1, o1, e1 = find_and_write_signal_rtn(file, lines, s, o, step, size, "I1")
                        else:
                            file.write(f".I1(1'b0),\n")
                            ps = 1

                        file.write(f'.I2({buf0}),\n')
                        file.write(f'.I3({buf1}),\n')
                        file.write(f".I4(1'b1),\n")
                        file.write(f".I5(1'b1));\n")
                        file.write('\n')

                        buf0 = f'p_s{s0}_o{o0}_{e0}'
                        if ps == 1:
                            buf1 = "1'b0"
                        else :
                            buf1 = f'p_s{s1}_o{o1}_{e1}'
                        buf2 = f'error!'
                        ps = 0

    # PPG ADD PART
    file.write('LUT6_2 #(\n')
    file.write(".INIT(64'h87777888F8888000)\n")
    file.write(') LUT6_2_inst_ooo (\n')
    file.write(f'.O6(P[{o}]),\n')
    file.write(f'.O5(G[{o}]),\n')
    file.write(f'.I0(b[{size - 1}]),\n')
    file.write(f'.I1(a[{size - 1}]),\n')
    file.write(f'.I2({buf0}),\n')
    file.write(f'.I3({buf1}),\n')
    last = lines.pop(0)
    file.write(f'.I4({last}),\n')
    file.write(f".I5(1'b1));\n")
    file.write('\n')

    # Carry Chain
    cr = (size * 2 - 4) // 4 if size%2 == 0 else ((size * 2 - 4) // 4)+1
    for b in range(cr):
        file.write(f'wire [3:0] carry_o_{b};\n')
        if (b == 0):
            file.write(f'CARRY4  CARRY4_inst_{b}(\n')
            file.write(f".CO(carry_o_{b}),\n")
            file.write(f".O(r[{(b + 1) * 4 + 2}:{b * 4 + 3}]),\n")
            file.write(f".CI(C1),\n")
            file.write(f".CYINIT(1'b0),\n")
            file.write(f".DI(G[{(b + 1) * 4 - 1}:{b * 4}]),\n")
            file.write(f".S(P[{(b + 1) * 4 - 1}:{b * 4}]));\n")
            file.write('\n')
            if (size == 4):
                file.write(f"assign  r[{2 * size - 1}] = carry_o_{((size * 2 - 4) // 4) - 1}[3] ;\n")
        else:
            if (size%2 == 0):
                file.write(f'CARRY4  CARRY4_inst_{b}(\n')
                file.write(f".CO(carry_o_{b}),\n")
                file.write(f".O(r[{(b + 1) * 4 + 2}:{b * 4 + 3}]),\n")
                file.write(f".CI(carry_o_{b - 1}[3]),\n")
                file.write(f".CYINIT(1'b0),\n")
                file.write(f".DI(G[{((b + 1) * 4) - 1}:{b * 4}]),\n")
                file.write(f".S(P[{((b + 1) * 4) - 1}:{b * 4}]));\n")
                file.write('\n')
                if(b == cr - 1):
                    file.write(f"assign  r[{2 * size - 1}] = carry_o_{((size * 2 - 4) // 4) - 1}[3] | (P[{2 * size - 5}] & G[{2 * size - 5}]);\n")
            else:
                if (b < cr - 1):
                    file.write(f'CARRY4  CARRY4_inst_{b}(\n')
                    file.write(f".CO(carry_o_{b}),\n")
                    file.write(f".O(r[{(b + 1) * 4 + 2}:{b * 4 + 3}]),\n")
                    file.write(f".CI(carry_o_{b - 1}[3]),\n")
                    file.write(f".CYINIT(1'b0),\n")
                    file.write(f".DI(G[{((b + 1) * 4) - 1}:{b * 4}]),\n")
                    file.write(f".S(P[{((b + 1) * 4) - 1}:{b * 4}]));\n")
                    file.write('\n')
                else:
                    file.write('wire [1:0] r0;\n')
                    file.write(f'CARRY4  CARRY4_inst_{b}(\n')
                    file.write(f".CO(carry_o_{b}),\n")
                    file.write(f".O(")
                    file.write("{")
                    file.write(f"r0,r[{(b + 1) * 4}:{b * 4 + 3}]")
                    file.write("}")
                    file.write("),\n")
                    file.write(f".CI(carry_o_{b - 1}[3]),\n")
                    file.write(f".CYINIT(1'b0),\n")
                    file.write(f".DI(")
                    file.write("{")
                    file.write(f"2'b0,G[{((b + 1) * 4) - 3}:{b * 4}]")
                    file.write("}")
                    file.write("),\n")
                    file.write(f".S(")
                    file.write("{")
                    file.write(f"2'b0,P[{((b + 1) * 4) - 3}:{b * 4}]")
                    file.write("}")
                    file.write("));\n")
                    file.write('\n')

                    file.write(f"assign r[{(b + 1) * 4 + 1}] = r0[0] | (P[{2 * size - 5}] & G[{2 * size - 5}]);\n")

    file.write(f'//v{datetime.now()}\n')
    file.write('endmodule\n')

    print(len(lines))
