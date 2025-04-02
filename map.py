import numpy as np

world_map = np.zeros((25,12))
world_map[0,7] = 33
world_map[1,9] = 39
world_map[0,8] = 4
world_map[0,9] = 40
world_map[1,7] = 2
world_map[1,8] = 14
world_map[2,7] = 2
world_map[2,8] = 37
world_map[2,9] = 40
world_map[3,8] = 37
world_map[3,9] = 4
world_map[3,7] = 2
world_map[4,7] = 3
world_map[4,8] = 41
world_map[4,9] = 35
world_map[5,5] = 49
world_map[6,5] = 50
world_map[7,5] = 51
world_map[9,4] = 18
world_map[5,9] = 10
world_map[6,9] = 10
world_map[7,9] = 10
world_map[8,9] = 36
world_map[8,8] = 9
world_map[9,7] = 48
world_map[9,8] = 40
world_map[10,8] = 10
world_map[11,8] = 33
world_map[12,8] = 34
world_map[13,8] = 12
world_map[13,9] = 62
world_map[13,10] = 35
world_map[14,10] = 33
world_map[15,10] = 2
world_map[16,10] = 2
world_map[17,10] = 2
world_map[18,10] = 2
world_map[19,10] = 3
world_map[12,11] = 20
world_map[13,11] = 4
world_map[14,11] = 40

for i in range(9,13):
    world_map[i,9] = np.random.choice([4,39,40,19,20])


for i in range(0,14):
    world_map[i,11] = np.random.choice([4,38,39,40,19,20])
    world_map[i,10] = np.random.choice([4,38,39,40,19,20])



world_map[15,11] = 14
world_map[16,11] = 15
world_map[17,11] = 15
world_map[18,11] = 15
world_map[19,11] = 15
world_map[19,11] = 15
world_map[20,11] = 11
world_map[21,11] = 11
world_map[22,11] = 11
world_map[23,11] = 11
world_map[24,11] = 11