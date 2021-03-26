from __future__ import unicode_literals
from boto3 import Session
from moto.core import BaseBackend, BaseModel
from collections import OrderedDict
from datetime import date

class Container(BaseModel):
    def __init__(self, *args, **kwargs):
        self.arn = kwargs.get("arn")
        self.name = kwargs.get("name")
        self.endpoint = kwargs.get("endpoint")
        self.status = kwargs.get("status")
        self.creation_time = kwargs.get("creation_time")

    def to_dict(self, exclude=None):
        data = {
            "arn": self.arn,
            "name": self.name,
            "endpoint": self.endpoint,
            "status": self.status,
            "creation_time": self.creation_time,
        }
        if exclude:
            for key in exclude:
                del data[key]
        return data
    
class MediaStoreBackend(BaseBackend):
    def __init__(self, region_name=None):
        super(MediaStoreBackend, self).__init__()
        self.region_name = region_name

    def reset(self):
        region_name = self.region_name
        self.__dict__ = {}
        self.__init__(region_name)
        self._containers = OrderedDict()

    def create_container(self, name, tags):
        arn = "arn:aws:mediastore:container:{}".format(name)
        container = Container(
            arn=arn,
            name=name,
            endpoint="/{}".format(name),
            status="CREATING",
            creation_time=date.today()
        )
        self._containers[id] = container
        return channel


mediastore_backends = {}
for region in Session().get_available_regions("mediastore"):
    mediastore_backends[region] = MediaStoreBackend()
for region in Session().get_available_regions("mediastore", partition_name="aws-us-gov"):
    mediastore_backends[region] = MediaStoreBackend()
for region in Session().get_available_regions("mediastore", partition_name="aws-cn"):
    mediastore_backends[region] = MediaStoreBackend()