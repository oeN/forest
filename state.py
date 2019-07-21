import tcod
import tcod.event

from game_map import GameMap
from session import Session
from components.location import Location
from components.fighter import Fighter
from components.ai import AI
from components.speed import Speed
from entity import Entity
from systems import movement
from ui import render_ui

class Accelerate(tcod.event.Event):
  type = 'ACCELERATE'
  entity: Entity

  def __init__(self, entity: Entity = None):
    super().__init__()
    self.entity = entity

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
      self.dispatch(Accelerate())

      for event in tcod.event.wait():
        print(event)
        self.dispatch(event)

  def on_draw(self, console: tcod.console.Console) -> None:
    console.clear()
    self.active_map.render(console)
    render_ui(console, self.session)

  def ev_quit(self, event: tcod.event.Quit) -> None:
    self.cmd_quit()

  def ev_keydown(self, event: tcod.event.KeyDown) -> None:
    if event.sym in self.COMMAND_KEYS:
      getattr(self, "cmd_%s" % event.sym)()
    elif event.sym in self.MOVE_KEYS:
      self.cmd_move(*self.MOVE_KEYS[event.sym])

  def accelerate_entity(self, entity: Entity) -> None:
    entity[Speed].accelerate()
    if not entity[Speed].can_take_action:
      self.dispatch(Accelerate(entity))
    elif AI in entity:
      entity[Speed].take_action(lambda: entity[AI].take_turn(entity))
      # self.dispatch(Accelerate(entity))

  def ev_accelerate(self, event: Accelerate) -> None:
    if event.entity:
      self.accelerate_entity(event.entity)
      return

    for entity in self.active_map.entities:
      if Speed not in entity:
        next
      self.accelerate_entity(entity)

  def cmd_quit(self) -> None:
    raise SystemExit()

  def cmd_move(self, x: int, y: int) -> None:
    player = self.session.player
    player[Speed].take_action(lambda: movement.move(player, (x, y)))
    # self.session.enemy_turn()
