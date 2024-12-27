from dotenv import load_dotenv

load_dotenv()
from pymongo import MongoClient
import os


client = MongoClient(os.environ["MONGO_URI"])
mongo_database = client[os.environ["MONGODB_DATABASE"]]