from __future__ import annotations

from game_map import GameMap
from entity import Entity
from components.ai import AI

class Session:
  active_map: GameMap

  @property
  def player(self) -> Entity:
    return self.active_map.player

  def enemy_turn(self) -> None:
    for obj in self.active_map.entities:
      if AI not in obj:
        continue
      if obj is self.player:
        continue
      obj[AI].take_turn(obj)
