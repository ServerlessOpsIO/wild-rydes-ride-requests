'''Request a ride'''

import datetime
import logging
import json
import os
import random
import string

import boto3

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type:ignore
_logger = logging.getLogger(__name__)

# DynamoDB
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')
dynamodb = boto3.resource('dynamodb')
ddt = dynamodb.Table(DYNAMODB_TABLE)

FLEET = [
    {
        'Name': 'Bucephalus',
        'Color': 'Golden',
        'Gender': 'Male',
    },
    {
        'Name': 'Shadowfax',
        'Color': 'White',
        'Gender': 'Male',
    },
    {
        'Name': 'Rocinante',
        'Color': 'Yellow',
        'Gender': 'Female',
    },

]


def _get_ride(pickup_location):
    '''Get a ride.'''
    ride_id = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(16))
    unicorn = _get_unicorn()

    # NOTE: upstream they replace Rider with User but that seems silly.
    resp = {
        'RideId': ride_id,
        'Unicorn': unicorn,
        'UnicornName': unicorn.get('Name'),
        'RequestTime': str(datetime.datetime.now()),
    }
    return resp


def _get_unicorn():
    '''Return a unicorn from the fleet'''
    return FLEET[random.randint(0, len(FLEET) - 1)]


def _get_pickup_location(body):
    '''Return pickup location from event'''
    return body.get('PickupLocation')


def handler(event, context):
    '''Function entry'''
    _logger.debug('Request: {}'.format(json.dumps(event)))

    body = json.loads(event.get('body'))
    pickup_location = _get_pickup_location(body)
    ride_resp = _get_ride(pickup_location)

    resp = {
        'statusCode': 201,
        'body': json.dumps(ride_resp),
        'headers': {
            "Access-Control-Allow-Origin": "*",
        }
    }

    return resp

