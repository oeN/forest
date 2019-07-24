from entity import Entity

from components import fighter, ai, sprite, location, item

player = lambda: Entity((fighter.Player(), sprite.Player()))

monsters = {
  'orc': lambda: Entity((
    fighter.Orc(),
    sprite.Orc(),
    ai.BasicMonster()
  ))
}

items = {
  'healing_potiont': lambda: Entity((
    item.HealingPotiont(),
    sprite.HealingPotiont()
  ))
}
