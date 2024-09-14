import jwt
import logging
from cryptography.hazmat.primitives import serialization

from helpers import pem


logger = logging.getLogger(__name__)

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

