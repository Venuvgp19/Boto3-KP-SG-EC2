import os
import json
import time
import boto3
import botocore


class EC2:
    def __init__(self,ec2):
        self.ec2 = ec2
   
    def create_keypair(self,name):
        try :
            print('Creating Keypair.......')
            kp = self.ec2.create_key_pair(KeyName = '%s'%name)
            with open('%s'%name + '.pem','w') as file:
                file.write(kp['KeyMaterial'])
        except botocore.exceptions.ClientError:
            print(f'KeyPair {name} already exists')
        return None
    
    def GetKpId(self,name):
        response = self.ec2.describe_key_pairs()
        kid = [response['KeyPairs'][x]['KeyPairId']  for x in range(len(response['KeyPairs'])) if response['KeyPairs'][x]['KeyName'] == '%s'%name]
        return kid[0]
    
    def CreateSecGrp(self,SgName):
        try:
            print('Creating Security Group.....')
            Sg = self.ec2.create_security_group(
    		Description='ec2 security group',
    		GroupName='%s'%SgName,
                DryRun = False
             )
        except botocore.exceptions.ClientError:
            #raise Security_group_Error('botocore.exceptions.ClientError','sg already exists')
            print(f'SG {SgName} already exists')
        finally: 
            response = self.ec2.describe_security_groups(
                GroupNames = ['%s'%SgName]
        )
            group_id = response['SecurityGroups'][0]['GroupId']
        return str(group_id)    

    def define_egress_sg(self,sgid):
        sg = self.ec2.SecurityGroup(sgid)
        response = sg.authorize_egress(
        DryRun=False,
        IpPermissions=[
        {
            'IpProtocol': '-1',
            'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'allow access to the internet'
                },
            ],
            'UserIdGroupPairs': [
                {
                    'GroupId': '%s'%sgid,
                },
            ]
        },
        ],
        )
        return response
    
    def define_ingress_sg(self,sgid):
        sg = self.ec2.SecurityGroup(sgid)
        resp = sg.authorize_ingress(
        IpPermissions=[
        {
            'FromPort': 22,
            'IpProtocol': 'tcp',
            'ToPort' : 22,
            'IpRanges' : [{'CidrIp' : '0.0.0.0/0'}]
        }
        ]
        )
        return(resp)

    def Create_EC2(self,kpname,sgid):
        instance = self.ec2.create_instances(
        ImageId='ami-0108d6a82a783b352',
        InstanceType='t2.micro',
        KeyName='%s'%kpname,
        MaxCount=1,
        MinCount=1,
        Monitoring={
        'Enabled': False
        },
        SecurityGroupIds=[
        '%s'%sgid,
        ],
        DryRun=False,
        InstanceInitiatedShutdownBehavior='terminate',
        )
        time.sleep(10)
        return(instance[0])

    def GetDnsName(self,instid):
        resp = self.ec2.describe_instances(
           InstanceIds = ['%s'%instid]
        )
        return resp
        
if __name__ == '__main__':
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    clt = EC2(ec2_client)
    res = EC2(ec2_resource)
    kpname = input("Enter Key pair name : ")
    kp = clt.create_keypair(kpname)
    Kpid = clt.GetKpId(kpname)
    sg_name = input("Enter the sg name : ")
    Sgid = clt.CreateSecGrp(sg_name)
    try :
        print(res.define_egress_sg(Sgid))    
    except botocore.exceptions.ClientError:
        print(f'Egress for SG {sg_name} already defined')
    try :
        print(res.define_ingress_sg(Sgid))
    except botocore.exceptions.ClientError:
        print(f'Ingress for SG {sg_name} already defined')
    
    instid = res.Create_EC2(kpname,Sgid)
    print(f'EC2 instace with ID {instid.id} has been created on AWS and downloaded keypair in the current working directory')
