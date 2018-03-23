'''Request a ride'''

from datetime import datetime
import logging
import json
import os
import random
import uuid

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type:ignore
_logger = logging.getLogger(__name__)

FLEET = [
    {
        'Name': 'Bucephalus',
        'Color': 'Golden',
    },
    {
        'Name': 'Shadowfax',
        'Color': 'White',
    },
    {
        'Name': 'Rocinante',
        'Color': 'Yellow',
    },

]


def _generate_ride_id():
    '''Generate a ride ID.'''
    return uuid.uuid1()


def _get_ride(pickup_location):
    '''Get a ride.'''
    ride_id = _generate_ride_id()
    unicorn = _get_unicorn()

    # NOTE: upstream they replace Rider with User but that seems silly.
    resp = {
        'RideId': str(ride_id),
        'Unicorn': unicorn,
        'RequestTime': str(_get_timestamp_from_uuid(ride_id)),
    }
    return resp


def _get_timestamp_from_uuid(u):
    '''Return a timestamp from the given UUID'''
    return datetime.fromtimestamp((u.time - 0x01b21dd213814000) * 100 / 1e9)


def _get_unicorn():
    '''Return a unicorn from the fleet'''
    # FIXME: would be good to get to a point where we don't fetch the entire table.
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

