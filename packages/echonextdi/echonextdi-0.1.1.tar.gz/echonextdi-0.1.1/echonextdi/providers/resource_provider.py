from typing import Any

from echonextdi.providers.provider import Provider


class ResourceProvider(Provider):
	def __init__(self, resource: Any):
		self.resource = resource

	def __call__(self) -> Any:
		return self.resource
