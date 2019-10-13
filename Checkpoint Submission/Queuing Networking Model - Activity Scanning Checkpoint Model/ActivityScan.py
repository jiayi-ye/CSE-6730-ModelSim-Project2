from Lane import Lane
import globalV    # global variables
import numpy as np
from TrafficLight import TrafficLight
import random


# Initialize Traffic Lights: only consider 2 traffic lights between 10 and 14 street
tf_11 = TrafficLight()
tf_12 = TrafficLight()

# Initialize Road Network
# we have a lane segment with 1mile length
ln_10 = Lane([], 1)
ln_11 = Lane([], 1)
ln_12 = Lane([], 1)

# Generate cars at the beginning of the lane (from 10 to 11 street) every 3s
# ran_interval = random.randint(4, 10)
# print(ran_interval)
arr_dist = list(np.arange(3,globalV.sim_time,3))

# repeat sim for 4 times

# for i in range(1, 10):
# Run Simulation
t = 0
# Record cars passed the 14th street
final_cars = []

for t in np.arange(0, globalV.sim_time, globalV.dt):
    # Generate cars at the beginning of the lane (from 10 to 11 street) every 3s
    if arr_dist != [] and t >= arr_dist[0]:
        ln_10.veh_arrival()
        arr_dist.pop(0)

    # update traffic light every 10s on tf 11
    if round(t % 20, 1) == 0.0: #change light every 20s 
        tf_11.updateLight()
    
    # condition 1: traffic light color
    # condition 2: is the car close to the traffic lights?
    for tempVeh in ln_10.cars:
        dist = ln_10.length - tempVeh.x
        dist_condition = (dist<=0.1 and dist >=0)
        if tf_11.color == 0 and dist_condition :  # red light && car close to red light in 10m
            tempVeh.stopV()
            tempVeh.stopX()
        else:  # green light
            tempVeh.updateV()
            tempVeh.updateX()

    # each time step, move vehicles reach the end of lane 10 to lane 11 using transfer_car
    transfer_cars = ln_10.veh_transfer()
    # print cars moved from lane 10 to lane 11
    # print(transfer_cars)
    ln_11.veh_transfer_arrival(transfer_cars)
    # remove transfer_car in lane 10
    ln_10.rem_temp()

    # update traffic light every 10s on tf 12
    if round(t % 30, 1) == 0.0: #change light every 30s 
        tf_12.updateLight()

    #condition 1: traffic light color
    #condition 2: is the car close to the traffic lights?
    for tempVeh in ln_11.cars:
        dist = ln_11.length - tempVeh.x
        dist_condition = (dist < 0.1 and dist >= 0)
        if tf_12.color == 0 and dist_condition :  # red light && car close to red light in 10m
            tempVeh.stopV()
            tempVeh.stopX()
            
        else:  # green light
            tempVeh.updateV()
            tempVeh.updateX()

    # each time step, move vehicles reach the end of lane 11 to lane 12 using transfer_car
    transfer_cars = ln_11.veh_transfer()
    # print cars moved from lane 11 to lane 12
    ln_12.veh_transfer_arrival(transfer_cars)
    # remove transfer_car in lane 11
    ln_11.rem_temp()

    # lane 12 st-14 st
    for tempVeh in ln_12.cars:
        tempVeh.updateV()
        tempVeh.updateX()

    # each time step, remove vehicles reach the end of the lane
    transfer_cars = ln_12.record_time(t)
    # print(t, len(transfer_cars))
    for i in transfer_cars:
        final_cars.append(i)
    ln_12.rem_temp()

# print(len(final_cars))
if len(final_cars) > 0:
    v_sum = 0
    for car in final_cars:
        v_sum += 3 / (car.t / 3600)           
# print the average speed of the cars which passes the whole 3 segments of lanes
    # print(len(final_cars))
    print('avg velocity', v_sum/len(final_cars))