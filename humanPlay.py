import tensorflow as tf # CAN YOU BELIEVE? IF YOU DON'T IMPORT TF, THE """"MATPLOTLIB.PYPLOT"""" WILL BROKEN!! WHAT A SWEETY COUPLES~

import matplotlib.pyplot as plt
from pynput import keyboard
import numpy as np
import time
from wrapped_megaman import MegaMan


pressed = np.array([1, 0, 0, 0, 0, 0, 0], dtype=int)
inputs = [None, 'a', 'd', 'j', 'k', 'q', 'e']

def on_press(key):
    try:
        global pressed
        for i in range(len(inputs)):
            if inputs[i] == key.char:
                pressed = np.zeros(7)
                pressed[i] = int(1)
                print(pressed)
            else:
                pressed[i] = int(0)
        if sum(pressed) == 0:
            pressed[0] = int(1)

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    # print('{0} released'.format(
    #     key))
    global pressed
    pressed[0] = int(1)
    for i in range(1, len(pressed)):
        pressed[i] = int(0)
    if key == keyboard.Key.esc:
        # Stop listener
        return False


env = MegaMan()
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
if True:
    obs, reward, done, truncated, info = env.step(pressed)
    print(pressed)
    plt.imshow(obs)
    plt.show()
    print(obs.shape)
    plt.imshow(obs[:, :, 0])
    plt.show()
    #print('boss hp:', info['boss_hp'])
    time.sleep(1 / 5)
