import boto3
import sys
from datetime import datetime, timedelta

client = boto3.client('cloudwatch')
response = client.get_metric_statistics(
    Namespace='http_request',
    MetricName='http',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-02f11052f0b309e20'
        },
    ],
    StartTime=datetime(2019, 3, 17,18,25) ,
    EndTime=datetime(2019, 3, 18),
    Period=60,
    Statistics=[
        'Maximum',
    ],
    Unit='Count/Second'
)
for k in response['Datapoints']:
    print(k)