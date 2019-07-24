from __future__ import annotations

from typing import List, Optional, Tuple, Type
from random import randint
import tcod
import numpy as np

from game_map import GameMap
import entity
from components import fighter, ai, item, location
from components.location import Location
import entities_db

WALL = 0
FLOOR = 1

def spawn_entity(e: entity.Entity, location: location.Location) -> entity.Entity:
  e[Location] = location
  location.map.entities.append(e)
  return e

class Room:
  def __init__(self, x, y, w, h) -> None:
    self.x1, self.y1 = x, y
    self.x2 = x + w
    self.y2 = y + h

  @property
  def inner(self) -> Tuple[slice, slice]:
    """Return the NumPy index for the inner room area."""
    index: Tuple[slice, slice] = np.s_[
      self.x1 + 1 : self.x2 - 1, self.y1 + 1 : self.y2 - 1
    ]
    return index

  @property
  def center(self) -> Tuple[int, int]:
    return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

  def intersects(self, other) -> bool:
    # returns true if this rectangle intersects with another one
    return (
      self.x1 <= other.x2 and self.x2 >= other.x1 and
      self.y1 <= other.y2 and self.y2 >= other.y1
    )

  def random_coordinates(self) -> Tuple[int, int]:
    x = randint(self.x1 + 1, self.x2 - 2)
    y = randint(self.y1 + 1, self.y2 - 2)
    return (x, y)

  def spawn_monsters(self, gamemap: GameMap) -> None:
    monsters = randint(0, 3)
    for _ in range(monsters):
      x, y = self.random_coordinates()
      if gamemap.is_blocked(x, y):
        continue
      # TODO: add code for random enemy type
      spawn_entity(entities_db.monsters['orc'](), gamemap[x, y])

  def spawn_items(self, gamemap: GameMap) -> None:
    items = randint(0, 2)
    for _ in range(items):
      x, y = self.random_coordinates()
      if gamemap.is_blocked(x, y):
        continue
      # TODO: add code for random enemy type
      spawn_entity(entities_db.items['healing_potiont'](), gamemap[x, y])

  def place_entities(self, gamemap: GameMap) -> None:
    self.spawn_monsters(gamemap)
    self.spawn_items(gamemap)


def generate(width: int, height: int) -> GameMap:
  ROOMS = {
    'min_size': 7,
    'max_size': 10,
    'max': 30
  }

  gm = GameMap(width, height)
  gm.tiles[...] = WALL
  rooms: List[Room] = []

  for _ in range(ROOMS['max']):
    w = randint(ROOMS['min_size'], ROOMS['max_size'])
    h = randint(ROOMS['min_size'], ROOMS['max_size'])
    x = randint(0, width - w - 1)
    y = randint(0, height - h - 1)

    new_room = Room(x, y, w, h)
    if any(new_room.intersects(other) for other in rooms):
      continue

    gm.tiles[new_room.inner] = FLOOR
    if rooms:
      other_room = rooms[-1]
      t_start = new_room.center
      t_end = other_room.center
      t_middle = t_start[0], t_end[1]

      gm.tiles[tcod.line_where(*t_start, *t_middle)] = FLOOR
      gm.tiles[tcod.line_where(*t_middle, *t_end)] = FLOOR
    rooms.append(new_room)

  for room in rooms:
    room.place_entities(gm)

  gm.player = spawn_entity(entities_db.player(), gm[rooms[0].center])
  gm.entities.append(gm.player)
  gm.update_fov()
  return gm
