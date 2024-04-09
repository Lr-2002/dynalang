import embodied
import numpy as np
import gymnasium
from gym import spaces
import os
from civrealm.freeciv.utils.freeciv_logging import  fc_logger
from civrealm.envs.freeciv_wrapper import DynalangWrapper
from civrealm.configs import fc_args
from civrealm.freeciv.utils.port_utils import Ports
import civrealm
from . import from_gym
class Minitask(embodied.Env):
    def __init__(self, tmp):
        self._env = gymnasium.make('civrealm/FreecivTensorMinitask-v0', client_port=Ports.get())
        self._env = DynalangWrapper(self._env)
        self._env = from_gym.FromGym(self._env)

        # self.wrappers = [DynalangWrapper, from_gym.FromGym]



    def step(self, action):
        obs, reward, terminated, truncated, info = self._env.step(action)
        return obs, reward, terminated or truncated, info

    def reset(self):
        self._env.close()
        return self._env.reset()

    @property
    def act_space(self):
        return self._env.act_space

    @property
    def obs_space(self):
        return self._env.obs_space

# class
