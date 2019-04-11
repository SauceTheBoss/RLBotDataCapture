from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.game_state_util import GameState
from rlbot.messages.flat import GameTickPacket
from util import *
import copy
import gc


import Procedure
import Strategy
import Handling



class Stick(BaseAgent):
    def get_output(self, packet):
        Procedure.pre_process(self, packet)
        Strategy.plan(self)
        Handling.execute(self)
        Procedure.feedback(self)
        self.LogAction(packet)
        return self

    def LogAction(self,packet: GameTickPacket):
        c_packet = copy.deepcopy(packet)
        newState = {
            'state': c_packet,
            'action': SimpleControllerState(
                steer = self.steer,
                throttle = self.throttle,
                pitch = self.pitch,
                yaw = self.yaw,
                roll = self.roll,
                jump = bool(self.jump),
                boost = bool(self.boost),
                handbrake = bool(self.handbrake))
            }
        self.memory.append(newState)

        lt_time = packet.game_ball.latest_touch.time_seconds

        if self.LastTouch == None:
            self.LastTouch = lt_time
        elif self.LastTouch != lt_time:
            self.LastTouch = lt_time
            self.SaveMemory()        

    def initialize_agent(self): 
        self.memory = []
        self.LastTouch = None

    def SaveMemory(self):
        l = len(self.memory)
        if l < 20 or l > 200:
            print("rejecting:",l)
        else:
            print("saving")
            import pickle
            from pathlib import Path
            frame_file = "capture\\" + self.name + ".pt"
            with open(frame_file, 'ab') as f_handle:
                pickle.dump(self.memory, f_handle)
        del self.memory
        gc.collect()
        self.memory = []

    # def retire(self): 
    #     if len(self.memory) > 0:
    #         self.SaveMemory()
        
