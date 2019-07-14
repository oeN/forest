from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING

import numpy as np
import tcod.path

from components import base
from components.location import Location
from components.fighter import Fighter

from systems import movement, combact

if TYPE_CHECKING:
  from entity import Entity

class AI(base.Component, base_component=True):
  def take_turn(self, owner: Entity) -> None:
    raise NotImplementedError()

  def get_path(
    self, owner: Entity, target_xy: Tuple[int, int]
  ) -> List[Tuple[int, int]]:
    map_ = owner[Location].map
    walkable = np.copy(map_.tiles)
    blocker_pos = [e[Location].xy for e in map_.entities if Fighter in e]
    blocker_index = tuple(np.transpose(blocker_pos))
    walkable[blocker_index] = False
    walkable[target_xy] = True
    return tcod.path.AStar(walkable).get_path(*owner[Location].xy, *target_xy)

class BasicMonster(AI):
  def __init__(self) -> None:
    self.path: List[Tuple[int, int]] = []

  def take_turn(self, owner: Entity) -> None:
    map_ = owner[Location].map
    if map_.visible[owner[Location].xy]:
      self.path = self.get_path(owner, map_.player[Location].xy)
      if len(self.path) >= 25:
        self.path = []
        movement.move_towards(owner, map_.player[Location].xy)
    if not self.path:
      return
    if owner[Location].distance_to(map_.player[Location]) <= 1:
      combact.attack(owner, map_.player)
    else:
      movement.move_to(owner, self.path.pop(0))
