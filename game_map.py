# Import this to avoid "name 'GameMap' is not defined" in the Room class
from __future__ import annotations

from typing import List, Optional, Tuple, Type
from random import randint

import tcod
import numpy as np

import entity
import fighter

WALL = 0
FLOOR = 1

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
  
  def place_entities(self, gamemap: GameMap) -> None:
    monsters = randint(0, 3)
    for _ in range(monsters):
      x = randint(self.x1 + 1, self.x2 - 2)
      y = randint(self.y1 + 1, self.y2 - 2)
      if gamemap.is_blocked(x, y):
        continue
      # TODO: add code for random enemy type
      gamemap.entities.append(entity.Entity(x, y, fighter.Orc()))

class GameMap:
  COLORS = {
    'dark_wall': tcod.Color(0, 0, 100),
    'dark_ground': tcod.Color(50, 50, 150),
    'light_wall': tcod.Color(130, 110, 50),
    'light_ground': tcod.Color(200, 180, 50)
  }

  ROOMS = {
    'max_size': 10,
    'min_size': 6,
    'max': 30
  }

  player = entity.Entity

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.shape = width, height
    self.tiles = np.zeros(self.shape, dtype=bool, order='F')
    self.explored = np.zeros(self.shape, dtype=bool, order='F')
    self.visible = np.zeros(self.shape, dtype=bool, order='F')
    self.rooms: List[Room] = []
    self.entities: List[entity.Entity] = []

  def generate(self) -> None:
    self.tiles[...] = WALL
    self.rooms = []
    self.entities = []


    for r in range(self.ROOMS['max']):
      w = randint(self.ROOMS['min_size'], self.ROOMS['max_size'])
      h = randint(self.ROOMS['min_size'], self.ROOMS['max_size'])
      x = randint(0, self.width - w - 1)
      y = randint(0, self.height - h - 1)

      new_room = Room(x, y, w, h)
      if any(new_room.intersects(other) for other in self.rooms):
        continue

      self.tiles[new_room.inner] = FLOOR
      if self.rooms:
        other_room = self.rooms[-1]
        t_start = new_room.center
        t_end = other_room.center
        t_middle = t_start[0], t_end[1]

        self.tiles[tcod.line_where(*t_start, *t_middle)] = FLOOR
        self.tiles[tcod.line_where(*t_middle, *t_end)] = FLOOR
      self.rooms.append(new_room)

    for room in self.rooms:
      room.place_entities(self)

    self.player = entity.Entity(*self.rooms[0].center, fighter.Player())
    self.entities.append(self.player)
    self.update_fov()
  
  def is_blocked(self, x, y):
    if not self.tiles[x, y]:
      return True
    if self.entity_at(x, y):
      return True

    return False
  
  def entity_at(self, x, y) -> Optional[entity.Entity]:
    """Return any entity found at x,y position"""
    # TODO: Check if having a bidimensional array of entities can improve performance
    for e in self.entities:
      if not e.visible:
        continue
      if x == e.x and y == e.y:
        return e
    return None
  
  def update_fov(self) -> None:
    self.visible = tcod.map.compute_fov(
      transparency=self.tiles,
      pov=(self.player.x, self.player.y),
      radius=10,
      light_walls=True,
      algorithm=tcod.FOV_RESTRICTIVE,
    )

    self.explored |= self.visible

  def render(self, console: tcod.console.Console) -> None:
    console.tiles['ch'][:self.width, :self.height] = ord(' ')

    dark = np.where(
      self.tiles[..., np.newaxis],
      self.COLORS['dark_ground'],
      self.COLORS['dark_wall']
    )
    light = np.where(
      self.tiles[..., np.newaxis],
      self.COLORS['light_ground'],
      self.COLORS['light_wall']
    )
    # conditions, pick_from_if_true, default
    console.tiles['bg'][:self.width, :self.height, :3] = np.select(
      (self.visible[..., np.newaxis], self.explored[..., np.newaxis]),
      (light, dark),
      (0, 0, 0)
    )

    for obj in self.entities:
      if not (0 <= obj.x < console.width and 0 <= obj.y < console.height):
        continue
      if not self.visible[obj.x, obj.y]:
        continue
      if not obj.visible:
        continue
      console.tiles['ch'][obj.x, obj.y] = obj.char
      console.tiles['fg'][obj.x, obj.y, :3] = obj.color