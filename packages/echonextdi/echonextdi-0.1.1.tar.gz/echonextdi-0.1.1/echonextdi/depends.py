from typing import Any, Dict, Optional, Type, TypeVar
from echonextdi.containers.container import Container

T = TypeVar("T")


class Depends:
	def __init__(self, container: Container, dependency: Type[T]):
		self.container = container
		self.dependency = dependency

	def __call__(self):
		return self.container.resolve(self.dependency)
