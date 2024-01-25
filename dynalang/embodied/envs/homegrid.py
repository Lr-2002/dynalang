import embodied
import numpy as np

from PIL import Image, ImageFont, ImageDraw


class HomeGrid(embodied.Env):

  def __init__(
    self,
    task,
    size=(64, 64),
    max_steps=100,
    num_trashobjs=2,
    num_trashcans=2,
    p_teleport=0.05,
    p_unsafe=0.,
    fixed_state=None,
    vis=False,
  ):
    from . import from_gym
    import homegrid
    import gym
    from gym.envs.registration import register
    sym = {'step': 0, 'agent': {'pos': (5, 9), 'room': 'K', 'dir': 1, 'carrying': None}, 'objects': [
      {'name': 'recycling bin', 'type': 'Storage', 'pos': (12, 10), 'room': 'D', 'state': 'open', 'action': 'lift',
       'invisible': None, 'contains': []},
      {'name': 'trash bin', 'type': 'Storage', 'pos': (11, 1), 'room': 'L', 'state': 'closed', 'action': 'lift',
       'invisible': None, 'contains': []},
      {'name': 'fruit', 'type': 'Pickable', 'pos': (8, 2), 'room': 'L', 'state': None, 'action': None,
       'invisible': False, 'contains': None},
      {'name': 'bottle', 'type': 'Pickable', 'pos': (12, 2), 'room': 'L', 'state': None, 'action': None,
       'invisible': False, 'contains': None}], 'front_obj': None, 'unsafe': {'name': None, 'poss': {}, 'end': -1}}
    register(
      id="homegrid-fix",
      entry_point="homegrid:HomeGrid",
      kwargs={"lang_types": ["task"],
              'fixed_state': sym},
    )
    assert task in ("task", "future", "dynamics", "corrections", 'fix')
    env = gym.make(f"homegrid-{task}", 
                   disable_env_checker=True,
                   max_steps=max_steps,
                   num_trashobjs=num_trashobjs,
                   num_trashcans=num_trashcans,
                   p_teleport=p_teleport,
                   p_unsafe=p_unsafe,
                   fixed_state=fixed_state)
    env = homegrid.wrappers.Gym26Wrapper(env)
    self._env = env
    self.observation_space = self._env.observation_space
    self.action_space = self._env.action_space
    self.wrappers = [
      from_gym.FromGym,
      lambda e: embodied.wrappers.ResizeImage(e, size),
    ]
    self.vis = vis

  def reset(self):
    obs = self._env.reset()
    if self.vis:
      obs["log_image"] = self.render_with_text(obs["log_language_info"])
    return obs

  def step(self, action):
    obs, rew, done, info = self._env.step(action)
    if self.vis:
      obs["log_image"] = self.render_with_text(obs["log_language_info"])
    return obs, rew, done, info

  def render(self):
    return self._env.render(mode="rgb_array")

  def render_with_text(self, text):
    img = self._env.render(mode="rgb_array")
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, (0, 0, 0))
    draw.text((0, 45), "Action: {}".format(self._env.prev_action), (0, 0, 0))
    img = np.asarray(img)
    return img

  def init_from_state(self, state):
    self._env.init_from_state(state)
