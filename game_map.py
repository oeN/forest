# Import this to avoid "name 'GameMap' is not defined" in the Room class
from __future__ import annotations

from typing import List, Optional, Tuple, Type

import tcod
import numpy as np

import entity
from session import Session
from components.fighter import Fighter
from components.location import Location
from components.sprite import Sprite

class MapLocation(Location):
  def __init__(self, gamemap: GameMap, x: int, y: int):
    self.map = gamemap
    self.x = x
    self.y = y

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

  player: entity.Entity
  session: Session

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.shape = width, height
    self.tiles = np.zeros(self.shape, dtype=bool, order='F')
    self.explored = np.zeros(self.shape, dtype=bool, order='F')
    self.visible = np.zeros(self.shape, dtype=bool, order='F')
    self.entities: List[entity.Entity] = []

  def is_blocked(self, x, y):
    if not (0 <= x < self.width and 0 <= y < self.height):
      return True
    if not self.tiles[x, y]:
      return True
    if self.fighter_at(x, y):
      return True

    return False

  def fighter_at(self, x, y) -> Optional[entity.Entity]:
    """Return any entity found at x,y position"""
    # TODO: Check if having a bidimensional array of entities can improve performance
    for e in self.entities:
      if Fighter not in e or e[Fighter].is_dead:
        continue
      if e[Location].xy == (x, y):
        return e
    return None

  def update_fov(self) -> None:
    self.visible = tcod.map.compute_fov(
      transparency=self.tiles,
      pov=self.player[Location].xy,
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
      if Sprite not in obj:
        continue
      if Fighter in obj and obj[Fighter].is_dead:
        continue
      x, y = xy = obj[Location].xy
      if not (0 <= x < console.width and 0 <= y < console.height):
        continue
      if not self.visible[xy]:
        continue
      console.tiles['ch'][xy] = obj[Sprite].char
      console.tiles['fg'][x, y, :3] = obj[Sprite].color

  def __getitem__(self, key: Tuple[int, int]) -> MapLocation:
    return MapLocation(self, *key)
