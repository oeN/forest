from typing import List

import tcod
import numpy as np

from map_objects.tile import Tile
import entity

class GameMap:
  COLORS = {
    'dark_wall': tcod.Color(0, 0, 100),
    'dark_ground': tcod.Color(50, 50, 150)
  }

  player = entity.Entity

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.shape = width, height
    self.tiles = np.zeros(self.shape, dtype=bool, order='F')
    self.entities: List[entity.Entity] = []

  def generate(self) -> None:
    # Make a simple wall
    self.tiles[30][22] = 1
    self.tiles[31][22] = 1
    self.tiles[32][22] = 1

    self.player = entity.Entity(self.width//2, self.height//2, ord('@'), tcod.white)
    self.entities = [self.player]

    # [[print(self.tiles[x][y].blocked) for x in range(self.width)] for y in range(self.height)]
  
  def is_blocked(self, x, y):
    if self.tiles[x][y]:
      return True

    return False

  def render(self, console: tcod.console.Console) -> None:
    console.tiles['ch'][:self.width, :self.height] = ord(' ')

    dark = np.where(
      self.tiles[..., np.newaxis],
      self.COLORS['dark_wall'],
      self.COLORS['dark_ground']
    )

    console.tiles['bg'][:self.width, :self.height, :3] = dark

    for obj in self.entities:
      if 0 <= obj.x < console.width and 0 <= obj.y < console.height:
        console.tiles["ch"][obj.x, obj.y] = obj.char
        console.tiles['fg'][obj.x, obj.y, :3] = obj.color