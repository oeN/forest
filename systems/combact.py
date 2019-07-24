from components.location import Location
from components.fighter import Fighter
from components.sprite import Sprite

def attack(actor, target) -> None:
  assert actor[Location].distance_to(target[Location]) <= 1

  session = actor[Location].map.session
  damage = actor[Fighter].power - target[Fighter].defense

  attack_direction = f"{actor[Sprite].name} attacks {target[Sprite].name}"

  if damage > 0:
    target[Fighter].hp -= damage
    session.report(f"{attack_direction} for {damage} hit points")
  else:
    session.report(f"{attack_direction} without consequences")
  if target[Fighter].hp <= 0:
    session.report(f"The {target[Sprite].name} dies")
