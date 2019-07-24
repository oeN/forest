from __future__ import annotations

from typing import Tuple, Any, Dict, Iterable, Type, TypeVar, TYPE_CHECKING
import tcod

if TYPE_CHECKING:
  from components.base import Component

T = TypeVar("T")


class Entity:
  def __init__(self, components: Iterable[Component] = ()):
    self._components: Dict[Any, Any] = {}
    for component in components:
      self[component.component_type] = component

  def __getitem__(self, key: Type[T]) -> T:
    component: T = self._components[key]
    return component

  def __setitem__(self, key: Type[T], value: T) -> None:
    self._components[key] = value

  def __contains__(self, key: Type[T]) -> bool:
    return key in self._components
