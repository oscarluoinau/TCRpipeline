from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest

import time
import json
import yaml
import base64
import paramiko

# Initialize AcsClient instance
client = AcsClient(
        "",
        "",
        "cn-shenzhen"
);

# Create instance
request = CreateInstanceRequest.CreateInstanceRequest()
request.set_ImageId("m-wz9dnmzrres9mycrl3ue")
request.set_InstanceName("TCR-test")
request.set_InstanceType("ecs.g5.large")
request.set_InternetChargeType("PostPaid")
request.set_SecurityGroupId("sg-wz90k8rmm9ch1bxd816t")
#request.set_ClientToken("<uuid>")
request.set_Password("CSiRO2113!")
request.set_InternetChargeType("PayByTraffic")
request.set_InternetMaxBandwidthOut('5')
response = client.do_action_with_exception(request)
print response

request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(10)
response = client.do_action_with_exception(request)
json_data = json.loads(response)
json_data = yaml.safe_load(response)
instanceID = json_data['Instances']['Instance'][0]['InstanceId']

# Allocate public IP
request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
request.set_InstanceId(instanceID)
response = client.do_action_with_exception(request)
print response

# Start instance
request = StartInstanceRequest.StartInstanceRequest()
request.set_InstanceId(instanceID)
response = client.do_action_with_exception(request)
print response
