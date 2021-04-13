from __future__ import unicode_literals

import json

from moto.core.responses import BaseResponse
from .models import mediaconnect_backends

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote


class MediaConnectResponse(BaseResponse):
    SERVICE_NAME = "mediaconnect"

    @property
    def mediaconnect_backend(self):
        return mediaconnect_backends[self.region]

    def create_flow(self):
        availability_zone = self._get_param("availabilityZone")
        entitlements = self._get_param("entitlements")
        name = self._get_param("name")
        outputs = self._get_param("outputs")
        source = self._get_param("source")
        source_failover_config = self._get_param("sourceFailoverConfig")
        sources = self._get_param("sources")
        vpc_interfaces = self._get_param("vpcInterfaces")
        flow = self.mediaconnect_backend.create_flow(
            availability_zone=availability_zone,
            entitlements=entitlements,
            name=name,
            outputs=outputs,
            source=source,
            source_failover_config=source_failover_config,
            sources=sources,
            vpc_interfaces=vpc_interfaces,
        )
        return json.dumps(dict(flow=flow.to_dict()))

    def list_flows(self):
        max_results = self._get_int_param("maxResults")
        next_token = self._get_param("nextToken")
        flows, next_token = self.mediaconnect_backend.list_flows(
            max_results=max_results, next_token=next_token,
        )
        return json.dumps(dict(flows=flows, nextToken=next_token))

    def describe_flow(self):
        flow_arn = unquote(self._get_param("flowArn"))
        flow, messages = self.mediaconnect_backend.describe_flow(flow_arn=flow_arn,)
        return json.dumps(dict(flow=flow, messages=messages))

    def delete_flow(self):
        flow_arn = unquote(self._get_param("flowArn"))
        flow_arn, status = self.mediaconnect_backend.delete_flow(flow_arn=flow_arn,)
        return json.dumps(dict(flowArn=flow_arn, status=status))

    def start_flow(self):
        flow_arn = unquote(self._get_param("flowArn"))
        flow_arn, status = self.mediaconnect_backend.start_flow(flow_arn=flow_arn,)
        return json.dumps(dict(flowArn=flow_arn, status=status))

    def stop_flow(self):
        flow_arn = unquote(self._get_param("flowArn"))
        flow_arn, status = self.mediaconnect_backend.stop_flow(flow_arn=flow_arn,)
        return json.dumps(dict(flowArn=flow_arn, status=status))

    def tag_resource(self):
        resource_arn = unquote(self._get_param("resourceArn"))
        tags = self._get_param("tags")
        self.mediaconnect_backend.tag_resource(
            resource_arn=resource_arn, tags=tags,
        )
        return json.dumps(dict())

    def list_tags_for_resource(self):
        resource_arn = unquote(self._get_param("resourceArn"))
        tags = self.mediaconnect_backend.list_tags_for_resource(
            resource_arn=resource_arn,
        )
        return json.dumps(dict(tags=tags))
    
    def add_flow_outputs(self):
        flow_arn = unquote(self._get_param("flowArn"))
        outputs = self._get_param("outputs")
        flow_arn, outputs = self.mediaconnect_backend.add_flow_outputs(
            flow_arn=flow_arn,
            new_outputs=outputs,
        )
        return json.dumps(dict(flowArn=flow_arn, outputs=outputs))
        
    
    def remove_flow_output(self):
        flow_arn = self._get_param("flowArn")
        output_arn = self._get_param("outputArn")
        flow_arn, output_arn = self.mediaconnect_backend.remove_flow_output(
            flow_arn=flow_arn,
            output_arn=output_arn,
        )
        return json.dumps(dict(flowArn=flow_arn, outputArn=output_arn))
    
    def update_flow_output(self):
        cidr_allow_list = self._get_list_prefix("CidrAllowList.member")
        description = self._get_param("Description")
        destination = self._get_param("Destination")
        encryption = self._get_param("Encryption")
        flow_arn = self._get_param("FlowArn")
        max_latency = self._get_int_param("MaxLatency")
        output_arn = self._get_param("OutputArn")
        port = self._get_int_param("Port")
        protocol = self._get_param("Protocol")
        remote_id = self._get_param("RemoteId")
        smoothing_latency = self._get_int_param("SmoothingLatency")
        stream_id = self._get_param("StreamId")
        vpc_interface_attachment = self._get_param("VpcInterfaceAttachment")
        flow_arn, output = self.mediaconnect_backend.update_flow_output(
            cidr_allow_list=cidr_allow_list,
            description=description,
            destination=destination,
            encryption=encryption,
            flow_arn=flow_arn,
            max_latency=max_latency,
            output_arn=output_arn,
            port=port,
            protocol=protocol,
            remote_id=remote_id,
            smoothing_latency=smoothing_latency,
            stream_id=stream_id,
            vpc_interface_attachment=vpc_interface_attachment,
        )
        # TODO: adjust response
        return json.dumps(dict(flowArn=flow_arn, output=output))
