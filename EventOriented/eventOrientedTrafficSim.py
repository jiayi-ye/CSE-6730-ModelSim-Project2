import random
import numpy as np
import scipy.stats as ss
import scipy as sp

from engine import *

class TrafficSimulation(EventOrientedSim):
    def __init__(self, maxTime=900, isDebug=True):
        super().__init__()
        random.seed(1234)
        self.maxTime = maxTime

        ### Global Information
        # Average time for car entering the road
        self.meanEnter = 60
        # On Peachtree Street between 10th and 14th in feet - @20mph, 54 sec
        self.totalDistance = 1584

        ### Execution Vars
        self.numEvents = 0

        ### Simulation constants
        # Debug flag
        self.isDebug = isDebug
        # Car speed in mph
        self.carSpeedMPH = 35.0
        self.carSpeedFPS = 51.33
        # Using car speed and total distance to calculate expected time
        self.expectedTime = (self.totalDistance / (5280 * self.carSpeedMPH)) * 3600
        self.maxCarsPerLight = 500

        ### Simulation State Variables
        self.carsEntered = 0
        self.carsExited = 0
        self.carsOnRoad = 0
        self.totalTravelTime = 0.0

        ### Traffic Light Variables
        self.light14 = TrafficLight.Green
        self.light12 = TrafficLight.Green
        self.light11 = TrafficLight.Green
        self.light10 = TrafficLight.Green

        self.red14Time = 49
        self.green14Time = 37
        self.red12Time = 53
        self.green12Time = 61
        self.red11Time = 59
        self.green11Time = 42
        self.red10Time = 53
        self.green10Time = 34

        ### Cars at each intersection
        self.cars14 = []
        self.cars12 = []
        self.cars11 = []
        self.cars10 = []

        ### Location of each light
        self.light14Loc = 0
        self.light12Loc = 1056
        self.light11Loc = 1584
        self.light10Loc = 2100

    ### Event Handlers
    def enter14(self, car):
        if self.isDebug:
            print("{}: = {}".format(TrafficEventTypes(TrafficEventTypes.Enter14), self.timeNow))

        nextTS = self.timeNow
        nextEvent = Event(nextTS, car, TrafficEventTypes.Wait14, self.wait14)
        self.schedule(nextEvent)
        pass

    def enter11(self, car):
        if self.isDebug:
            print("{}: = {}".format(TrafficEventTypes(TrafficEventTypes.Enter11), self.timeNow))

        nextTS = self.timeNow
        nextEvent = Event(nextTS, car, TrafficEventTypes.Wait11, self.wait11)
        self.schedule(nextEvent)
        pass

    def exit10(self, car):
        if car.enterEventType == TrafficEventTypes.Enter14:
            self.carsExited += 1
            self.totalTravelTime += self.timeNow - car.enterTS
        pass

    def red_light14(self, car):
        if self.isDebug:
            print("{}: = {}".format(TrafficEventTypes(TrafficEventTypes.RedLight14), self.timeNow))

        nextTS = self.timeNow + self.red14Time
        nextEvent = Event(nextTS, None, TrafficEventTypes.GreenLight14, self.green_light14)
        self.schedule(nextEvent)
        pass

    def green_light14(self, car):
        greenType = TrafficEventTypes.GreenLight14
        carsAtLight = self.cars14
        nextWaitType = TrafficEventTypes.Wait12
        nextWaitHandler = self.wait12
        nextRedType = TrafficEventTypes.RedLight14
        nextRedHandler = self.red_light14
        self.greenLightGeneric(greenType, self.green14Time, carsAtLight, nextWaitType, nextWaitHandler, nextRedType, nextRedHandler)
        # self.greenLightGeneric(car, greenType, self.green14Time, carsAtLight, TrafficEventTypes.Exit10, self.exit10, nextRedType, nextRedHandler)

        # if self.isDebug:
        #     print("Green light 14th: time = {}".format(self.timeNow))
        #
        # # keeps track of last index deleted
        # maxIndex = 0
        # for i, car in enumerate(self.cars14):
        #     if i == self.maxCarsPerLight:
        #         break
        #
        #     maxIndex = i
        #     nextTS = self.timeNow
        #     nextEvent = Event(nextTS, TrafficEventTypes.Wait11, self.wait11)
        #     self.schedule(nextEvent)
        #     if self.isDebug:
        #         print("Car moved to 11th: time = {}".format(self.timeNow))
        #
        # del self.cars14[0:maxIndex + 1]
        #
        # nextTS = self.timeNow + self.greenLightTime
        # nextEvent = Event(nextTS, TrafficEventTypes.RedLight14, self.red_light14)
        # self.schedule(nextEvent)
        # pass

    def red_light12(self, car):
        if self.isDebug:
            print("{}: = {}".format(TrafficEventTypes(TrafficEventTypes.RedLight12), self.timeNow))

        nextTS = self.timeNow + self.red12Time
        nextEvent = Event(nextTS, None, TrafficEventTypes.GreenLight12, self.green_light12)
        self.schedule(nextEvent)
        pass

    def green_light12(self, car):
        greenType = TrafficEventTypes.GreenLight12
        carsAtLight = self.cars12
        nextWaitType = TrafficEventTypes.Wait11
        nextWaitHandler = self.wait11
        nextRedType = TrafficEventTypes.RedLight12
        nextRedHandler = self.red_light12
        self.greenLightGeneric(greenType, self.green12Time, carsAtLight, nextWaitType, nextWaitHandler, nextRedType, nextRedHandler)
        pass

    def red_light11(self, car):
        if self.isDebug:
            print("{}: = {}".format(TrafficEventTypes(TrafficEventTypes.RedLight11), self.timeNow))

        nextTS = self.timeNow + self.red11Time
        nextEvent = Event(nextTS, None, TrafficEventTypes.GreenLight11, self.green_light11)
        self.schedule(nextEvent)
        pass

    def green_light11(self, car):
        greenType = TrafficEventTypes.GreenLight11
        carsAtLight = self.cars11
        nextWaitType = TrafficEventTypes.Wait10
        nextWaitHandler = self.wait10
        nextRedType = TrafficEventTypes.RedLight11
        nextRedHandler = self.red_light11
        self.greenLightGeneric(greenType, self.green11Time, carsAtLight, nextWaitType, nextWaitHandler, nextRedType, nextRedHandler)
        pass

    def red_light10(self, car):
        if self.isDebug:
            print("{}: = {}".format(TrafficEventTypes(TrafficEventTypes.RedLight10), self.timeNow))

        nextTS = self.timeNow + self.red10Time
        nextEvent = Event(nextTS, None, TrafficEventTypes.GreenLight10, self.green_light10)
        self.schedule(nextEvent)
        pass

    def green_light10(self, car):
        greenType = TrafficEventTypes.GreenLight10
        carsAtLight = self.cars10
        nextWaitType = TrafficEventTypes.Exit10
        nextWaitHandler = self.exit10
        nextRedType = TrafficEventTypes.RedLight10
        nextRedHandler = self.red_light10
        self.greenLightGeneric(greenType, self.green10Time, carsAtLight, nextWaitType, nextWaitHandler, nextRedType, nextRedHandler)
        pass

    def wait14(self, car):
        if self.isDebug:
            print("Car waiting at 14th: time = {}".format(self.timeNow))

        heappush(self.cars14, (self.timeNow, car))
        pass

    def wait12(self, car):
        if self.isDebug:
            print("Car waiting at 12th: time = {}".format(self.timeNow))

        heappush(self.cars12, (self.timeNow, car))
        pass

    def wait11(self, car):
        if self.isDebug:
            print("Car waiting at 11th: time = {}".format(self.timeNow))

        heappush(self.cars11, (self.timeNow, car))
        pass

    def wait10(self, car):
        if self.isDebug:
            print("Car waiting at 10th: time = {}".format(self.timeNow))

        heappush(self.cars10, (self.timeNow, car))
        pass

    def greenLightGeneric(self, greenType, greenLightTime, carsAtLight, nextWaitType, nextWaitHandler, nextRedType, nextRedHandler):
        if self.isDebug:
            print("{}: time = {}".format(TrafficEventTypes(greenType), self.timeNow))

        # keeps track of last index deleted
        maxIndex = 0
        for i, carData in enumerate(carsAtLight):
            carTS, car = carData
            if i == self.maxCarsPerLight:
                break

            maxIndex = i
            nextTS = self.timeNow
            # Calculate whether the car can make it past the next light as well
            calcNextWaitType = self.getNextWaitType(greenType)
            calcNextWaitHandler = self.getHandlerForType(calcNextWaitType)
            nextEvent = Event(nextTS, car, calcNextWaitType, calcNextWaitHandler)
            self.schedule(nextEvent)
            if self.isDebug:
                print("Car moved to {}: time = {}".format(TrafficEventTypes(nextWaitType), self.timeNow))

        del carsAtLight[0:maxIndex + 1]

        nextTS = self.timeNow + greenLightTime
        nextEvent = Event(nextTS, None, nextRedType, nextRedHandler)
        self.schedule(nextEvent)
        pass


    # Using the current light type, and the current time, check if the car can make it to the next location
    def getNextWaitType(self, currentLightType):
        if currentLightType == TrafficEventTypes.GreenLight14:
            # check light at 12, if it can make it send it past
            return TrafficEventTypes.Wait12
        elif currentLightType == TrafficEventTypes.GreenLight12:
            return TrafficEventTypes.Wait11
        elif currentLightType == TrafficEventTypes.GreenLight11:
            return TrafficEventTypes.Wait10
        else:
            # last case, currentLightType == TrafficEventTypes.GreenLight10:
            return TrafficEventTypes.Exit10

    def getHandlerForType(self, type):
        eventHandlerDict = {
            TrafficEventTypes.Wait14: self.wait14,
            TrafficEventTypes.Wait12: self.wait12,
            TrafficEventTypes.Wait11: self.wait11,
            TrafficEventTypes.Wait10: self.wait10,
            TrafficEventTypes.GreenLight14: self.green_light14,
            TrafficEventTypes.GreenLight12: self.green_light12,
            TrafficEventTypes.GreenLight11: self.green_light11,
            TrafficEventTypes.GreenLight10: self.green_light10,
            TrafficEventTypes.RedLight14: self.red_light14,
            TrafficEventTypes.RedLight12: self.red_light12,
            TrafficEventTypes.RedLight11: self.red_light11,
            TrafficEventTypes.RedLight10: self.red_light10,
            TrafficEventTypes.Enter14: self.enter14,
            TrafficEventTypes.Enter11: self.enter11,
            TrafficEventTypes.Exit10: self.exit10,
        }

        return eventHandlerDict[type]


    def genCarsEnter14High(self):
        return self.genCarsEnter14(1.0)

    def genCarsEnter14Low(self):
        return self.genCarsEnter14(2.0)

    # Higher ratio = longer time between cars
    def genCarsEnter14(self, ratio):
        lognorm_dist = sp.stats.lognorm
        car_14 = [0]
        next_time = 0
        while next_time <= 900:
            # Will's distribution - Only cars that pass all the way through, average 85 cars over 100 runs of 900sec
            # r = lognorm_dist.rvs(1.235172097023483, loc=0.37297021138469266, scale=4.820377381126887)
            # Jiayi's distribution - Cars that are ever in the section 5
            r = lognorm_dist.rvs(1.123494632217069, loc=-0.1308024415404237, scale=2.222162369513514)

            next_time = car_14[-1] + r * ratio
            if next_time <= 900:
                car_14.append(next_time)

        if self.isDebug:
            print('num of cars generated from 14th:', len(car_14), '\n')
            print(car_14)

        return car_14

    def genCarsEnter11High(self):
        return self.genCarsEnter11(1.0)

    def genCarsEnter11Low(self):
        return self.genCarsEnter11(2.0)

    # Higher ratio = longer time between cars
    def genCarsEnter11(self, ratio):
        lognorm_dist = sp.stats.lognorm
        car_11 = [0]
        next_time = 0
        while next_time <= 900:
            r = lognorm_dist.rvs(1.5234191072345973, loc=1.9716462121837928, scale=7.605110207945611)

            next_time = car_11[-1] + r * ratio
            if next_time <= 900:
                car_11.append(next_time)

        if self.isDebug:
            print('num of cars generated from 11th:', len(car_11), '\n')
            print(car_11)

        return car_11

    # generates all the signal times for green/red lights given red interval and green interval times
    # Assumes lights start as green. All even index is green, odd is red. All end on red light
    def genAllTimingsForLight(self, redTime, greenTime):
        tempTime = 0
        allTimes = []
        count = 0
        while tempTime < self.maxTime:
            if count == 0:
                allTimes.append(tempTime)
            elif count % 2 == 1:
                tempTime += greenTime
                allTimes.append(tempTime)
            elif count % 2 == 0:
                tempTime += redTime
                allTimes.append(tempTime)

            count += 1

        if count % 2 == 1:
            tempTime += greenTime
            allTimes.append(tempTime)

        return allTimes


    def setupSimulation(self):
        green14 = Event(0, None, TrafficEventTypes.GreenLight14, self.green_light14)
        green12 = Event(0, None, TrafficEventTypes.GreenLight12, self.green_light12)
        green11 = Event(0, None, TrafficEventTypes.GreenLight11, self.green_light11)
        green10 = Event(0, None, TrafficEventTypes.GreenLight10, self.green_light10)
        self.schedule(green14)
        self.schedule(green12)
        self.schedule(green11)
        self.schedule(green10)
        pass


