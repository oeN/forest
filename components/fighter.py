from typing import Tuple, Optional

class Fighter:
    name: str = "<Unnamed>"
    char: int = ord("!")
    color: Tuple[int, int, int] = (255, 255, 255)

    hp: int = 0
    power: int = 0
    defense: int = 0

    def __init__(self) -> None:
        self.max_hp = self.hp

    @property
    def is_dead(self):
      return self.hp == 0


class Player(Fighter):
    name = "You"
    char = ord("@")
    color = (255, 255, 255)

    hp = 30
    power = 5
    defense = 2


class Orc(Fighter):
    name = "Orc"
    char = ord("o")
    color = (63, 127, 63)

    hp = 10
    power = 3
    defense = 0
