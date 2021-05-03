import boto3
def assume_role(accountid,rolename):
    try:
        print("entro a assume role")
        sts = boto3.client('sts')
        roleasumir = "arn:aws:iam::" + accountid + ':role/'+ rolename
        assumed_role_object=sts.assume_role(
            RoleArn=roleasumir,
            RoleSessionName=rolename
        )
        credentials=assumed_role_object['Credentials']
        print("salio de asume role")
        return credentials
    except Exception as e:
        print('Cant assume role %s'% e)

def conex_dynamo():
    try:
        rolename = 'aws-ec2-role'
        accountid = '463217511710'
        
        credentials = assume_role(accountid, rolename)
        client = boto3.client(
            'dynamodb',
            region_name='us-east-1',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )

        return client
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