def avgNumCarsGen():
    trafficSim = TrafficSimulation(isDebug=False)

    totalLen14 = 0
    totalLen11 = 0
    for _ in range(0, 100):
        car_enter_14 = trafficSim.genCarsEnter14High()
        car_enter_11 = trafficSim.genCarsEnter11High()

        totalLen14 += len(car_enter_14)
        totalLen11 += len(car_enter_11)

    print("AVG cars gen 14", totalLen14 / 100)
    print("AVG cars gen 11", totalLen11 / 100)


def runSimMultipleTimesHigh(iterations):
    avgWaits = [0] * iterations

    for i in range(iterations):
        trafficSim = TrafficSimulation(maxTime=900, isDebug=False)
        trafficSim.setupSimulation()

        # Sample each entering distribution over 900 seconds, scheduling an entering event at each time step
        for carTS in trafficSim.genCarsEnter14High():
            testCar = Car()
            testCar.enterTS = carTS
            testCar.enterEventType = TrafficEventTypes.Enter14
            testEnter = Event(carTS, testCar, TrafficEventTypes.Enter14, trafficSim.enter14)
            trafficSim.schedule(testEnter)

        for carTS in trafficSim.genCarsEnter11High():
            testCar = Car()
            testCar.enterTS = carTS
            testCar.enterEventType = TrafficEventTypes.Enter11
            testEnter = Event(carTS, testCar, TrafficEventTypes.Enter11, trafficSim.enter11)
            trafficSim.schedule(testEnter)

        print("Starting traffic simulation run {}:".format(i))
        trafficSim.runSim()
        print("Ended traffic simulation run {}".format(i))

        avgWaits[i] = float(trafficSim.totalTravelTime) / float(trafficSim.carsExited)

    return avgWaits


