import tcod
import tcod.event

from game_map import GameMap
from session import Session

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

  def __init__(self, session: Session):
    self.session = session

  @property
  def active_map(self) -> GameMap:
    return self.session.active_map

  def run(self, console: tcod.console.Console) -> None:
    while True:
      self.on_draw(console)
      tcod.console_flush()

      for event in tcod.event.wait():
        self.dispatch(event)

  def on_draw(self, console: tcod.console.Console) -> None:
    console.clear()
    self.active_map.render(console)

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
    target = self.active_map.entity_at(*player.relative(x, y))
    if not self.active_map.is_blocked(*player.relative(x, y)):
      player.move(x, y)
      self.active_map.update_fov()
    elif target:
      player.attack(target)
    self.session.enemy_turn()
