from heapq import *


class EventOrientedSim:
    def __init__(self):
        self.eventQueue = []
        self.timeNow = 0.0
        self.firstEventTime = None

    # Given an event object, schedules the event onto a min priority queue
    # Uses event timestamp as priority
    def schedule(self, event):
        heappush(self.eventQueue, (event.ts, event))

    # Pops one event off the min queue. If empty, then return None
    def remove(self):
        if len(self.eventQueue) == 0:
            return None

        return heappop(self.eventQueue)

    # Prints events in the queue
    def printEvents(self):
        for ts, event in self.eventQueue:
            print("Time: {}, Type: {}".format(event.ts, event.eventType))

    def runSim(self):
        print("Starting simulation: ")
        self.printEvents()

        while len(self.eventQueue) > 0:
            # Pop the lowest prioirty
            ts, event = self.remove()

            # If this is the first event, update the first event time
            if self.firstEventTime is None:
                self.firstEventTime = ts

            # Update the timestamp
            self.timeNow = event.ts
            # Use the callback
            event.callback()


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
    def __init__(self, ts, eventType, callback):
        self.ts = ts
        self.eventType = eventType
        self.callback = callback
