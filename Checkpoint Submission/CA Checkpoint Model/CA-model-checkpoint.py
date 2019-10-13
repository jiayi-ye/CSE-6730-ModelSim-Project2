import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

unoccupied = 0
occupied = 1

ROAD_SIZE = (50, 2)

def init_road_vels():
    R = np.zeros(ROAD_SIZE)
    V = np.full(ROAD_SIZE, -1)
    
    return R, V

def show_road(R, time_no):
    args = {}
    args['cmap'] = 'jet'
    args['vmin'] = 0
    args['vmax'] = 1
    plt.figure(figsize=(8, 8))
    plt.matshow(R, fignum=1, **args)
    plt.xlabel('lanes')
    plt.ylabel('Peachtree southbound')
    # plt.colorbar()
    
    plt.title("Road at time {}".format(time_no))
    pass

def get_rand_dir():
    r = random.random()
    
    # right
    if r > .9:
        return 1
    
    # left
    if r > .8:
        return -1

    # straight
    return 0

def step(R, V):
    R_new = np.zeros(R.shape)
    V_new = np.full(V.shape, -1)
    no_cars_leaving = 0
    
    cars = (R == 1)
    
    # go backwards since cars moving forward
    for i in range(R.shape[0] -1, -1, -1):
        for j in range(R.shape[1]):    
            if cars[i, j]:
                # print("there's a car in {}, {}".format(i, j))
                d = get_rand_dir()
                
                new_lane = j + d
                
                # don't actually change lane if on edge
                if new_lane > 1 or new_lane < 0:
                    new_lane -= d
                
                new_block = i + V[i, j]
                
                if new_block >= R.shape[0]:
                    print('Car left road')
                    no_cars_leaving += 1
                    new_block = None
                else:
                    # make sure not occupied
                    while R_new[new_block, new_lane] and new_block > i:
                        new_block -= 1
                
                # couldnt move
                if new_block == i:
                    new_block = i
                    new_lane = j
                
                if new_block:
                    R_new[new_block, new_lane] = 1
                    V_new[new_block, new_lane] = V[i, j]
        
    return R_new, V_new, no_cars_leaving

def run_sim():
    T_MAX = 100
    R, V = init_road_vels()
    R[0, 0] = 1
    R[0, 1] = 1
    V[0, 0] = 2
    V[0, 1] = 2
    times = []
    for t in range(T_MAX):
        num = 0
        R, V, num = step(R, V)
        
        if num > 0:
            l = [t] * num
            times.extend(l)
    
    print("Cars exited road at times: ", times)
    print("On average, took a car {} seconds to get through road.".format(np.average(times)))

    show_road(R, t)

def main():
    print('Running basic simulation with 2 cars starting at road with speeds of 43 mph...')
    run_sim()


if __name__ == '__main__':
    main()