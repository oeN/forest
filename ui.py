from __future__ import annotations

from typing import Tuple, List
from session import Session
from components.fighter import Fighter
import tcod

def render_ui(console: tcod.console.Console, session: Session) -> None:
  bar_width = 20
  player = session.player

  # Render player HP bar
  hp = player[Fighter].hp
  max_hp = player[Fighter].max_hp
  render_bar(
    console,
    1,
    console.height - 2,
    bar_width,
    f"HP: {hp:02}/{max_hp:02}",
    hp / max_hp,
    (0x40, 0x80, 0),
    (0x80, 0, 0)
  )

  render_logs_window(console, bar_width + 2, console.height, session.log)

def render_bar(
  console: tcod.console.Console,
  x: int,
  y: int,
  width: int,
  text: str,
  fullness: float,
  fg: Tuple[int, int, int],
  bg: Tuple[int, int, int]
) -> None:
  console.print(x, y, text.center(width)[:width], fg=(255, 255, 255))
  bar_bg = console.tiles["bg"][x : x + width, y]
  bar_bg[:, :3] = bg
  fill_width = max(0, min(width, int(fullness * width)))
  bar_bg[:fill_width, :3] = fg

def render_logs_window(
  console: tcod.console.Console,
  x: int,
  y: int,
  logs: List[str]
) -> None:
  log_width = console.width - x
  i = 0
  for text in logs[::-1]:
    i += tcod.console.get_height_rect(log_width, text)
    if i >= 7:
      break
    console.print_box(x, y - i, log_width, 0, text)
