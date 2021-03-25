from __future__ import unicode_literals
from moto.core.responses import BaseResponse
from .models import mediastore_backends
import json


class MediaStoreResponse(BaseResponse):
    SERVICE_NAME = 'mediastore'
    @property
    def mediastore_backend(self):
        return mediastore_backends[self.region]

    
    def put_lifecycle_policy(self):
        container_name = self._get_param("ContainerName")
        lifecycle_policy = self._get_param("LifecyclePolicy")
        policy = self.mediastore_backend.put_lifecycle_policy(
            container_name=container_name,
            lifecycle_policy=lifecycle_policy,
        )
        return json.dumps(policy.to_dict())


# add templates from here
