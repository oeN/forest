import tcod
import tcod.event

from game_map import GameMap
from session import Session
from components.location import Location
from components.fighter import Fighter

def attack(actor, target) -> None:
  assert actor[Location].distance_to(target[Location]) <= 1

  damage = actor[Fighter].power - target[Fighter].defense

  attack_direction = f"{actor[Fighter].name} attacks {target[Fighter].name}"

  if damage > 0:
    target[Fighter].hp -= damage
    print(f"{attack_direction} for {damage} hit points")
  else:
    print(f"{attack_direction} without consequences")
  if target[Fighter].hp <= 0:
    print(f"The {target[Fighter].name} dies")

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
    destination = player[Location].relative(x, y)
    target = self.active_map.entity_at(*destination)
    if not self.active_map.is_blocked(*destination):
      player[Location] = self.active_map[destination]
      self.active_map.update_fov()
    elif target:
      attack(player, target)
    self.session.enemy_turn()
