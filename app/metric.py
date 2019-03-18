import boto3
import botocore
from datetime import datetime, timedelta
import os
from flask import render_template, session, request, redirect, url_for, g
import sys
from threading import Thread
import sched
import time
from app import webapp
command='wget -q -O - http://169.254.169.254/latest/meta-data/instance-id'
instance_id=os.popen(command).read().strip()
def start():
    storepath = 'app/static/'
    txtname = 'request.txt'
    dest = os.path.join(storepath, txtname)
    text=open(dest,'r')
    RQ=text.read()
    value=float(RQ)
    print(value)

    return value
def uploadrequest(value):
    client = boto3.client('cloudwatch')
    response = client.put_metric_data(
        Namespace='http_request',
        MetricData=[
            {
                'MetricName': 'http',
                'Dimensions': [
                    {
                        'Name': 'InstanceId',
                        'Value':instance_id
                    },
                ],
                'Timestamp': datetime.now(),
                'StatisticValues': {
                    'SampleCount': 60,
                    'Sum': 234,
                    'Minimum': 0,
                    'Maximum': value
                },
                'Unit': 'Count/Second',
                'StorageResolution': 60
            },
        ]
    )




# This scheduler trigger every 10 seconds to update the cpu and http information
refresh_scheduler = sched.scheduler(time.time, time.sleep)


def init():
    thread1 = Thread(target=run_scheduler, args=(0, refresh_event, refresh_scheduler))
    thread1.start()
@webapp.route('/request', methods=['GET', 'POST'])
def refresh_event(scheduler):
    value = start()
    uploadrequest(value)
    refresh_scheduler.enter(60, 1, refresh_event, (scheduler,))

def run_scheduler(start_time, event, scheduler):
    scheduler.enter(start_time, 1, event, (scheduler,))
    scheduler.run()