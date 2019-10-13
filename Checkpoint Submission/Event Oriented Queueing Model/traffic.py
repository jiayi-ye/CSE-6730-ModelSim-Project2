import random
from engine import *

class TrafficSimulation(EventOrientedSim):
    def __init__(self):
        super().__init__()
        random.seed(1234)

        ### Global Information
        # Average time for car entering the road
        self.meanEnter = 60
        # On Peachtree Street between 10th and 14th in feet - @20mph, 54 sec
        self.totalDistance = 1584

        ### Execution Vars
        self.numEvents = 0

        ### Simulation constants
        # Debug flag
        self.isDebug = True
        # How many cars can enter?
        self.CARS_LIMIT = 5
        # Car speed in mph
        self.carSpeed = 20
        # Using car speed and total distance to calculate expected time
        self.expectedTime = (self.totalDistance / (5280 * self.carSpeed)) * 3600

        ### Simulation State Variables
        self.carsEntered = 0
        self.carsOnRoad = 0
        self.totalTravelTime = 0.0

    ### Event Handlers
    def enter(self):
        self.numEvents += 1
        self.carsOnRoad += 1
        self.carsEntered += 1

        if self.isDebug:
            print("Car Entered: time = {}".format(self.timeNow))

        # Schedule another arrival if this isn't the last car to arrive
        if self.carsEntered < self.CARS_LIMIT:
            ts = self.timeNow + random.randint(0, self.meanEnter)
            next_enter_event = Event(ts, EventTypes.Enter, self.enter)
            self.schedule(next_enter_event)

        # Currently schedule a set time to schedule the car leaving
        # TODO: Figure out how to represent a car in the simulation that's not hardcoded

        exit_ts = self.timeNow + random.randint(self.expectedTime - 10, self.expectedTime + 10)
        exit_event = Event(exit_ts, EventTypes.Exit, self.exit)
        self.schedule(exit_event)

    def exit(self):
        self.numEvents += 1
        self.carsOnRoad -= 1

        if self.isDebug:
            print("Car Exited: time = {}".format(self.timeNow))

    def start(self):
        self.numEvents += 1
        pass

    def stop(self):
        self.numEvents += 1
        pass

    # Returns the time since the first event!
    def totalUsedTime(self):
        return self.timeNow - self.firstEventTime


if __name__ == '__main__':
    trafficSim = TrafficSimulation()

    ts = random.randint(0, trafficSim.meanEnter)
    enter_event = Event(ts, EventTypes.Enter, trafficSim.enter)
    trafficSim.schedule(enter_event)

    print("Starting traffic simulation")
    trafficSim.runSim()
    print("Ended traffic simulation")

    avgWait = float(trafficSim.totalUsedTime()) / float(trafficSim.carsEntered)
    print("Average Wait time: {}".format(avgWait))
