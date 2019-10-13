To run the simulation, run eventOrientedTrafficSim.py with python3

The packages needed are as follows:
heapq
numpy
scipy.stats
scipy
(optional) matplotlib.pyplot


engine.py houses the mechanism necessary to run the event oriented simulation
eventOrientedTrafficSim.py houses all the events and event handlers needed to simulate traffic

The main function inside eventOrientedTrafficSim runs 100 iterations
of the traffic sim at high traffic and low traffic by calling runSimMultipleTimesLow()
and runSimMultipleTimesHigh(). Change the isDebug flag inside either of these
methods to see the full debug text output.

After the 200 total iterations complete, the mean wait time is printed for
high and low traffic, along with the 1 sample t-test p value.

I've commented out code that plots the data, so uncomment each plot individually
and the import for matplotlib to see the plots.

Other notable functions:
- runTest(): runs the simulation with isDebug=True, with only two cars. One enters 14th at ts=15
the other enters 11th at ts=200

- runOnce(): runs the simulation with isDebug=True all the way through once using the distributions

- TrafficSimulation's genAllTimingsForLight(...): Generates a full 900 second list of timings
for a given set of light timings. See below for a code example that runs the simulation
once and also generates a traffic light timing list for intersection 14

Example code:
tempSim = TrafficSimulation(isDebug=True)
runOnce()
print(tempSim.genAllTimingsForLight(tempSim.red14Time, tempSim.green14Time))
