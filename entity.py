class Entity:
  """
  A generic object to represent players, enemies, items, etc.
  """
  def __init__(self, x, y, char, color):
    self.x = x
    self.y = y
    self.char = char
    self.color = color
  
  def relative(self, x: int, y: int):
    return self.x + x, self.y + y

  def move(self, x: int, y: int) -> None:
    # Move the entity by a given amount
    self.x, self.y = self.relative(x, y)