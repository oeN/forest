import tcod
import tcod.event

from map_objects.game_map import GameMap

class GameState(tcod.event.EventDispatch):
  COMMAND_KEYS = {
    tcod.event.K_ESCAPE: 'quit'
  }

  MOVE_KEYS = {
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1)
  }

  fov_recompute = bool

  def __init__(self, active_map: GameMap):
    self.active_map = active_map
    self.initialize_fov()

  def initialize_fov(self) -> None:
    self.fov_recompute = True
    self.fov_map = tcod.map_new(self.active_map.width, self.active_map.height)

    for y in range(self.active_map.height):
      for x in range(self.active_map.width):
        tcod.map_set_properties(self.fov_map, x, y, 
          not self.active_map.tiles[x][y].block_sight,
          not self.active_map.tiles[x][y].blocked)
  
  def recompute_fov(self):
    if self.fov_recompute:
      player = self.active_map.player
      fov_algorithm = 6
      fov_light_walls = True
      fov_radius = 10
      tcod.map_compute_fov(self.fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
  
  def on_draw(self, console: tcod.console.Console) -> None:
    console.clear()
    self.recompute_fov()
    self.active_map.render(console, self.fov_map, self.fov_recompute)
    self.fov_recompute = False
    tcod.console_flush()
  
  def ev_quit(self, event: tcod.event.Quit) -> None:
    self.cmd_quit()
  
  def ev_keydown(self, event: tcod.event.KeyDown) -> None:
    if event.sym in self.COMMAND_KEYS:
      getattr(self, "cmd_%s" % event.sym)()
    elif event.sym in self.MOVE_KEYS:
      self.cmd_move(*self.MOVE_KEYS[event.sym])
  
  def cmd_quit(self) -> None:
    raise SystemExit()
  
  def cmd_move(self, x: int, y: int) -> None:
    player = self.active_map.player
    if not self.active_map.is_blocked(*player.relative(x, y)):
      player.move(x, y)
      self.fov_recompute = True