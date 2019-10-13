import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plot
import random
import scipy.stats as ss

ROAD_SIZE = (66, 2)

def init_road_vels():
    R = np.zeros(ROAD_SIZE)
    V = np.full(ROAD_SIZE, -1)
    
    return R, V

def show_road(R, time_no):
    args = {}
    args['cmap'] = 'jet'
    args['vmin'] = 0
    args['vmax'] = 1
    plot.figure(figsize=(8, 8))
    plot.matshow(R, fignum=1, **args)
    plot.xlabel('lanes')
    plot.ylabel('Peachtree southbound')
    # plt.colorbar()
    
    plot.title("Road at time {}".format(time_no))
    pass

def get_rand_dir():
    r = random.random()
    
    # right
    if r > .996:
        return 1
    
    # left
    if r > .992:
        return -1

    # straight
    return 0

# constant velocity of 2 blocks per time step
def get_velo():
    return 2

def get_next_entry_time_14th():
    log_dist = ss.lognorm
    rand = log_dist.rvs(1.123494632217069, loc=-0.1308024415404237, scale=2.222162369513514, size=1)[0]
    return int(rand)

def get_next_entry_time_11th():
    log_dist = ss.lognorm
    rand = log_dist.rvs(1.5234191072345973, loc=1.9716462121837928, scale=7.605110207945611, size=1)[0]
    
    return int(rand)

def step(R, V, lights):
    R_new = np.zeros(R.shape)
    V_new = np.full(V.shape, -1)
    cars_leaving = []
    
    cars = (R >= 1)
    
    # 10th, 11th, 12th, and 14th st
    LIGHT_ROWS = [65, 49, 33, 0]
    
    # go backwards since cars moving forward
    for i in range(R.shape[0] -1, -1, -1):
        for j in range(R.shape[1]):    
            if cars[i, j]:
                car_id = R[i, j].astype(int)
                # print("there's a car in {}, {} with id: {}".format(i, j, car_id))
                # print('Carid: ', car_id)
                d = get_rand_dir()
                
                new_lane = j + d
                
                # don't actually change lane if on edge
                if new_lane > 1 or new_lane < 0:
                    new_lane -= d
                
                new_block = i + V[i, j]
                
                # check lights
                for light_i, light_row in enumerate(LIGHT_ROWS):
                    if not lights[light_i] and i <= light_row and new_block > light_row:
                        # Want to cross intersection but light is 0
                        new_block = light_row
                        break
                 
                # See if car has left corridor
                if new_block >= R.shape[0]:
                    cars_leaving.append(car_id)
                    new_block = None
                else:
                    # make sure not occupied, else dont move
                    while R_new[new_block, new_lane] and new_block > i:
                        new_block -= 1
                
                # couldnt move
                if new_block == i:
                    new_block = i
                    new_lane = j
                
                if new_block:
                    R_new[new_block, new_lane] = car_id
                    V_new[new_block, new_lane] = V[i, j]
        
    return R_new, V_new, cars_leaving
    

def run_sim(T_MAX=100, print_stats=False, slow_traffic=False):
    # constants
    light_timing = [[53, 34], [59, 42], [53, 61], [49, 37]]
    index_11th_right = (49, 0)
    
    # init state
    R, V = init_road_vels()
    next_entry_left_time = 0
    next_entry_right_time = 0
    next_11th_right_time = 0
    times = []
    times_entered = {}
    id_c = 1
    
    # 10th, 11th, 12th, 14th
    lights = [1,1,1,1]
    light_counters = [light_timing[index][val] for index, val in enumerate(lights)]
    
    for t in range(T_MAX):
         
        # check lights and increment
        for index, count_value in enumerate(light_counters):
            if not count_value:
                lights[index] = not lights[index]
                light_counters[index] = light_timing[index][lights[index]]
            else:
                light_counters[index] -= 1
        
        # Enter left lane top
        if not next_entry_left_time:
            if not R[0, 0]:
                R[0, 0] = id_c
                times_entered[id_c] = t
                
                id_c += 1
                V[0, 0] = get_velo()
                next_entry_left_time = get_next_entry_time_14th()
                if slow_traffic:
                    next_entry_left_time *= 2
        else:
            next_entry_left_time -= 1
            
        # Enter right lane top
        if not next_entry_right_time:
            if not R[0, 1]:
                R[0, 1] = id_c
                times_entered[id_c] = t
                
                id_c += 1
                V[0, 1] = get_velo()
                next_entry_right_time = get_next_entry_time_14th()
                if slow_traffic:
                    next_entry_right_time *= 2
        else:
            next_entry_right_time -= 1
        
        #Enter 11th turn right
        if not next_11th_right_time:
            if not R[index_11th_right]:
                R[index_11th_right] = id_c
                
                # don't add to times_entered since dont want to track time
                id_c += 1
                V[index_11th_right] = get_velo()
                next_11th_right_time = get_next_entry_time_11th()
                if slow_traffic:
                    next_11th_right_time *= 2
        else:
            next_11th_right_time -= 1
        
        R, V, exited_ids = step(R, V, lights)
        
        for id_exit in exited_ids:
            if id_exit in times_entered:
                elapsed_time = t - times_entered[id_exit]
                del times_entered[id_exit]
                times.append(elapsed_time)
    
    av_time = np.average(times)
    num_cars = len(times)
    
    if print_stats:
        print("{} cars passed through.".format(num_cars))
        print("On average, took a car {} seconds to get through road.".format(av_time))
        show_road(R, t)
    
    return num_cars, av_time

def run_monte_carlo_sims(num_trials_p=20, num_iterations=900, slow_traffic=False):
    
    times = []
    num_cars = []
    for _ in range(num_trials_p):
        run_cars, run_time = run_sim(num_iterations, slow_traffic=slow_traffic)
        times.append(run_time)
        num_cars.append(run_cars)
    
    print('Across {} trials got following stats:'.format(num_trials_p))
    print('\t Time: {}'.format(np.average(times)))
    print('\t # Cars: {}'.format(np.average(num_cars)))
    return times, num_cars

def main():
    print('Running simulation with high traffic...')
    t_normal, _ = run_monte_carlo_sims(num_trials_p=100, num_iterations=900, slow_traffic=False)
    print('Running simulation with low traffic...')
    t_slow, _ = run_monte_carlo_sims(num_trials_p=100, num_iterations=900, slow_traffic=True)


if __name__ == '__main__':
    main()