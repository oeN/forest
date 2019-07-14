from __future__ import annotations

from typing import Optional, Tuple

from components import fighter

class Entity:
  """
  A generic object to represent players, enemies, items, etc.
  """
  def __init__(self, x: int, y: int, fighter: Optional[fighter.Fighter] = None):
    self.x = x
    self.y = y
    self.fighter = fighter

  @property
  def char(self) -> int:
    if self.fighter:
      return self.fighter.char
    return ord('!')
  
  @property
  def color(self) -> Tuple[int, int, int]:
    if self.fighter:
      return self.fighter.color
    return (255, 255, 255)
  
  @property
  def visible(self) -> bool:
    if self.fighter:
      return not self.fighter.is_dead
    return True
  
  def relative(self, x: int, y: int):
    return self.x + x, self.y + y

  def move(self, x: int, y: int) -> None:
    # Move the entity by a given amount
    self.x, self.y = self.relative(x, y)
  
  def attack(self, target: Entity) -> None:
    assert self.fighter
    assert target.fighter
    damage = self.fighter.power - target.fighter.defense

    attack_direction = f"{self.fighter.name} attacks {target.fighter.name}"

    if damage > 0:
      target.fighter.hp -= damage
      print(f"{attack_direction} for {damage} hit points")
    else:
      print(f"{attack_direction} without consequences")
    if target.fighter.hp <= 0:
      print(f"The {target.fighter.name} dies")
