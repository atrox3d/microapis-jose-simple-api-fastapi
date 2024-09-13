from datetime import datetime, timedelta
import datetime as dt
import logging
import json
import uuid

logger = logging.getLogger(__name__)

def get_payload_example():
    return {
        'iss': 'https://auth.coffeemesh.io/',
        'sub': 'fasdf-fasd-fasdf-fasd-fasf',
        'aud': 'http://localhost:8000/orders',
        # 'iat': None,
        # 'exp': None,
        'scope': 'openid'
    }

def load_payload_from_json(payload_json:str) -> dict:
    with open(payload_json) as jp:
        return json.load(jp)

def save_payload_to_json(payload:dict, payload_json:str, indent=2) -> dict:
    with open(payload_json, 'w') as jp:
        return json.dump(payload, jp, indent=indent)

def add_time_to_payload(payload:dict, **timedelta_params) -> dict:
    ''' adds current iat and exp fields to payload'''

    now = datetime.now(dt.UTC)
    logger.info (f'setting {now = }')

    payload['iat'] = now.timestamp()
    payload['exp'] = (now + timedelta(**timedelta_params)).timestamp()

    logger.info(f'setting payload = {json.dumps(payload, indent=2)}')
    return payload

def add_uuid_to_payload(payload:dict) -> dict:
    payload['sub'] = str(uuid.uuid4())
    return payload

