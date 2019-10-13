import globalV
# Vehicle Class

class Vehicle:
    def __init__(self, x, v, road):
        self.x = 0 # mile position
        self.v = 0 # m/h velocity
        self.a = 0 # m/h^2 acceleration
        self.beta = 250 #h^-1
        self.road = road
        self.leader = 0  #is it the first car?
        self.t = 0

    def updateV(self):
        self.a = self.beta * (self.road.u - self.v)
        self.v = self.v + self.a * (globalV.dt / 3600)

    def stopV(self):
        self.v = 0
        self.a = 0

    def updateX(self):
        self.x = self.x + self.v * (globalV.dt / 3600)

    def stopX(self):
        self.x = self.x
    
    
    
        