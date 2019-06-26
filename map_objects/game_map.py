from typing import List
from random import randint

import tcod
import numpy as np

from map_objects.tile import Tile
from map_objects.room import Room
import entity

WALL = 0
FLOOR = 1

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
    self.tiles: List[Tile] = []
    self.entities: List[entity.Entity] = []

  def generate(self) -> None:
    self.tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
    self.player = entity.Entity(self.width//2, self.height//2, ord('@'), tcod.white)
    rooms = []
    num_rooms = 0

    for r in range(self.ROOMS['max']):
      w = randint(self.ROOMS['min_size'], self.ROOMS['max_size'])
      h = randint(self.ROOMS['min_size'], self.ROOMS['max_size'])
      x = randint(0, self.width - w - 1)
      y = randint(0, self.height - h - 1)

      new_room = Room(x, y, w, h)
      for other_room in rooms:
        if new_room.intersect(other_room):
          break
      else:
        self.create_room(new_room)
        (new_x, new_y) = new_room.center()
        if num_rooms == 0:
          self.player.x = new_x
          self.player.y = new_y
        else:
          (prev_x, prev_y) = rooms[num_rooms - 1].center()
          if randint(0, 1) == 1:
            # first move horizontally, then vertically
            self.create_h_tunnel(prev_x, new_x, prev_y)
            self.create_v_tunnel(prev_y, new_y, new_x)
          else:
            # first move vertically, then horizontally
            self.create_v_tunnel(prev_y, new_y, prev_x)
            self.create_h_tunnel(prev_x, new_x, new_y)
        
        rooms.append(new_room)
        num_rooms += 1

    self.entities = [self.player]
    self.colored_tiles = [[self.COLORS['dark_wall'] for y in range(self.height)] for x in range(self.width)]
  
  def create_room(self, room: Room) -> None:
    for x in range(room.x1 + 1, room.x2):
      for y in range(room.y1 + 1, room.y2):
        self.tiles[x][y].blocked = False 
        self.tiles[x][y].block_sight = False 
  
  def create_h_tunnel(self, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
      self.tiles[x][y].blocked = False 
      self.tiles[x][y].block_sight = False 

  def create_v_tunnel(self, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
      self.tiles[x][y].blocked = False 
      self.tiles[x][y].block_sight = False 
  
  def is_blocked(self, x, y):
    if self.tiles[x][y].blocked:
      return True

    return False

  # TODO: clean me up!
  def render(self, console: tcod.console.Console, fov_map, fov_recompute: bool) -> None:
    console.tiles['ch'][:self.width, :self.height] = ord(' ')

    if fov_recompute:
      # FIXME: find a better way to do this, like with np.where
      for x in range(self.width):
        for y in range (self.height):
          visible = tcod.map_is_in_fov(fov_map, x, y) 
          wall = self.tiles[x][y].block_sight

          if visible:
            self.colored_tiles[x][y] = self.COLORS['light_wall'] if wall else self.COLORS['light_ground']
            self.tiles[x][y].explored = True
          elif self.tiles[x][y].explored:
            self.colored_tiles[x][y] = self.COLORS['dark_wall'] if wall else self.COLORS['dark_ground']
    console.tiles['bg'][:self.width, :self.height, :3] = self.colored_tiles

    # def is_visible(tile):
    #   print(tile)
    #   return False
    #   # return tcod.map_is_in_fov(fov_map, x, y) 
    # vis_visible = np.vectorize(is_visible)
    # light = np.where(
    #   vis_visible(self.tiles),
    #   self.COLORS['light_wall'],
    #   self.COLORS['light_ground']
    # )

    for obj in self.entities:
      if 0 <= obj.x < console.width and 0 <= obj.y < console.height:
        console.tiles['ch'][obj.x, obj.y] = obj.char
        console.tiles['fg'][obj.x, obj.y, :3] = obj.color