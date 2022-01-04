import robot
import matplotlib.pyplot as plt
import numpy as np
import sys

robot = robot.Robot(0.05, 0.2)
step = 0.001
pi = np.pi
t_list = []
vl_list = []
vr_list = []
t_end = 5
a = 0

if len(sys.argv) == 1:
    raise ValueError("You must specify if you want to draw cube or you want to specify vectors by input here")

elif sys.argv[1] == '-c':
    a_input = input("Enter length of side of cube, range is 1 meter to 10 meters, e.g. value 1 to 10: ")
    a_side = float(a_input)
    if 1 > a > 10:
        raise ValueError("You entered length of side of cube outside of range")

    v_straight = 1
    L = robot.L

    vl_list = [1, -1, 1, -1, 1, -1, 1]
    vr_list = [1, 1, 1, 1, 1, 1, 1]

    w_turn = (max(vr_list) + max(vl_list)) / robot.L
    t_turn = (pi / 2) / w_turn
    t_straight = a_side / v_straight
    t_list = [0, t_straight, t_straight + t_turn, t_straight + t_turn + t_straight,
              t_straight + t_turn + t_straight + t_turn, t_straight + t_turn + t_straight + t_turn + t_straight,
              t_straight + t_turn + t_straight + t_turn + t_straight + t_turn]
    t_end = t_straight

    print("Generated time vector: ", t_list)
    print("Generated left wheel vector: ", vl_list)
    print("Generated right wheel vector: ", vr_list)

elif sys.argv[1] == '-s':
    t_list_input = input("Enter a list of time values separated by space: ")
    t_list = [int(s.strip()) for s in t_list_input.split(' ')]
    vl_list_input = input("Enter a list of speed values for left wheel separated by space: ")
    vl_list = [int(s.strip()) for s in vl_list_input.split(' ')]
    vr_list_input = input("Enter a list of speed values for right wheel separated by space: ")
    vr_list = [int(s.strip()) for s in vr_list_input.split(' ')]
    if len(vr_list) != len(vl_list) != len(t_list):
        raise ValueError("You entered vectors with different lengths")

elif sys.argv[1] == '-t':
    R1_input = input("Enter a radius 1: ")
    R1 = float(R1_input)

    R2_input = input("Enter a radius 2: ")
    R2 = float(R2_input)

    L_lin_input = input("Enter a length of linear move: ")
    L_lin = float(L_lin_input)

    v_straight = 1

    t_straight = L_lin / v_straight

    vr = (R1 + robot.L/2) / (R1 - robot.L/2)
    r1_t = ((1/2)*pi*R1) / vr

    vl = (R2 + robot.L/2) / (R2 - robot.L/2)
    r2_t = ((1/2)*pi*R2) / vl

    t_list = [0, t_straight, t_straight + np.abs(r1_t), t_straight + np.abs(r1_t) + t_straight,
              t_straight + np.abs(r1_t) + t_straight + np.abs(r2_t)]
    vl_list = [1, 1, 1, vl, 1]
    vr_list = [1, vr, 1, 1, 1]
    t_end = t_straight

    print("Generated time vector: ", t_list)
    print("Generated left wheel vector: ", vl_list)
    print("Generated right wheel vector: ", vr_list)

else:
    raise ValueError("You must specify if you want to download (-d) or load (-l) file")


num_iter = int((t_list[-1] + t_end) / step)

k = 1
count = 0
robot.vl = vl_list[0]
robot.vr = vr_list[0]

for i in range(1, num_iter):
    if k <= len(t_list) - 1:
        if i >= int(t_list[k] / step):
            robot.vl = vl_list[k]
            robot.vr = vr_list[k]
            k += 1
            count = 0

    robot.run(step)
    count += 1

x = [cord[0] for cord in robot.trajectory_center]
y = [cord[1] for cord in robot.trajectory_center]

x_l = [cord[0] for cord in robot.trajectory_left_wheel]
y_l = [cord[1] for cord in robot.trajectory_left_wheel]

x_r = [cord[0] for cord in robot.trajectory_right_wheel]
y_r = [cord[1] for cord in robot.trajectory_right_wheel]

ax1 = plt.subplot(111)
ax1.plot(x, y)
ax1.plot(x_l, y_l)
ax1.plot(x_r, y_r)

max_left_x = max(x_l)
max_right_x = max(x_r)
max_center_x = max(x)
max_x = max(max_left_x, max_right_x, max_center_x)
max_left_y = max(y_l)
max_right_y = max(y_r)
max_center_y = max(y)
max_y = max(max_left_y, max_right_y, max_center_y)
max_value = max(max_x, max_y)

min_left_x = min(x_l)
min_right_x = min(x_r)
min_center_x = min(x)
min_x = min(min_left_x, min_right_x, min_center_x)
min_left_y = min(y_l)
min_right_y = min(y_r)
min_center_y = min(y)
min_y = min(min_left_y, min_right_y, min_center_y)
min_value = min(min_x, min_y)

ax1.set_xlim([min_x - 1, max_x + 1])
ax1.set_ylim([min_y - 1, max_y + 1])
plt.show()
