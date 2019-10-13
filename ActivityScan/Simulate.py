from ActivityScan import one_simulate
import statistics
import matplotlib.pyplot as plt

#simulate one time and plot graph
sim = one_simulate()
# print(sim)

cf_mean_1 = statistics.mean(sim[0])
cf_std_1 = statistics.stdev(sim[0])
print('1 sim avg', cf_mean_1, 'std', cf_std_1)

figure_1_sim = plt.figure(1)
plt.plot(sim[0], label="left lane")
plt.plot(sim[1], label="right lane")
plt.xlabel('Simulation Time')
plt.title('Activity Scanning Simulation')
plt.legend()
plt.grid()
# plt.show()

# simulate for 100 times
sim_list = [one_simulate() for _ in range(100)]
comb_run_sim = [[], []]
for i in sim_list:
    # comb_run_sim[0].extend(i[0])
    comb_run_sim[1].extend(i[1])
# print(statistics.mean(comb_run_sim[0]), statistics.stdev(comb_run_sim[0]))
print('100 sim avg', statistics.mean(comb_run_sim[1]), 'std',
      statistics.stdev(comb_run_sim[1]))
# plt.hist([comb_run_sim[0], comb_run_sim[1]], color=['blue', 'orange'])
figure_100_sim = plt.figure(2)
plt.hist(comb_run_sim[1], color='blue')
# legend = ['left', 'right']
plt.title('Activity Scanning Simulation 100 times')
# plt.legend(legend)
plt.show()
