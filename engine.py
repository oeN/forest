import tcod
import tcod.event

from input_handlers import handle_keys
from render_functions import render_all, clear_all

import state
from game_map import GameMap
import map_generator
from session import Session

def main():
  screen_width, screen_height = 80, 50
  map_width, map_height = 80, 45

  tcod.console_set_custom_font('data/arial10x10.png', tcod.FONT_LAYOUT_TCOD)

  with tcod.console_init_root(
    screen_width,
    screen_height,
    'Forest',
    renderer=tcod.RENDERER_SDL2,
    vsync=True,
    order='F'
  ) as console:
    session_ = Session()
    session_.active_map = map_generator.generate(map_width, map_height)
    current_state = state.GameState(session_)
    current_state.run(console)

if __name__ == '__main__':
  main()
