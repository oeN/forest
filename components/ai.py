from __future__ import annotations
from typing import TYPE_CHECKING

from components import base, fighter
from entity import Entity

class AI(base.Component, base_component=True):
  def take_turn(self, owner: Entity) -> None:
    raise NotImplementedError()

class BasicMonster(AI):
  def take_turn(self, owner: Entity) -> None:
    print(f"The {owner[fighter.Fighter].name} wonders when it will get to move")
