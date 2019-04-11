import copy
import gc

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat import GameTickPacket
from rlbot.utils.game_state_util import GameState

import Bot


class RashBot(BaseAgent):

    def get_output(self, packet):

        game = self.convert_packet_to_v3(packet)
        output = Bot.Process(self, game)
        rtn = self.convert_output_to_v4(output)
        self.LogAction(packet, rtn)

        return rtn

    def LogAction(self,packet: GameTickPacket, action: SimpleControllerState):
        c_packet = copy.deepcopy(packet)
        newState = {
            'state': c_packet,
            'action': action
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