def runSimMultipleTimesLow(iterations):
    avgWaits = [0] * iterations

    for i in range(iterations):
        trafficSim = TrafficSimulation(maxTime=900, isDebug=False)
        trafficSim.setupSimulation()

        # Sample each entering distribution over 900 seconds, scheduling an entering event at each time step
        for carTS in trafficSim.genCarsEnter14Low():
            testCar = Car()
            testCar.enterTS = carTS
            testCar.enterEventType = TrafficEventTypes.Enter14
            testEnter = Event(carTS, testCar, TrafficEventTypes.Enter14, trafficSim.enter14)
            trafficSim.schedule(testEnter)

        for carTS in trafficSim.genCarsEnter11Low():
            testCar = Car()
            testCar.enterTS = carTS
            testCar.enterEventType = TrafficEventTypes.Enter11
            testEnter = Event(carTS, testCar, TrafficEventTypes.Enter11, trafficSim.enter11)
            trafficSim.schedule(testEnter)

        print("Starting traffic simulation run {}:".format(i))
        trafficSim.runSim()
        print("Ended traffic simulation run {}".format(i))

        avgWaits[i] = float(trafficSim.totalTravelTime) / float(trafficSim.carsExited)

    return avgWaits

def runOnce():
    trafficSim = TrafficSimulation(maxTime=900, isDebug=True)
    trafficSim.setupSimulation()

    # avgNumCarsGen()

    # Sample each entering distribution over 900 seconds, scheduling an entering event at each time step
    for carTS in trafficSim.genCarsEnter14High():
        testCar = Car()
        testCar.enterTS = carTS
        testCar.enterEventType = TrafficEventTypes.Enter14
        testEnter = Event(carTS, testCar, TrafficEventTypes.Enter14, trafficSim.enter14)
        trafficSim.schedule(testEnter)

    for carTS in trafficSim.genCarsEnter11High():
        testCar = Car()
        testCar.enterTS = carTS
        testCar.enterEventType = TrafficEventTypes.Enter11
        testEnter = Event(carTS, testCar, TrafficEventTypes.Enter11, trafficSim.enter11)
        trafficSim.schedule(testEnter)

    print("Starting traffic simulation")
    trafficSim.runSim()
    print("Ended traffic simulation")

    avgWait = float(trafficSim.totalTravelTime) / float(trafficSim.carsExited)
    print("Average Wait time: {}".format(avgWait))

