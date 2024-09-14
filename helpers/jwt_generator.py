import jwt
import logging
from pathlib import Path
from cryptography.hazmat.primitives import serialization

try:
    from helpers import pem
    from helpers import payload_manager
    from helpers import tokenmanager
except ModuleNotFoundError:
    from pathlib import Path
    module = Path(__file__)
    print(f'SYNTAX | python -m {module.parent.name}.{module.stem}')
    exit()


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

