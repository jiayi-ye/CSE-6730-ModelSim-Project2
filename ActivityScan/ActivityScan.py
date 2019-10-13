from Lane import Lane
import Vars
import numpy as np
from TrafficLight import TrafficLight
import random
import statistics


def one_simulate():
    # print('works')
    # Initialize Traffic Lights: only consider 2 traffic lights between 14 and 10 street
    tf_12 = TrafficLight()
    tf_11 = TrafficLight()

    # Initialize Road Network
    # we have a lane segment
    ln_14_12 = Lane([], 0.2)  # Lane between 14 and 12: 0.2 mile
    ln_12_11 = Lane([], 0.1)  # Lane between 12 and 11: 0.1 mile
    ln_11_10 = Lane([], 0.1)  # Lane between 11 and 10: 0.1 mile

    # Generate cars at the beginning of the lane (from 14 street)
    # can be low or high
    arr_dist_14 = Vars.car_generation_14_high.copy()

    # Run Simulation
    t = 0

    # Record cars reached the 10th street
    final_cars = [[], []]

    # Record the avg time the cars reached the 10th street
    all_avg_time = [[], []]
    # all_avg_time_ln2 = []
    # start simulation, timestamp is 1
    for t in np.arange(0, Vars.sim_time, 1):
        ####### 14-12 ########
        # Generate cars at the beginning of the lane (14 street)
        if arr_dist_14 != [] and t >= arr_dist_14[0]:
            ln_14_12.veh_arrival(t)
            arr_dist_14.pop(0)

        # update traffic light of intersection 12 and Peachtree
        tf_12.updateLight('12', t)

        # condition 1: traffic light color
        # condition 2: is the car close to the traffic lights?
        # print(len(ln_14_12.cars[0]))
        for ln in ln_14_12.cars:
            for tempVeh in ln:
                dist = ln_14_12.length - tempVeh.x
                dist_condition = (dist <= 0.01 and dist >= 0)
                if tf_12.color == 0 and dist_condition:  # red light && car close to red light in 0.01 mile
                    tempVeh.stopV()
                    tempVeh.stopX()
                else:  # green light
                    tempVeh.updateV()
                    tempVeh.updateX()

        # each time step, move vehicles reach the end of 14_12 to lane 12_11 using transfer_car
        transfer_cars = ln_14_12.veh_transfer()
        # print cars moved from lane 14-12 to lane 12-11
        merge_car_12 = [[], []]  # no car merged from 12th street
        ln_12_11.veh_transfer_arrival(transfer_cars, merge_car_12)
        # remove transfer_car in lane 14-12
        ln_14_12.rem_temp()

        ####### 12-11 ########
        # update traffic light of intersection 11 and Peachtree
        tf_11.updateLight('11', t)

        #condition 1: traffic light color
        #condition 2: is the car close to the traffic lights?
        for ln in ln_12_11.cars:
            for tempVeh in ln:
                dist = ln_12_11.length - tempVeh.x
                dist_condition = (dist <= 0.01 and dist >= 0)
                if tf_11.color == 0 and dist_condition:  # red light && car close to red light in 0.01 mile
                    tempVeh.stopV()
                    tempVeh.stopX()
                else:  # green light
                    tempVeh.updateV()
                    tempVeh.updateX()

        # each time step, move vehicles reach the end of 12_11 to lane 11_10 using transfer_car
        transfer_cars = ln_12_11.veh_transfer()
        # print cars moved from lane 12-11 to lane 11-10
        # merge_car_11 = Vars.car_merge_11  # car merged from 12th street
        merge_car_11 = [[], []]
        ln_11_10.veh_transfer_arrival(transfer_cars, merge_car_11)
        # remove transfer_car in lane 14-12
        ln_12_11.rem_temp()
        # print(len(ln_11_10.cars[0]))

        ####### 11-10 ########
        for ln in ln_11_10.cars:
            for tempVeh in ln:
                tempVeh.updateV()
                tempVeh.updateX()

        # each time step, remove vehicles reach the end of the lane
        transfer_cars = ln_11_10.record_time(t)
        for i in range(2):
            for car in transfer_cars[i]:
                final_cars[i].append(car)
        ln_11_10.veh_remove()

        if (len(final_cars[0]) + len(final_cars[1])) != 0:
            for i in range(2):
                ln_len = len(final_cars[i])
                if ln_len != 0:
                    t_sum = 0
                    for car in final_cars[i]:
                        t_sum += (car.t - car.start_t)
                    all_avg_time[i].append(t_sum / ln_len)
    return all_avg_time
