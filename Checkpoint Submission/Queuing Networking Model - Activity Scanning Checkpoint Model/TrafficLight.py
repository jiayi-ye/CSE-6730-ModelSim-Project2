from random import random
import globalV

class TrafficLight:
    def __init__(self):
        self.color = 1  #0 for Red, 1 for Green

    def updateLight(self):
        self.color = 1 - self.color  #alternate traffic light
        # print(self.color)
