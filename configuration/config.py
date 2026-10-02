from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME=os.getenv('DATABASE_NAME')
DATABASE_URL=os.getenv('DATABASE_URL')
DATABASE_USERNAME=os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')