from __future__ import annotations
from typing import Tuple, Optional

from components import base

class Sprite(base.Component, base_component=True):
  name: str = "<Unamed>"
  char: int = ord('!')
  color: Tuple[int, int, int] = (255, 255, 255)

class Player(Sprite):
  name = "You"
  char = ord('@')
  color = (255, 255, 255)

class Orc(Sprite):
  name = "Orc"
  char = ord('o')
  color = (63, 127, 63)

class HealingPotiont(Sprite):
  name = "Healing Potiont"
  char = ord('I')
  color = (255, 0, 0)
