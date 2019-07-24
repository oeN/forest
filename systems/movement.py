from typing import Tuple, TYPE_CHECKING

from components.location import Location
import entity

from systems import combact

def move_to(actor: entity.Entity, xy_destination: Tuple[int, int]) -> None:
  """Move an entity to a position, interacting with obstacles."""
  map_ = actor[Location].map
  target = map_.fighter_at(*xy_destination)
  if not map_.is_blocked(*xy_destination):
    actor[Location] = map_[xy_destination]
    map_.update_fov()
  elif target:
    return combact.attack(actor, target)

def move(actor: entity.Entity, xy_direction: Tuple[int, int]) -> None:
  move_to(actor, actor[Location].relative(*xy_direction))

def move_towards(actor: entity.Entity, destination: Tuple[int, int]) -> None:
  dx = destination[0] - actor[Location].x
  dy = destination[1] - actor[Location].y
  distance = max(abs(dx), abs(dy))
  dx = int(round(dx / distance))
  dy = int(round(dy / distance))
  return move(actor, (dx, dy))

