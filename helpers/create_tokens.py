import logging
from pathlib import Path
import sys

try:
    from helpers import pem
    from helpers import payload_manager
    from helpers import tokenmanager
    from helpers import jwt_generator
except ModuleNotFoundError:
    from pathlib import Path
    module = Path(__file__)
    print(f'SYNTAX | python -m {module.parent.name}.{module.stem}')
    exit()

#################################################
# python -m helpers.create_tokens
#################################################

logger = logging.getLogger(__name__)

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
pem.create_pems(private_pem, public_pem, delete=False)
#
payload_json = Path(__file__).parent / 'payload.json'
payload = payload_manager.load_payload_from_json(payload_json)
payload = payload_manager.add_time_to_payload(payload, hours=24)
payload = payload_manager.add_uuid_to_payload(payload, id=userid)
#
token = jwt_generator.generate_jwt(payload, private_pem)
print(f'token = \n{token}')

token_path = Path(__file__).parent / f'{username}.txt'
tokenmanager.save_token(token, token_path)    
logger.warning('saved token to txt')

tokenmanager.copy_token_to_clipboard(token)
logger.warning('copied toke to clipboard')

json_path = Path(__file__).parent / f'{username}.json'
tokenmanager.save_user_token_to_json(json_path, userid, token)
logger.warning('saved userid and token to json')
