import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pw}@localhost/travel_booking'.format(
    user=os.getenv('DB_USER'),
    pw=os.getenv('DB_PASSWORD'),
)

SQLALCHEMY_TRACK_MODIFICATIONS = False