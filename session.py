from __future__ import annotations

from typing import List, TYPE_CHECKING

from entity import Entity
from components.ai import AI

if TYPE_CHECKING:
  from game_map import GameMap

class Session:
  active_map: GameMap

  def __init__(self) -> None:
    self.log: List[str] = []

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

  def report(self, text: str) -> None:
    print(text)
    self.log.append(text)

