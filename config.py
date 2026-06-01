import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.environ["MONGO_URI"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    print(f"MONGO_URI carregada: {MONGO_URI}")