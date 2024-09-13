# print('SERVER | ------- START ----------')
from fastapi import FastAPI

server = FastAPI(debug=True)

# print('SERVER | ------- import api -----')
import api

# print('SERVER | ------- END ----------')
