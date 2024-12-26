import os

import requests
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Command(BaseCommand):
    help = "Fetches data from S3 and loads it into MongoDB"

    def handle(self, *args, **kwargs):
        load_dotenv()

        # Get MongoDB connection details from .env file
        db_name = os.getenv("DATABASE_NAME")
        db_host = os.getenv("DATABASE_HOST")
        db_port = os.getenv("DATABASE_PORT")

        # Connect to MongoDB with database name in the connection string
        try:
            client = MongoClient(f"mongodb://{db_host}:{db_port}/{db_name}")
            db = client.get_database()
            collection = db["feed_collection"]
        except ConnectionFailure as e:
            self.stdout.write(self.style.ERROR(f"MongoDB connection failed: {e}"))
            return

        # Fetch data from the URL
        url = "https://qmeter-fb-dev.s3.amazonaws.com/media/feedback.json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch data: {e}"))
            return

        if response.status_code == 200:
            data = response.json()
            if data:
                try:
                    collection.insert_many(data)
                    self.stdout.write(self.style.SUCCESS("Data successfully loaded!"))
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to insert data into MongoDB: {e}")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING("No data found in the fetched JSON.")
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to fetch data, HTTP status: {response.status_code}"
                )
            )
