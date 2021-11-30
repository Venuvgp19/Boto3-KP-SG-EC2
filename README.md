# Boto3-KP-SG-EC2
This module uses boto3 library to interact with AWS and create resources.

Requirement

    awscli setup on your local machine. check link https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

What it does?
 1) It creates a KeyPair
 2) It create a security group and adds ingress and egress rules
 3) It finally creates and Amazon Ec2 machine and attaches the security group to it and downloads the Keypair to do the ssh to the server.

## clone the project
    git clone https://github.com/Venuvgp19/Boto3-KP-SG-EC2.git
    
## navigate to the Directory and execute the script.
    (venu) (base) [root@wppljmp001 Boto3-KP-SG-EC2]# python Create_EC2.py
    Enter Key pair name : KP1
    Creating Keypair.......
    Enter the sg name : ec2-ssh
    Creating Security Group.....
    Egress for SG ec2-ssh already defined
    EC2 instace with ID i-00fa463f2039b4800 has been created on AWS and downloaded keypair in the current working directory
    
    
Note : if you execute the script again with same keypair name and security group name one more server will be spinned up.
