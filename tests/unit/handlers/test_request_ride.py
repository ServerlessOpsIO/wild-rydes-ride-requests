'''Test request_ride'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
import json
import os

import pytest

# Need to ensure function environment settings are set before import
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE'] = 'mock_test_request_ride'
DYNAMODB_HASH_KEY = 'RideId'
import handlers.request_ride as h # noqa


EVENT_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    'events',
    'request-ride-event.json'
)


@pytest.fixture
def event() -> dict:
    '''Function trigger event'''
    with open(EVENT_FILE) as f:
        return json.load(f)


@pytest.fixture
def body(event) -> dict:
    '''Event request body'''
    return json.loads(event.get('body'))


@pytest.fixture
def pickup_location(body) -> dict:
    '''Pickup location'''
    return body.get('PickupLocation')


@pytest.fixture
def ride_id() -> str:
    '''Ride Id'''
    return h._generate_ride_id()


@pytest.fixture
def ride(ride_id, unicorn) -> dict:
    '''Unicorn ride item'''
    ride = {
        'RideId': ride_id,
        'Unicorn': unicorn,
        'RequestTime': str(h._get_timestamp_from_uuid(ride_id))
    }

    return ride


@pytest.fixture
def unicorn() -> dict:
    '''Random unicorn'''
    unicorn = {
        'Name': 'TestUnicorn',
        'Color': 'Golden',
    }
    return unicorn


def test__get_pickup_location(body, pickup_location):
    '''Return pickup location from event'''
    this_pl = h._get_pickup_location(body)
    assert this_pl == pickup_location


@pytest.mark.skip(reason="Need to figure out how to mock calls to _get_unicorn()")
def test__get_ride(pickup_location):
    '''test _get_ride'''
    this_ride = h._get_ride(pickup_location)
    # Just checking the shape of the response
    assert 'RideId' in this_ride.keys()
    assert 'Unicorn' in this_ride.keys()
    assert 'RequestTime' in this_ride.keys()


@pytest.mark.skip(reason="Need to figure out how to mock calls to _get_unicorn()")
def test__get_unicorn():
    '''test _get_ride'''
    this_unicorn = h._get_unicorn()
    # Just checking the shape of the response
    assert 'Name' in this_unicorn.keys()
    assert 'Color' in this_unicorn.keys()

