import pyperclip

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
    pyperclip.copy(token)

