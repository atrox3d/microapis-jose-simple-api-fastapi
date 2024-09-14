from pathlib import Path
import jwt
import logging
from cryptography.x509 import load_pem_x509_certificate


logger = logging.getLogger(__name__)

def decode_and_validate_token(access_token:str, public_pem:str, audience:str):
    unverified_headers = jwt.get_unverified_header(access_token)
    logger.debug(f'{unverified_headers = }')

    public_key = Path(public_pem).read_text()
    logger.debug(f'{public_key = }')

    x509_certificate = load_pem_x509_certificate(
        public_key.encode()
    ).public_key()
    logger.debug(f'{x509_certificate = }')

    decoded =  jwt.decode(
        access_token,
        x509_certificate,
        algorithms=unverified_headers['alg'],
        audience=audience
    )
    print(f'{decoded = }')
    return decoded



