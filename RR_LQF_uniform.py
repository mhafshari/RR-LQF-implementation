###################################


# written by @mhafshari
# simulating bursty traffic on switches and routers
# RR/LQF algorithm implementation with any iteration and speedUp with uniform traffic

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
packet_arrive_each_input_port = [0] * N
packet_leave_each_input_port = [0] * N
matched_output = []
matched_input = []
delay = [0] * 300
for T in range(300):
    start = time.clock()
    flag_output_report = [[0] * N for i in range(N)]
    # report
    print("request input->output")
    # producing uniform traffic based on p (load probability) and N (switch size)
    if T % 10 == 0:
        send_time_slot = [[0] * 10 for i in range(N)]
        for u in range(N):
            send_time_slot[u] = random.sample(range(0, 10), int(p * 10))
            if 0 in send_time_slot[u]:
                j = random.randrange(1, N, 1)
                flag_output_report[u][j] = 1
                total_arrived_packet = total_arrived_packet + 1
                packet_arrive_each_input_port[u] = packet_arrive_each_input_port[u] + 1
                print(str(u) + "->" + str(j))
    else:
        for u in range(N):
            if T % 10 in send_time_slot[u]:
                j = random.randrange(1, N, 1)
                flag_output_report[u][j] = 1
                total_arrived_packet = total_arrived_packet + 1
                packet_arrive_each_input_port[u] = packet_arrive_each_input_port[u] + 1
                print(str(u) + "->" + str(j))
                # single bit reporting
                # flag_output_report[i][j] = 1

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

                            # print("counter is " + str(c))
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
