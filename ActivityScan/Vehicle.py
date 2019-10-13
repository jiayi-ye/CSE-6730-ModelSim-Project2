import Vars
# Vehicle Class


class Vehicle:
    def __init__(self, x, v, road, t):
        self.x = 0  # mile position
        self.v = 0  # mph velocity
        self.a = 0  # mph^2 acceleration
        self.beta = 100  #h^-1 100 for high traffic, 90 for low traffic
        self.road = road
        self.leader = 0  #is it the first car?
        self.t = 0
        self.start_t = t

    def updateV(self):
        self.a = self.beta * (self.road.u - self.v)
        self.v = self.v + self.a * (Vars.dt / 3600)
        # print(self.v)

    def stopV(self):
        self.v = 0
        self.a = 0

    def updateX(self):
        self.x = self.x + self.v * (Vars.dt / 3600)

    def stopX(self):
        self.x = self.x
