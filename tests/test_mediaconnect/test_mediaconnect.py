from __future__ import unicode_literals

import boto3
import sure  # noqa
from moto import mock_mediaconnect


region = "eu-west-1"


def _create_flow_config(name, **kwargs):
    availability_zone = kwargs.get("availability_zone", "AZ1")
    entitlements = kwargs.get(
        "entitlements",
        [
            {
                "DataTransferSubscriberFeePercent": 12,
                "Description": "An entitlement",
                "Encryption": {"Algorithm": "aes256", "RoleArn": "some:role"},
                "EntitlementStatus": "ENABLED",
                "Name": "Entitlement A",
                "Subscribers": [],
            }
        ],
    )
    outputs = kwargs.get("outputs", [{"Name": "Output 1", "Protocol": "zixi-push"}])
    source = kwargs.get(
        "source",
        {
            "Decryption": {"Algorithm": "aes256", "RoleArn": "some:role"},
            "Description": "A source",
            "Name": "Source A",
        },
    )
    source_failover_config = kwargs.get("source_failover_config", {})
    sources = kwargs.get("sources", [])
    vpc_interfaces = kwargs.get("vpc_interfaces", [])
    flow_config = dict(
        AvailabilityZone=availability_zone,
        Entitlements=entitlements,
        Name=name,
        Outputs=outputs,
        Source=source,
        SourceFailoverConfig=source_failover_config,
        Sources=sources,
        VpcInterfaces=vpc_interfaces,
    )
    return flow_config


@mock_mediaconnect
def test_create_flow_succeeds():
    client = boto3.client("mediaconnect", region_name=region)
    flow_config = _create_flow_config("test Flow 1")

    response = client.create_flow(**flow_config)

    response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    response["Flow"]["FlowArn"][:26].should.equal("arn:aws:mediaconnect:flow:")
    response["Flow"]["Name"].should.equal("test Flow 1")
    response["Flow"]["Status"].should.equal("STANDBY")
    response["Flow"]["Sources"][0][
        "SourceArn"
    ] == "arn:aws:mediaconnect:source:Source A"


@mock_mediaconnect
def test_list_flows_succeeds():
    client = boto3.client("mediaconnect", region_name=region)
    flow_1_config = _create_flow_config("test Flow 1")
    flow_2_config = _create_flow_config("test Flow 2")

    client.create_flow(**flow_1_config)
    client.create_flow(**flow_2_config)

    response = client.list_flows()
    len(response["Flows"]).should.equal(2)

    response["Flows"][0]["Name"].should.equal("test Flow 1")
    response["Flows"][0]["AvailabilityZone"].should.equal("AZ1")
    response["Flows"][0]["SourceType"].should.equal("OWNED")
    response["Flows"][0]["Status"].should.equal("STANDBY")

    response["Flows"][1]["Name"].should.equal("test Flow 2")
    response["Flows"][1]["AvailabilityZone"].should.equal("AZ1")
    response["Flows"][1]["SourceType"].should.equal("OWNED")
    response["Flows"][1]["Status"].should.equal("STANDBY")


@mock_mediaconnect
def test_describe_flow_succeeds():
    client = boto3.client("mediaconnect", region_name=region)
    flow_config = _create_flow_config("test Flow 1")

    create_response = client.create_flow(**flow_config)
    create_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    flow_arn = create_response["Flow"]["FlowArn"]
    describe_response = client.describe_flow(FlowArn=flow_arn)
    describe_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    describe_response["Flow"]["Name"].should.equal("test Flow 1")


@mock_mediaconnect
def test_delete_flow_succeeds():
    client = boto3.client("mediaconnect", region_name=region)
    flow_config = _create_flow_config("test Flow 1")

    create_response = client.create_flow(**flow_config)
    create_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    flow_arn = create_response["Flow"]["FlowArn"]
    delete_response = client.delete_flow(FlowArn=flow_arn)
    delete_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    delete_response["FlowArn"].should.equal(flow_arn)
    delete_response["Status"].should.equal("STANDBY")


