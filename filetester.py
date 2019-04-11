import pickle
from pathlib import Path
import numpy as np
from os import listdir
from os.path import isfile, join
import os
from rlbot.messages.flat.Physics import Physics

# def FieldPosition(p: Physics, team: int):
#     l = p.Location

#     return 0,0,0

np.set_printoptions(linewidth=400)
#frame_file = 'capture\\BallRollingToGoalie.pt'
#save_file = 'capture\\BallRollingToGoalie.npz'
save_file = 'capture\\unlabeled.npz'
collection = []
folder = 'capture'

files = [f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".pt")]
for i in range(len(files)):
    file = join(folder, files[i])
    count = 0
    with open(file, 'rb') as f_handle:
        while f_handle.tell() != os.fstat(f_handle.fileno()).st_size:
            count += 1
            memory = pickle.load(f_handle)
            sz = len(memory)
            if sz < 200 and sz > 10:
                seq = np.zeros((sz, 9))
                for z in range(sz):
                    i = sz - z - 1
                    action = memory[i]['action']
                    state = memory[i]['state']                    

                    seq[i][0] = action.throttle
                    seq[i][1] = action.steer
                    seq[i][2] = action.roll
                    seq[i][3] = action.pitch
                    seq[i][4] = action.yaw
                    seq[i][5] = action.boost
                    seq[i][6] = action.handbrake
                    seq[i][7] = action.jump

                    c_inx = memory[i]['index']
                    car = state.game_cars[c_inx]
                    seq[i][8] = not car.has_wheel_contact
                collection.append(seq)
    print(file,count)
np.savez_compressed(save_file, collection)
