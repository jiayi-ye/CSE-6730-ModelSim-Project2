from heapq import *

class EventOrientedSim:
    def __init__(self):
        self.eventQueue = []
        self.timeNow = 0.0
        self.firstEventTime = None
        self.maxTime = 900

    # Given an event object, schedules the event onto a min priority queue
    # Uses event timestamp as priority
    def schedule(self, event):
        if event.ts > self.maxTime:
            return
        heappush(self.eventQueue, (event.ts, event))

    # Pops one event off the min queue. If empty, then return None
    def remove(self):
        if len(self.eventQueue) == 0:
            return None

        return heappop(self.eventQueue)

    # Prints events in the queue
    def printEvents(self):
        for ts, event in self.eventQueue:
            print("Time: {}, Type: {}".format(event.ts, TrafficEventTypes(event.eventType)))

    def runSim(self):
        print("Starting simulation: ")
        # self.printEvents()

        while len(self.eventQueue) > 0:
            # Pop the lowest prioirty
            ts, event = self.remove()

            # If this is the first event, update the first event time
            if self.firstEventTime is None:
                self.firstEventTime = ts

            # Update the timestamp
            self.timeNow = event.ts
            # Use the callback
            event.callback(event.car)

class TrafficEventTypes:
    Enter14, Enter11, Exit10, RedLight14, GreenLight14, RedLight12,\
    GreenLight12, RedLight11, GreenLight11, RedLight10, GreenLight10,\
    Wait14, Wait12, Wait11, Wait10 = range(15)

    def __init__(self, eventType):
        self.value = eventType

    def __str__(self):
        if self.value == TrafficEventTypes.Enter14:
            return 'Enter from 14th Street Event'
        if self.value == TrafficEventTypes.Enter11:
            return 'Enter from 11th Street Event'
        if self.value == TrafficEventTypes.Exit10:
            return 'Exit from 10th Street Event'
        if self.value == TrafficEventTypes.RedLight14:
            return 'Red light at 14th Street'
        if self.value == TrafficEventTypes.GreenLight14:
            return 'Green light at 14th Street'
        if self.value == TrafficEventTypes.RedLight12:
            return 'Red light at 12th Street'
        if self.value == TrafficEventTypes.GreenLight12:
            return 'Green light at 12th Street'
        if self.value == TrafficEventTypes.RedLight11:
            return 'Red light at 11th Street'
        if self.value == TrafficEventTypes.GreenLight11:
            return 'Green light at 11th Street'
        if self.value == TrafficEventTypes.RedLight10:
            return 'Red light at 10th Street'
        if self.value == TrafficEventTypes.GreenLight10:
            return 'Green light at 10th Street'
        if self.value == TrafficEventTypes.Wait14:
            return 'Waiting at 14th Street Intersection'
        if self.value == TrafficEventTypes.Wait12:
            return 'Waiting at 12th Street Intersection'
        if self.value == TrafficEventTypes.Wait11:
            return 'Waiting at 11th Street Intersection'
        if self.value == TrafficEventTypes.Wait10:
            return 'Waiting at 10th Street Intersection'


class Car:
    uniqueID = 0
    def __init__(self):
        self.id = Car.uniqueID
        Car.uniqueID += 1

        self.enterTS = 0
        self.enterEventType = None
        self.exitTS = None

    def __lt__(self, other):
        return self.uniqueID < other.uniqueID

class TrafficLight:
    Red, Green = range(2)

    def __init__(self, lightColor):
        self.value = lightColor

    def __str__(self):
        if self.value == TrafficLight.Red:
            return "red"
        if self.value == TrafficLight.Green:
            return "green"

class EventTypes:
    Enter, Exit, Start, Stop = range(4)

    def __init__(self, eventType):
        self.value = eventType

    def __str__(self):
        if self.value == EventTypes.Enter:
            return 'Enter Event'
        if self.value == EventTypes.Exit:
            return 'Exit Event'
        if self.value == EventTypes.Start:
            return 'Start Event'
        if self.value == EventTypes.Stop:
            return 'Stop Event'


class Event:
    def __init__(self, ts, car, eventType, callback):
        self.ts = ts
        self.car = car
        self.eventType = eventType
        self.callback = callback

    def __str__(self):
        print("Time: {}, Type: {}".format(self.ts, TrafficEventTypes(self.eventType)))

    def __lt__(self, other):
        return self.eventType < other.eventType

