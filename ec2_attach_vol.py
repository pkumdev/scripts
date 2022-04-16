
"""
    script to attach ec2 volume
    1. Attach the volume to current ec2 instance
    2. Check if volume is already a xfs , if not create one
    3. Mount it
"""




import json
import boto3
import json
import requests
import os, subprocess, sys
from time import sleep

try:
    volume_id = sys.argv[1]
except IndexError:
    print('please provide volume id as argument')
    sys.exit(1)

resp_instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = resp_instance_id.text


client = boto3.client('ec2', region_name='ap-south-1')

while True:
    volume_info  = client.describe_volumes(Filters=[{'Name':'attachment.instance-id', 'Values':[instance_id]},
                                    {'Name':'attachment.status','Values':['attached']},
                                    {'Name':'volume-id','Values':[volume_id]}])
    volumes = volume_info['Volumes']
    
    if len(volumes) == 0:
        print('volume not mounted')
    
    elif len(volumes) == 1:
        subprocess.run(['mount','/dev/nvme1n1','/newvolume']) 
        print('volume mounted;exiting')
        break
    else:
        print('some error occured; volume already mounted to other instance or we do not know what happened')
    sleep(10)



# to view all volumes : lsblk
# to create fs out of volume , only for newly created volueme and to be run only once: 
     #sudo mkfs -t xfs /dev/xvdf
#
#
#
#
#
