from random import random
import Vars


class TrafficLight:
    def __init__(self):
        self.color = 1  #0 for Red, 1 for Green

    def updateLight(self, intersection, time_now):
        if intersection == '12':
            # follow green, red, green, red, ..........
            traffic_change = [
                0, 61.4, 99.3, 160.7, 198.6, 260.0, 297.9, 359.29999999999995,
                397.19999999999993, 458.5999999999999, 496.4999999999999,
                557.8999999999999, 595.7999999999998, 657.1999999999998,
                695.0999999999998, 756.4999999999998, 794.3999999999997,
                855.7999999999997, 893.6999999999997
            ]
            if time_now >= traffic_change[0]:
                self.color = 1 - self.color  #alternate traffic light
                traffic_change.pop(0)

        else:
            # follow green, red, green, red, ..........
            traffic_change = [
                0, 41.5, 100.1, 141.6, 200.2, 241.7, 300.3, 341.8,
                400.40000000000003, 441.90000000000003, 500.50000000000006,
                542.0, 600.6, 642.1, 700.7, 742.2, 800.8000000000001
            ]
            if time_now >= traffic_change[0]:
                self.color = 1 - self.color  #alternate traffic light
                traffic_change.pop(0)
