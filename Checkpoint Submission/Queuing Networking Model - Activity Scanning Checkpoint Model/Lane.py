from random import random
from Vehicle import Vehicle
## Lane class

class Lane:
    # def __init__(self, list, length, tl_11, tl_12):
    def __init__(self, list, length):
        self.u = 45.0 # m/hr
        self.jamden = 150.0 #veh/km
        self.jamspacing = 1.0 / self.jamden #km
        self.cars = list
        self.pos = 0
        self.q = 1000.0
        self.length = length
        self.cars_temp = []
        self.t = 0 # total time until it disappeared
        
    # generate cars for the first lane
    def veh_arrival(self):
        car = Vehicle(0, self.u, self)  
        if self.cars != []:
            car.leader = self.cars[-1]
        self.cars.append(car)

    # transfer car from current lane to next lane
    def veh_transfer(self):
        if len(self.cars) > 0:
            for car in self.cars:
                if car.x > self.length:
                    self.cars_temp.append(car)
                    self.cars.remove(car)
                    if len(self.cars) > 0:
                        self.cars[0].leader = None
        return self.cars_temp
    
    # remove temp car in veh_transfer
    def rem_temp(self):
        self.cars_temp =[]

    # set the transfered cars as arrival cars for the next lane
    def veh_transfer_arrival(self, temp_car):
        for car in temp_car:
            car.x = 0
            if self.cars != []:
                car.leader = self.cars[-1]
            self.cars.append(car)

    # remove cars from the last lane
    def veh_remove(self):
        if len(self.cars) > 0:
            for car in self.cars:
                if car.x > self.length:
                    self.cars.remove(car)
                    if len(self.cars) > 0:
                        self.cars[0].leader = None
        return self.cars_temp
    
    # record the time that the cars pass the last segment of the lane
    def record_time(self,t):
        if len(self.cars) > 0:
            for car in self.cars:
                if car.x > self.length:
                    car.t = t
                    self.cars_temp.append(car)
        return self.cars_temp
    
        