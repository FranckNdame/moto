from __future__ import unicode_literals
from moto.core.responses import BaseResponse
from .models import mediastore_backends
import json


class MediaStoreResponse(BaseResponse):
    SERVICE_NAME = 'mediastore'
    @property
    def mediastore_backend(self):
        return mediastore_backends[self.region]

    def create_container(self):
        name = self._get_param("name")
        tags = self._get_param("tags")
        container = self.mediastore_backend.create_container(name, tags)
        )
        return json.dumps(container.to_dict())