from dotenv import load_dotenv
import os
from os.path import join, dirname

def get_token(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)