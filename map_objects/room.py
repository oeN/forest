from typing import List, Optional, Tuple, Type
import numpy as np

class Room:
  def __init__(self, x, y, w, h) -> None:
    self.x1, self.y1 = x, y
    self.x2 = x + w
    self.y2 = y + h

  @property
  def inner(self) -> Tuple[slice, slice]:
    """Return the NumPy index for the inner room area."""
    index: Tuple[slice, slice] = np.s_[
      self.x1 + 1 : self.x2 - 1, self.y1 + 1 : self.y2 - 1
    ]
    return index
  
  @property
  def center(self) -> Tuple[int, int]:
    return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

  def intersects(self, other) -> bool:
    # returns true if this rectangle intersects with another one
    return (
      self.x1 <= other.x2 and self.x2 >= other.x1 and
      self.y1 <= other.y2 and self.y2 >= other.y1
    )