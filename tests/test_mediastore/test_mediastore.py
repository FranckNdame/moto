from __future__ import unicode_literals

import boto3
import sure  # noqa
from moto import mock_mediastore
from botocore.exceptions import ClientError

# from moto.mediastore.exceptions import ResourceNotFoundException

region = "eu-west-1"


@mock_mediastore
def test_create_container_succeeds():
    client = boto3.client("mediastore", region_name=region)
    response = client.create_container(
        ContainerName="Awesome container!", Tags=[{"Key": "customer"}]
    )
    container = response["Container"]
    response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    container["ARN"].should.equal(
        "arn:aws:mediastore:container:{}".format(container["Name"])
    )
    container["Name"].should.equal("Awesome container!")
    container["Status"].should.equal("CREATING")


@mock_mediastore
def test_describe_container_succeeds():
    client = boto3.client("mediastore", region_name=region)
    create_response = client.create_container(
        ContainerName="Awesome container!", Tags=[{"Key": "customer"}]
    )
    container_name = create_response["Container"]["Name"]
    response = client.describe_container(ContainerName=container_name)
    response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    container = response["Container"]
    container["ARN"].should.equal(
        "arn:aws:mediastore:container:{}".format(container["Name"])
    )
    container["Name"].should.equal("Awesome container!")
    container["Status"].should.equal("ACTIVE")


@mock_mediastore
def test_put_lifecycle_policy_succeeds():
    client = boto3.client("mediastore", region_name=region)
    container_response = client.create_container(
        ContainerName="container-name", Tags=[{"Key": "customer"}]
    )
    container = container_response["Container"]
    response = client.put_lifecycle_policy(
        ContainerName=container["Name"], LifecyclePolicy="lifecycle-policy"
    )
    response = client.get_lifecycle_policy(ContainerName=container["Name"])
    response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    response["LifecyclePolicy"].should.equal("lifecycle-policy")


@mock_mediastore
def test_put_lifecycle_policy_raises_error_if_container_does_not_exist():
    client = boto3.client("mediastore", region_name=region)
    client.put_lifecycle_policy.when.called_with(
        ContainerName="container-name", LifecyclePolicy="lifecycle-policy"
    ).should.throw(
        ClientError,
        "An error occurred (ResourceNotFoundException) when calling the PutLifecyclePolicy operation: The specified container does not exist",
    )


@mock_mediastore
def test_get_lifecycle_policy_raises_error_if_container_does_not_exist():
    client = boto3.client("mediastore", region_name=region)
    client.get_lifecycle_policy.when.called_with(
        ContainerName="container-name"
    ).should.throw(
        ClientError,
        "An error occurred (ResourceNotFoundException) when calling the GetLifecyclePolicy operation: The specified container does not exist",
    )