def runTest():
    trafficSim = TrafficSimulation(maxTime=900, isDebug=True)
    trafficSim.setupSimulation()

    carTS = 15
    testCar = Car()
    testCar.enterTS = carTS
    testCar.enterEventType = TrafficEventTypes.Enter14
    testEnter = Event(carTS, testCar, TrafficEventTypes.Enter14, trafficSim.enter14)
    trafficSim.schedule(testEnter)

    carTS = 200
    testCar = Car()
    testCar.enterTS = carTS
    testCar.enterEventType = TrafficEventTypes.Enter11
    testEnter = Event(carTS, testCar, TrafficEventTypes.Enter11, trafficSim.enter11)
    trafficSim.schedule(testEnter)

    print("Starting traffic simulation")
    trafficSim.runSim()
    print("Ended traffic simulation")

    avgWait = float(trafficSim.totalTravelTime) / float(trafficSim.carsExited)
    print("Average Wait time: {}".format(avgWait))


def mean_confidence_interval(data, confidence=0.99):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), ss.sem(a)
    h = se * ss.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

if __name__ == '__main__':

    # First make the two probability distributions for each entering point
    sp.random.seed(1234)

    highWaits = runSimMultipleTimesHigh(100)
    print(highWaits)
    high_ci = mean_confidence_interval(highWaits)
    print(high_ci)

    lowWaits = runSimMultipleTimesLow(200)
    print(lowWaits)
    low_ci = mean_confidence_interval(lowWaits)
    print(low_ci)

    # import matplotlib.pyplot as plt

    ### PLOT 1
    # plt.ylabel('Frequency')
    # plt.xlabel('Simulation Run Time (sec)')
    # plt.title('High Traffic Event-Oriented Simulation')
    # plt.hist(highWaits, bins=20)
    # plt.axvline(high_ci[1], color='k', linestyle='dashed', linewidth=1)
    # plt.axvline(high_ci[2], color='k', linestyle='dashed', linewidth=1)
    # plt.show()

    ### PLOT 2
    # plt.ylabel('Frequency')
    # plt.xlabel('Simulation Run Time (sec)')
    # plt.title('Low Traffic Event-Oriented Simulation')
    # plt.hist(lowWaits, bins=20)
    # plt.axvline(low_ci[1], color='k', linestyle='dashed', linewidth=1)
    # plt.axvline(low_ci[2], color='k', linestyle='dashed', linewidth=1)
    # plt.show()

    ### PLOT 3
    # plt.xlabel('Iteration')
    # plt.ylabel('Simulation Run Time (sec)')
    # plt.title('High vs Low Traffic Event-Oriented Simulation')
    # plt.plot(highWaits)
    # plt.plot(lowWaits)
    # plt.legend(["High Traffic Wait", "Low Traffic Wait"])
    # plt.show()

    high_meanWait = sum(highWaits) / float(len(highWaits))
    ttest1_samp_res = ss.ttest_1samp(a=highWaits, popmean=high_meanWait)
    print("High ttest1_samp_res", ttest1_samp_res)
    print("High mean wait", high_meanWait)

    low_meanWait = sum(lowWaits) / float(len(lowWaits))
    ttest1_samp_res = ss.ttest_1samp(a=lowWaits, popmean=low_meanWait)
    print("Low ttest1_samp_res", ttest1_samp_res)
    print("Low mean wait", low_meanWait)

    # tempSim = TrafficSimulation(isDebug=False)
    # runOnce()
    # print(tempSim.genAllTimingsForLight(tempSim.red14Time, tempSim.green14Time))

    # runTest()

    pass
