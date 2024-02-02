import retro
from pynput import keyboard
import numpy as np
import time
pressed = [None]
meanings = [[None], ['LEFT'], ['RIGHT'], ['A'], ['B'], ['LEFT', 'A'], ['RIGHT', 'A']]
buttons = ['B', None, 'SELECT', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'A']
    
def make_env(game, state):
    def _init():
        env = retro.make(
            game=game, 
            state=state, 
            use_restricted_actions=retro.Actions.FILTERED,
            obs_type=retro.Observations.IMAGE
        )
        return env
    return _init    

class MegaMan():
    def __init__(self) -> None:
        game = "MegaMan-Nes"
        self.env = make_env(game, state="boss2.state")()
        self.env.reset()
        arr = np.array([False] * self.env.action_space.n)
        arr[1] = True
        obs, _reward, done, truncated, info = self.env.step(arr)
        self.current_player_hp = info['health']
        self.current_boss_hp = info['boss_hp']

    def step(self, action):
        if sum(action) != 1:
            raise ValueError('Multiple input actions!')
        for i in range(len(action)):
            if action[i] == 1:
                pressed = meanings[i]
                
        arr = np.array([False] * self.env.action_space.n)
        for pressed_element in pressed:
            arr[buttons.index(pressed_element)] = True
        obs, _reward, _done, truncated, info = self.env.step(arr)

        damage_to_boss = -(info['boss_hp'] - self.current_boss_hp)
        damage_to_player = -(info['health'] - self.current_player_hp)
        reward = damage_to_boss - damage_to_player

        self.current_boss_hp = info['boss_hp']
        self.current_player_hp = info['health']

        done = False
        if self.current_boss_hp <= 0 or self.current_player_hp <= 0:
            if self.current_boss_hp <= 0:
                reward = 4 + self.current_player_hp
            elif self.current_player_hp <= 0:
                reward = -4 - self.current_boss_hp
            done = True
            self.env.reset()
        return obs, reward, done, truncated, info
    
    def reset(self):
        self.env.reset()

    def closeGame(self):
        self.env.close()