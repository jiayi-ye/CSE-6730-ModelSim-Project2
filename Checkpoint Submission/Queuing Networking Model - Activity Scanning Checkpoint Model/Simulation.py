from Lane import Lane
import globalV    # global variables
import numpy as np

# Initialize Road Network
# we have a lane segment with 1km length
ln = Lane([], 1)

# Run Simulation
for t in np.arange(0, globalV.sim_time, globalV.dt):
    # each time step, generate cars at the beginning of the lane
    ln.veh_arrival(ln.q, globalV.dt)

    # update all vehicles' speed and location on each lane
    for tempVeh in ln.cars:
        tempVeh.updateV()
        tempVeh.updateX()

    # each time step, remove vehicles reach the end of the lane
    ln.veh_transfer()

    # print('number of vehs', len(ln.cars), 'at time', t)
    if len(ln.cars) > 0:
        print('position of first car', ln.cars[0].x)
        print('velocity of first car', ln.cars[0].v)
    #print(t)

