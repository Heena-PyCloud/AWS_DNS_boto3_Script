from datetime import datetime
import boto3

client = boto3.client('route53', aws_access_key_id="****", aws_secret_access_key="****") #Enter your access key and secret access key
aws_region = "US"
def hosted_zone():
   response = client.create_hosted_zone(
   Name='max.com',
   VPC={
        'VPCRegion': 'us-east-1', #Etter your VPC Region and Id.
        'VPCId': 'vpc-23117123'
    },
    CallerReference='Max' + datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p"),
    HostedZoneConfig={
        'Comment': 'For Max Migration',
        'PrivateZone': True
    },
)

print("Creating Hosted zone in Route53")


def get_zone_id():
    domain='max.com.'  #Enter your domain 
    zones = client.list_hosted_zones_by_name(DNSName=domain)
    if not zones or len(zones['HostedZones']) == 0:
       raise Exception("Could not find DNS zone to update")
    zone_id = zones['HostedZones'][0]['Id']
    return zone_id

def a_record():
   ip= '192.0.1.00'  #Enter ip address
   if aws_region == "US":
    #US is my default region. So cont_code is blank
      cont_code = {}
   elif aws_region == "EU":
      cont_code = {'ContinentCode':'EU'}
   elif aws_region == "AP":
      cont_code = {'ContinentCode':'AS'}
   response = client.change_resource_record_sets(
       HostedZoneId = get_zone_id(),
       ChangeBatch={
           'Comment': 'For Maximus Migration',
           'Changes': [
               {
                   'Action': 'CREATE',
                    'ResourceRecordSet': {
                    'Name': 'max.com.',
                    'Type': 'A',
                    'SetIdentifier': 'Max_A_record',
                    'GeoLocation': cont_code,
                    'TTL': 60,
                    'ResourceRecords': [
                        {
                            'Value': ip
                        },
                        ],
                    }
            },
            ]
    }
)
def add_cname_record():
    try:
        response = client.change_resource_record_sets(
        HostedZoneId=get_zone_id(),

        ChangeBatch= {
                        'Comment': 'Create cname for max',
                        'Changes': [
                            {
                             'Action': 'CREATE',
                             'ResourceRecordSet': {
                                 'Name': 'test.max.com.',
                                 'Type': 'CNAME',
                                 'TTL': 300,
                                 'ResourceRecords': [{'Value': 'max.com.'}]
                            }
                        }]
        })
    except Exception as e:
        print(e)



hosted_zone()
a_record()
add_cname_record()