@mock_mediaconnect
def test_start_stop_flow_succeeds():
    client = boto3.client("mediaconnect", region_name=region)
    flow_config = _create_flow_config("test Flow 1")

    create_response = client.create_flow(**flow_config)
    create_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    create_response["Flow"]["Status"].should.equal("STANDBY")
    flow_arn = create_response["Flow"]["FlowArn"]

    start_response = client.start_flow(FlowArn=flow_arn)
    start_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    start_response["FlowArn"].should.equal(flow_arn)
    start_response["Status"].should.equal("STARTING")

    describe_response = client.describe_flow(FlowArn=flow_arn)
    describe_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    describe_response["Flow"]["Status"].should.equal("ACTIVE")

    stop_response = client.stop_flow(FlowArn=flow_arn)
    stop_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    stop_response["FlowArn"].should.equal(flow_arn)
    stop_response["Status"].should.equal("STOPPING")

    describe_response = client.describe_flow(FlowArn=flow_arn)
    describe_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    describe_response["Flow"]["Status"].should.equal("STANDBY")


@mock_mediaconnect
def test_tag_resource_succeeds():
    client = boto3.client("mediaconnect", region_name=region)

    tag_response = client.tag_resource(ResourceArn="some-arn", Tags={"Tag1": "Value1"})
    tag_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)

    list_response = client.list_tags_for_resource(ResourceArn="some-arn")
    list_response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    list_response["Tags"].should.equal({"Tag1": "Value1"})

@mock_mediaconnect
def test_add_flow_outputs_succeeds():
    client = boto3.client("mediaconnect", region_name=region)

    flow_config = _create_flow_config("test-flow")
    flow = client.create_flow(**flow_config)
    flow["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    flow_arn =flow["Flow"]["FlowArn"]
    flow["Flow"]["Outputs"].should.equal([{'Name': 'Output 1'}])
    response = client.add_flow_outputs(
        FlowArn=flow_arn,
        Outputs=[{"Name":"Output 2", "Protocol": "zixi-push"}]
    )
    response["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    response["Outputs"].should.equal([{'Name': 'Output 1'}, {'Name': 'Output 2'}])
    response = client.remove_flow_output(
        FlowArn=flow_arn,
        OutputArn=response["Outputs"]["OutputArn"]
    )
    response["Outputs"].should.equal([{'Name': 'Output 1'}])
    # response["Outputs"].should.equal([{'Name': 'Output 1', 'Protocol': 'zixi-push'}, {'Name': 'Output 2', 'Protocol': 'zixi-push'}])

# @mock_mediaconnect
# def test_remove_flow_outputs_succeeds():
#     client = boto3.client("mediaconnect", region_name=region)

#     flow_config = _create_flow_config("test-flow")
#     flow = client.create_flow(**flow_config)
#     response["Outputs"].should.equal([{'Name': 'Output 1'}

@mock_mediaconnect
def test_update_flow_output_succeeds():
    client = boto3.client("mediaconnect", region_name=region)

    flow_config = _create_flow_config("test-flow")
    flow = client.create_flow(**flow_config)
    flow["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    flow_arn =flow["Flow"]["FlowArn"]
    print(flow)
    print (flow["Flow"]["Outputs"])
    output_arn = flow["Flow"]["Outputs"]["OutputArn"]
    output["Name"].should.equal('Output 1')
    flow["Flow"]["Outputs"]["Name"].should.equal('Output 1')

    response = client.update_flow_output(
        CidrAllowList=["allow-list"],
        Description="output-description",
        Destination="output-destination",
        Encryption={"Url":"url"},
        FlowArn=flow_arn,
        MaxLatency=123,
        OutputArn=output_arn,
        Port=123,
        Protocol="rtp-fec",
        RemoteId="remote-id",
        SmoothingLatency=123,
        StreamId="stream-id",
        VpcInterfaceAttachment={'VpcInterfaceName': 'vpc-interface-name'},  
    )

    print(response)
    print(res)
