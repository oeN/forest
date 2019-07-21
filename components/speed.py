from components import base

class Speed(base.Component, base_component=True):
  """ Define when an entity can take an action """
  speed: int = 0
  speed_limit: int = 100
  acceleration: float = 1.0

  def accelerate(self) -> None:
    self.speed += self.acceleration
    # print(f"current speed {self.speed}")

  @property
  def can_take_action(self) -> bool:
    return self.speed >= self.speed_limit

  def take_action(self, action) -> None:
    if self.can_take_action:
      action()
      # Reset the speed
      self.speed = 0

class Player(Speed):
  speed_limit = 80

class BasicMonster(Speed):
  speed_limit = 100
  # acceleration = 0.1

