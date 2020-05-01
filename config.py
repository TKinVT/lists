import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('CSRF_SECRET_KEY')
    API_TOKEN = os.getenv('API_TOKEN')
    MONGOATLAS_USERNAME = os.getenv("MONGOATLAS_USERNAME")
    MONGOATLAS_PASSWORD = os.getenv("MONGOATLAS_PASSWORD")
    MONGOATLAS_URL = os.getenv("MONGOATLAS_URL")
