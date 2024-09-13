import jwt
import logging
from pathlib import Path
from cryptography.hazmat.primitives import serialization

import pem

logger = logging.getLogger(__name__)

def create_pems(private_pem:str, public_pem:str):
    ''' creates pem files deleting any existing ones'''

    for pemfile in private_pem, public_pem:
        pemfile = Path(pemfile)
        if pemfile.exists():
            logger.info(f'deleting existing {pemfile}')
            pemfile.unlink()

    pem.create_pem_keys(cn='jwt-tutorial')

def generate_jwt(payload:dict, private_pem:str):
    ''' creates jwt token from payload and private pem file'''

    logger.info('getting private pem text')
    private_key_text = pem.load_pem_key(private_pem)

    logger.info('getting private key')
    private_key = serialization.load_pem_private_key(
        private_key_text.encode(),
        password=None
    )

    logger.info('generating jwt token')
    return jwt.encode(payload, private_key, 'RS256')

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    
    # private_pem = 'private_key.pem'
    # public_pem = 'public_key.pem'
    
    # create_pems(private_pem, public_pem)
    
    # payload = payload_manager.load_payload_from_json('payload.json')
    # payload = payload_manager.add_time_to_payload(payload, hours=24)
    
    # token = generate_jwt(payload, private_pem)
    # print(f'{token = }')
    pass