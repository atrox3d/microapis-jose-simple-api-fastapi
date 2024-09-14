import jwt
import logging
from pathlib import Path
from cryptography.hazmat.primitives import serialization

try:
    from helpers import pem
    from helpers import payload_manager
except ModuleNotFoundError:
    from pathlib import Path
    module = Path(__file__)
    print(f'SYNTAX | python -m {module.parent.name}.{module.stem}')
    exit()


logger = logging.getLogger(__name__)

def create_pems(private_pem:str, public_pem:str, *, delete:bool, force_overwrite:bool=False):
    ''' creates pem files deleting any existing ones'''

    for pemfile in private_pem, public_pem:
        pemfile = Path(pemfile)
        if pemfile.exists():
            if delete:
                logger.info(f'deleting existing {pemfile}')
                pemfile.unlink()
            if not force_overwrite:
                # raise FileExistsError(str(pemfile))
                logger.warning(f'{pemfile} exists, use force_overwrite to substitute')
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

def save_token(token:str, filepath:str):
    with open(filepath, 'w') as fp:
        fp.write(token)

def load_token(token:str, filepath:str):
    with open(filepath) as fp:
        return fp.read(token)

def save_user_token_to_json(json_path:str, userid:str, token:str):
    import json
    data = {
        'userid': userid,
        'token': token
    }
    with open(json_path, 'w') as jp:
        json.dump(data, jp)    

def copy_token_to_clipboard(token:str):
    import pyperclip
    pyperclip.copy(token)

if __name__ == '__main__':
    #################################################
    # python -m helpers.jwt_generator
    #################################################
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s | %(funcName)s | %(message)s'
    )

    try:
        username, userid = sys.argv[1:]
        logger.info(f'got {userid = } {username = }')
    except ValueError:
        logging.critical('syntax python -m helpers.jwt_generator username userid')
        exit()

    # 
    private_pem = 'private_key.pem'
    public_pem = 'public_key.pem'
    # 
    # try:
    create_pems(private_pem, public_pem, delete=False)
    # except FileExistsError as fee:
        # logger.critical(f'{fee} exists: please delete or force overwrite')
        # exit()
    #
    payload_json = Path(__file__).parent / 'payload.json'
    payload = payload_manager.load_payload_from_json(payload_json)
    payload = payload_manager.add_time_to_payload(payload, hours=24)
    payload = payload_manager.add_uuid_to_payload(payload, id=userid)
    #
    token = generate_jwt(payload, private_pem)
    print(f'token = \n{token}')
    
    token_path = Path(__file__).parent / f'{username}.txt'
    save_token(token, token_path)    
    logger.warning('saved token to txt')

    copy_token_to_clipboard(token)
    logger.warning('copied toke to clipboard')

    json_path = Path(__file__).parent / f'{username}.json'
    save_user_token_to_json(json_path, userid, token)
    logger.warning('saved userid and token to json')
