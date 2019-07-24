from __future__ import annotations
from typing import Tuple, Optional

from components import base
from components.sprite import Sprite

class Item(base.Component, base_component=True):
  value: int = 0

class HealingPotiont(Item):
  value = 10
