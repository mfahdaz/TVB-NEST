#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0. "

from nest_elephant_tvb.Tvb.modify_tvb.test_interface import tvb_sim
import numpy as np
import numpy.random as rgn

weight = np.array([[5,2,4,0],[8,5,4,1],[6,1,7,9],[10,0,5,6]])
delay = np.array([[7,8,5,1],[0,3,7,9],[4,3,2,8],[9,10,11,5]])
resolution_simulation = 0.1
resolution_monitor = 0.1*10
time_synchronize = 0.1*10
proxy_id_1 = [1]
proxy_id_2 = [0,2]

# full simulation
rgn.seed(42)
sim_ref = tvb_sim(weight, delay,[], resolution_simulation, resolution_monitor,time_synchronize)
time,result_ref,s_ref = sim_ref(resolution_monitor,s=True)

# simulation with one proxy
rgn.seed(42)
sim_1 = tvb_sim(weight, delay,proxy_id_1, resolution_simulation, resolution_monitor,time_synchronize)
time,result_1,s_1 = sim_1(resolution_monitor,[time,result_ref[:,proxy_id_1][:,:,0]],s=True)

# simulation_2 with one proxy
rgn.seed(42)
sim_2 = tvb_sim(weight, delay,proxy_id_2, resolution_simulation, resolution_monitor,time_synchronize)
time,result_2,s_2 = sim_2(resolution_monitor,[time,result_1[:,proxy_id_2][:,:,0]],s=True)

print("COMPARE PROXY 1 ---------------")
diff_1 = np.where(np.squeeze(result_ref,axis=2)[0] != np.squeeze(result_1,axis=2)[0])
if diff_1[0].size != 0:
    print("Fail compare")
    print(diff_1)
    print(result_ref)
    print(result_1)
else:
    print('test 0 : succeed')
diff_s_1 = np.where(np.squeeze(s_ref,axis=2)[0] != np.squeeze(s_1,axis=2)[0])
if diff_s_1[0].size != 0:
    print("Fail compare")
    print(diff_s_1)
    print(result_ref)
    print(result_1)
else:
    print('test 0 : succeed')
print("COMPARE PROXY 2 ---------------")
diff_2 = np.where(np.squeeze(result_ref,axis=2)[0] != np.squeeze(result_2,axis=2)[0])
if diff_2[0].size != 0:
    print("Fail compare")
    print(diff_2)
    print(result_ref)
    print(result_2)
else:
    print('test 0 : succeed')
diff_s_2 = np.where(np.squeeze(s_ref,axis=2)[0] != np.squeeze(s_2,axis=2)[0])
if diff_s_2[0].size != 0:
    print("Fail compare")
    print(diff_s_2)
    print(result_ref)
    print(result_2)
else:
    print('test 0 : succeed')

max_error_h_1 = 0.0
max_error_s_1 = 0.0
max_error_h_2 = 0.0
max_error_s_2 = 0.0

for i in range(0,100):
    time,result_ref,s_ref = sim_ref(time_synchronize,s=True)
    time,result_1,s_1 = sim_1(time_synchronize,[time,result_ref[:,proxy_id_1][:,:,0]],s=True)
    time,result_2,s_2 = sim_2(time_synchronize,[time,result_1[:,proxy_id_2][:,:,0]],s=True)

    print("COMPARE PROXY 1 ---------------")
    if np.max(np.abs(result_ref- result_1)) > max_error_h_1:
        max_error_h_1 = np.max(np.abs(result_ref- result_1))
    diff_1 = np.where(np.squeeze(result_ref, axis=2)[0] != np.squeeze(result_1, axis=2)[0])
    if diff_1[0].size != 0:
        print("Fail compare")
        print(diff_1)
        print(result_ref)
        print(result_1)
    else:
        print('test' + str(i + 1) + ' : succeed')
    if np.max(np.abs(s_ref - s_1)) > max_error_s_1:
        max_error_s_1 = np.max(np.abs(s_ref - s_1))
    diff_s_1 = np.where(np.squeeze(s_ref, axis=2)[0] != np.squeeze(s_1, axis=2)[0])
    if diff_s_1[0].size != 0:
        print("Fail compare")
        print(diff_s_1)
        print(result_ref)
        print(result_1)
    else:
        print('test' + str(i + 1) + ' : succeed')
    print("COMPARE PROXY 2 ---------------")
    if np.max(np.abs(result_ref- result_2)) > max_error_h_2:
        max_error_h_2 = np.max(np.abs(result_ref- result_2))
    diff_2 = np.where(np.squeeze(result_ref, axis=2)[0] != np.squeeze(result_2, axis=2)[0])
    if diff_2[0].size != 0:
        print("Fail compare")
        print(diff_2)
        print(result_ref)
        print(result_2)
    else:
        print('test' + str(i + 1) + ' : succeed')
    if np.max(np.abs(s_ref - s_2)) > max_error_s_2:
        max_error_s_2 = np.max(np.abs(s_ref - s_2))
    diff_s_2 = np.where(np.squeeze(s_ref, axis=2)[0] != np.squeeze(s_2, axis=2)[0])
    if diff_s_2[0].size != 0:
        print("Fail compare")
        print(diff_s_2)
        print(result_ref)
        print(result_2)
    else:
        print('test' + str(i + 1) + ' : succeed')

print("time_synchronize : %r s"%(time_synchronize*10**-3))
print("time_monitor : %r s"%(resolution_monitor*10**-3))
print("max error firing rate for 1: %r Hz" % (max_error_h_1*10**3))
print("max error S rate for 1 : %r" % max_error_s_1)
print("max error firing rate for 2: %r Hz" % (max_error_h_2*10**3))
print("max error S rate for 2: %r" % max_error_s_2)