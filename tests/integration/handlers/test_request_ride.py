'''Integration tests for request-ride-event'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
import json
import os

import boto3
from botocore.vendored import requests
import pytest

EVENT_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    'events',
    'request-ride-event.json'
)

STACK_NAME = 'wild-rydes-ride-requests-dev'
ENDPOINT_OUTPUT_NAME = 'RequestRideUrl'


def _get_output_value_from_cfn(stack_name, output_key):
    '''Get an aoutput from a stack'''
    cfn = boto3.client('cloudformation')
    stacks = cfn.describe_stacks()

    for s in stacks.get('Stacks'):
        if s.get('StackName') == stack_name:
            stack = s
            break
    assert stack is not None

    for output in stack.get('Outputs'):
        if output.get('OutputKey') == output_key:
            value = output.get('OutputValue')

    return value


@pytest.fixture
def request_data() -> str:
    '''Function trigger event'''
    with open(EVENT_FILE) as f:
        return json.load(f).get('body')


@pytest.fixture
def website_url() -> str:
    '''website URL'''
    site_url = _get_output_value_from_cfn(
        STACK_NAME,
        ENDPOINT_OUTPUT_NAME
    )
    assert site_url is not None
    return site_url


def test_request_ride_endpoint(website_url, request_data):
    '''test API gateway + lambda integration'''
    resp = requests.post(website_url, data=request_data)

    # Check status code
    assert resp.status_code == 201

    # Check we have appropriate response data
    j = resp.json()
    assert j.get('RideId') is not None
    assert j.get('Unicorn') is not None
    assert j.get('RequestTime') is not None


