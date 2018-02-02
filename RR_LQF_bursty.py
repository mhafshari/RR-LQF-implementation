###################################


# written by @mhafshari
# simulating bursty traffic on switches and routers
# RR/LQF algorithm implementation with any iteration and speedUp with bursty traffic

###################################


import random
import math
import time

total_arrived_packet = 0
total_passed_packet = 0
print("Enter probability (p) for inputs load")
p = float(input())
print("Enter switch size: ")
N = int(input())
print("Enter iteration times: ")
iteration = int(input())
print("Enter speedup: ")
speedup = int(input())
c = [[0] * N for i in range(N)]
n = math.ceil(N * p)
packet_arrive_each_input_port = [0] * N
packet_leave_each_input_port = [0] * N
matched_output = []
matched_input = []
on = [0] * n
off = [0] * n
out_port = [0] * N
input_arrive = [0] * N
input_unique = random.sample(range(0, N), n)
delay = [0] * 300
for T in range(300):
    start = time.clock()
    flag_output_report = [[0] * N for i in range(N)]
    # report
    print("request input->output")
    # producing bursty traffic based on p (load probability) and N (switch size)
    for k in range(int(n)):
        if on[k] == 0 and off[k] == 0:
            on[k] = 30
            out_port[k] = random.randrange(0, N, 1)
            input_arrive[k] = input_unique[k]
            if p < 1:
                off[k] = random.randrange(1, ((30 * (1 - p)) / p) + 1, 1)
            else:
                off[k] = 0
        if on[k] > 0:
            flag_output_report[input_arrive[k]][out_port[k]] = 1
            total_arrived_packet = total_arrived_packet + 1
            packet_arrive_each_input_port[input_arrive[k]] = packet_arrive_each_input_port[input_arrive[k]] + 1
            print(str(input_arrive[k]) + "->" + str(out_port[k]))
            on[k] = on[k] - 1
        elif off[k] > 0:
            off[k] = off[k] - 1

    for s in range(speedup):
        print("speedup " + str(s + 1))
        print("--------------------------------------------------------")
        matched_output.clear()
        matched_input.clear()
        for k in range(iteration):
            flag_input_report = [[0] * N for i in range(N)]
            print("*********iteration " + str(k + 1))
            # print(matched_input)
            # grant
            for j in range(N):
                if str(j) not in matched_output:
                    for i in range(N):
                        if (flag_output_report[i][j] == 1) and (str(i) not in matched_input):
                            c[i][j] = c[i][j] + 1
                            flag_output_report[i][j] = 0
            for j in range(N):
                if str(j) not in matched_output:
                    i = (j + T) % N
                    # print("prefer input is " + str(i) + " for output->" + str(j))
                    if (c[i][j] > 0) and (str(i) not in matched_input):
                        flag_input_report[i][j] = 1
                    else:
                        check = False
                        for i in range(N):
                            check = bool(c[i][j]) or check
                        if check:
                            maximum = 0
                            for i in range(N):
                                if str(i) not in matched_input:
                                    if c[i][j] > maximum:
                                        maximum = c[i][j]
                                        input_max = i
                                        output_max = j
                            flag_input_report[input_max][output_max] = 1
                            # print("counter is" + str(c))
                            # print("input flag is" + str(flag_input_report))

            # accept
            for i in range(N):
                if str(i) not in matched_input:
                    j = (i + T) % N
                    if flag_input_report[i][j] == 1:
                        if str(j) not in matched_output:
                            c[i][j] = c[i][j] - 1
                            flag_input_report[i][j] = 0
                            matched_output.append(str(j))
                            matched_input.append(str(i))
                            print("input " + str(i) + " matched " + str(j) + " (this matching occur by prefer output) ")
                            total_passed_packet = total_passed_packet + 1
                            packet_leave_each_input_port[i] = packet_leave_each_input_port[i] + 1
                    else:
                        check = False
                        for j in range(N):
                            check = bool(flag_input_report[i][j]) or check
                        if check:
                            maximum = 0
                            for j in range(N):
                                if str(j) not in matched_output:
                                    if flag_input_report[i][j] == 1:
                                        if c[i][j] > maximum:
                                            maximum = c[i][j]
                                            input_max = i
                                            output_max = j
                            c[input_max][output_max] = c[input_max][output_max] - 1
                            flag_input_report[input_max][output_max] = 0
                            matched_output.append(str(output_max))
                            matched_input.append(str(input_max))
                            total_passed_packet = total_passed_packet + 1
                            packet_leave_each_input_port[input_max] = packet_leave_each_input_port[input_max] + 1
                            print("input " + str(input_max) + " matched " + str(
                                output_max) + " (this matching occur by maximum counter) ")
    delay[T] = time.clock() - start

print("--------------------------------------------")
print("-----------------Evaluation-----------------")
print("--------------------------------------------\n")
# 300 is number of time slots and N is switch size
print("overall throughput is :" + str((total_passed_packet / (300 * N)) * 100) + "%\n")

result = 0
for i in range(300):
    result = delay[i] + result
print("overall delay for switch : " + str(round(result, 3)))
