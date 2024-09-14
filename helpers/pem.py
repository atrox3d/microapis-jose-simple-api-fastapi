import subprocess
import os
import shlex
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def run(command:str, path:str = None) -> subprocess.CompletedProcess:
    if path is not None:
        logger.debug(f'changing dir to {path}')
        os.chdir(Path(path).resolve())
    # shlex.split breaks on windows paths
    # use Path(path).as_posix()
    # https://stackoverflow.com/a/63534016
    args = shlex.split(command)
    try:
        logger.debug(f'running {args}')
        completed = subprocess.run(args, check=True, shell=False, capture_output=True, text=True)
        return completed
    except subprocess.CalledProcessError as cpe:
        logger.exception(cpe)
        logger.exception(cpe.stderr)
        logger.exception(cpe.stdout)
        raise

def create_pem_keys(cn:str, private_filename='private_key.pem', public_filename='public_key.pem'):
    # openssl req -x509 -nodes -newkey rsa:2048 -keyout private_key.pem -out public_key.pem -subj "/CN=jwt-tutorial"
    cmd = f'openssl req -x509 -nodes -newkey rsa:2048 -keyout {private_filename} -out {public_filename} -subj "/CN={cn}"'
    logger.info(f'creating {private_filename}, {public_filename} with {cn=}')
    run(cmd)

def load_pem_key(pem_path:str) -> str:
    logger.info(f'loading key from {pem_path}')
    text = Path(pem_path).read_text()
    logger.debug(f'{pem_path}::{text = }')
    return text

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    private_pem = 'private_key.pem'
    public_pem = 'public_key.pem'
    create_pem_keys(cn='jwt-tutorial')
    load_pem_key(private_pem)
    load_pem_key(public_pem)
