import retro
from pynput import keyboard
import matplotlib.pyplot as plt
import numpy as np
import time
import os
os.environ['CUDA_VISIBLE_DEVICES']='0'
pressed = [None]
meanings = [[None], ['LEFT'], ['RIGHT'], ['C'], ['B'], ['LEFT', 'C'], ['RIGHT', 'C'], ['B', 'C']]
buttons = ['B', 'A', 'MODE', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'C', 'Y', 'X', 'Z']
def is_executed_locally():
    """
    Checks if the script is being executed locally or via SSH.
    Returns True if local, False if via SSH.
    """
    return os.name == 'posix' and 'SSH_CLIENT' not in os.environ

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
        game = "MegaManTheWilyWars-Genesis"
        self.env = make_env(game, state="boss1.state")()
        self.env.reset()
        if not is_executed_locally():
            self.env.render_mode = None
        arr = np.array([False] * self.env.action_space.n)
        obs, _reward, done, truncated, info = self.env.step(arr)
        self.current_player_hp = info['health']
        self.current_boss_hp = info['boss_hp']
        self.is_pressing_jump = False

    def step(self, action):            
        if sum(action) != 1:
            raise ValueError('Multiple input actions!')
        for i in range(len(action)):
            if action[i] == 1:
                pressed = meanings[i]
                
        arr = np.array([False] * self.env.action_space.n)
        for pressed_element in pressed:
            if pressed_element != None:
                arr[buttons.index(pressed_element)] = True
        if arr[buttons.index('C')] == True:
            self.is_pressing_jump = True
        else:
            self.is_pressing_jump = False
        obs, _reward, _done, truncated, info = self.env.step(arr)
        
        # Create a 10x10 pure green square
        green_square = np.zeros((20, 20, 3), dtype=np.uint8)
        green_square[:, :, 1] = 255  # Set green channel to maximum
        if self.is_pressing_jump:
            # Add the green square to the top right corner of the image
            image_height, image_width, _ = obs.shape
            obs[image_height - 20:, image_width - 20:] = green_square

        # green_square = np.zeros((35, 25, 3), dtype=np.uint8)
        # green_square[:, :, 1] = 255  # Set green channel to maximum
        player_X = 0
        if info['Player_X'] > 0:
            player_X = info['Player_X']
        else:
            player_X = 256 + info['Player_X']
        player_X -= 13
        player_Y = info['Player_Y'] + 8
        print(player_X, player_Y)
        #obs[player_Y - 35:player_Y, player_X:player_X + 25] = green_square

        # Define the RGB values to be replaced with black
        image = obs[player_Y - 35:player_Y, player_X:player_X + 25]
        target_colors = [
            np.array([0, 100, 232]),   # 0044e8
            np.array([96, 204, 232]),   # 0020e8
            np.array([0, 68, 200]),  # 0064e8
            np.array([0, 32, 96])   # 0088e8
        ]
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                pixel_color = image[y, x]

                # Check if the pixel color matches any of the target colors
                for target_color in target_colors:
                    if np.array_equal(pixel_color, target_color):
                        # Replace the pixel color with black
                        image[y, x] = [50, 255, 87]
        obs[player_Y - 35:player_Y, player_X:player_X + 25] = image

        _, _, _, _, info2 = self.env.step(arr)
        damage_to_boss1 = -(info['boss_hp'] - self.current_boss_hp)
        damage_to_player1 = -(info['health'] - self.current_player_hp)
        damage_to_boss2 = -(info2['boss_hp'] - self.current_boss_hp)
        damage_to_player2 = -(info2['health'] - self.current_player_hp)

        if info['is_invincible'] != 0:
            reward = 0
            red_square = np.zeros((20, 20, 3), dtype=np.uint8)
            red_square[:, :, 0] = 255  # Set green channel to maximum
            image_height, image_width, _ = obs.shape
            obs[0:20, image_width - 20:] = red_square
        else:
            if damage_to_boss1 != 0 or damage_to_player1 != 0 or damage_to_boss2 != 0 or damage_to_player2 != 0:
                reward = (damage_to_boss1 + damage_to_boss2) * 2 - (damage_to_player1 + damage_to_player2)
            else:
                reward = 0.38

        self.current_boss_hp = info2['boss_hp'] # update boss hp
        self.current_player_hp = info2['health'] # update player hp

        done = False
        if info['boss_hp'] <= 0 or info['health'] <= 0 or info2['boss_hp'] <= 0 or info2['health'] <= 0:
            # if self.current_boss_hp <= 0:
            #     reward = 4 + self.current_player_hp
            # elif self.current_player_hp <= 0:
            #     reward = -4 - self.current_boss_hp
            done = True
            self.env.reset()

        
        return obs, reward, done, truncated, info
    
    def reset(self):
        self.env.reset()

    def closeGame(self):
        self.env.close()

