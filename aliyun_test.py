from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest

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
request.set_ImageId("m-wz9ar858klloktrfj4ch")
request.set_InstanceName("TCR-test")
request.set_InstanceType("ecs.g5.large")
request.set_InternetChargeType("PostPaid")
request.set_SecurityGroupId("sg-wz90k8rmm9ch1bxd816t")
#request.set_ClientToken("<uuid>")
request.set_KeyPairName("SSHKey")
request.set_InternetChargeType("PayByTraffic")
request.set_InternetMaxBandwidthOut('5')
response = client.do_action_with_exception(request)
print response

# Describe instance and get instance ID
request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(10)
response = client.do_action_with_exception(request)
#json_data = json.loads(response)
json_data = yaml.safe_load(response)
instanceID = json_data['Instances']['Instance'][0]['InstanceId']

# Allocate IP
time.sleep(60)
request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
request.set_InstanceId(instanceID)
response = client.do_action_with_exception(request)
print response

# Start instance
request = StartInstanceRequest.StartInstanceRequest()
request.set_InstanceId(instanceID)
response = client.do_action_with_exception(request)
print response

time.sleep(60)

# Get IP
request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(10)
response = client.do_action_with_exception(request)
#json_data = json.loads(response)
json_data = yaml.safe_load(response)
publicIP = json_data['Instances']['Instance'][0]['PublicIpAddress']['IpAddress']

#print response
print instanceID
print publicIP[0]

server = publicIP[0]
ssh = paramiko.SSHClient()
key = paramiko.RSAKey.from_private_key_file("/Users/luo024/Downloads/SSHKey.pem")
#ssh.load_system_host_keys()
#ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#ssh.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)

print "Connecting to remote ECS"
ssh.connect(server, username='root', pkey=key)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('bash run_migec.sh')
for line in ssh_stdout:
	print(line.strip('\n'))
ssh.close()

# Stop instance
#request = StopInstanceRequest.StopInstanceRequest()
#request.set_InstanceId(instanceID)
#response = client.do_action_with_exception(request)
#print response

# Release instance
request = DeleteInstanceRequest.DeleteInstanceRequest()
request.set_InstanceId(instanceID)
request.set_Force('true')
response = client.do_action_with_exception(request)
print response

