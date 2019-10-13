from random import random
from Vehicle import Vehicle
import numpy as np
import Vars


## Lane class
class Lane:
    # def __init__(self, list, length, tl_11, tl_12):
    def __init__(self, list, length):
        self.u = 35.0  # speed limit mph
        self.jamden = 20.0  #veh/m
        self.jamspacing = 1.0 / self.jamden  #m
        self.cars = [[], []]  # 1st for left lane, 2nd for right lane
        self.pos = 0
        self.length = length
        self.cars_temp = [[], []]
        self.cars_next = [[], []]
        self.t = 0  # total time until it disappeared

    # generate cars for the first lane
    def veh_arrival(self, t):
        car = Vehicle(0, self.u, self, t)
        prob = np.random.rand()
        if prob < 0.5:  # left lane
            if self.cars[0] != []:
                car.leader = self.cars[0][-1]
            self.cars[0].append(car)
        else:
            if self.cars[1] != []:
                car.leader = self.cars[1][-1]
            self.cars[1].append(car)

    # transfer car from current lane to next lane
    def veh_transfer(self):
        # print(len(self.cars))
        for i in range(len(self.cars)):
            if len(self.cars[i]) > 0:
                for car in self.cars[i]:
                    if car.x >= self.length:
                        prob_next = np.random.rand()
                        if prob_next < Vars.prob_straight:
                            self.cars_temp[i].append(car)
                            car.x = 0
                            # self.cars_next[i].append(car)
                            # if self.cars_next[i] != []:
                            #     car.leader = self.cars[-1]
                            # self.cars_temp[i].append(car)
                            self.cars[i].remove(car)
                            # if len(self.cars[i]) > 0:
                            #     self.cars[i][0].leader = None
        return self.cars_temp

    # set the transfered cars as arrival cars for the next lane
    def veh_transfer_arrival(self, temp_car, merge_car):
        for i in range(len(temp_car)):
            for car in temp_car[i]:
                car.x = 0
                # if self.cars != []:
                #     car.leader = self.cars[-1]
                self.cars[i].append(car)
            if merge_car[i] != 0:  ## append merged cars if exist
                for car in merge_car[i]:
                    car.x = 0
                    self.cars[i].append(car)

    # remove temp car in veh_transfer
    def rem_temp(self):
        self.cars_temp = [[], []]

    # record the time that the cars pass the last segment of the lane
    def record_time(self, t):
        self.cars_temp = [[], []]
        for i in range(2):
            if len(self.cars[i]) > 0:
                for car in self.cars[i]:
                    if car.x > self.length:
                        car.t = t
                        self.cars_temp[i].append(car)
        return self.cars_temp

    # remove cars from the last lane
    def veh_remove(self):
        for i in range(len(self.cars)):
            if len(self.cars[i]) > 0:
                for car in self.cars[i]:
                    if car.x > self.length:
                        self.cars[i].remove(car)
