from typing import Tuple, Optional

from components import base


class Fighter(base.Component, base_component=True):
  hp: int = 0
  power: int = 0
  defense: int = 0

  def __init__(self) -> None:
    self.max_hp = self.hp

  @property
  def is_dead(self):
    return self.hp == 0


class Player(Fighter):
  hp = 30
  power = 5
  defense = 2


class Orc(Fighter):
  hp = 10
  power = 3
  defense = 0
