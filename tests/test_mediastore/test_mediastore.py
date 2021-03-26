from __future__ import unicode_literals

import boto3
import sure
from moto import mock_mediastore

region = "eu-west-1"


@mock_mediastore
def test_create_channel_succeeds():
    client = boto3.client("mediastore", region_name=region)
    response = client.create_container(name="Awesome container!", tags={"Customer": "moto"})
    response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    response["Arn"].should.equal(
         "arn:aws:mediastore:channel:{}".format(response["Name"])
    )
    response["Name"].should.equal("Awesome container!")
    response["Status"].should.equal("ACTIVE")
    response["Tags"]["Customer"].should.equal("moto")