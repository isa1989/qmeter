import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoAggregation:
    def __init__(self):
        self.db_name = os.getenv("DATABASE_NAME")
        self.collection_name = "feed_collection"
        self.mongo_host = os.getenv("DATABASE_HOST")
        self.mongo_port = os.getenv("DATABASE_PORT", 27017)
        self.client = MongoClient(
            f"mongodb://{self.mongo_host}:{self.mongo_port}/{self.db_name}"
        )
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def calculate_feedback_rate(self):
        pipeline = [
            {"$unwind": "$feedback_rate"},
            {
                "$group": {
                    "_id": {
                        "branch_name": "$branch.name",
                        "service_name": "$feedback_rate.service.name",
                    },
                    "rating_1": {
                        "$sum": {
                            "$cond": [{"$eq": ["$feedback_rate.rate_option", 1]}, 1, 0]
                        }
                    },
                    "rating_2": {
                        "$sum": {
                            "$cond": [{"$eq": ["$feedback_rate.rate_option", 2]}, 1, 0]
                        }
                    },
                    "rating_3": {
                        "$sum": {
                            "$cond": [{"$eq": ["$feedback_rate.rate_option", 3]}, 1, 0]
                        }
                    },
                    "rating_4": {
                        "$sum": {
                            "$cond": [{"$eq": ["$feedback_rate.rate_option", 4]}, 1, 0]
                        }
                    },
                    "rating_5": {
                        "$sum": {
                            "$cond": [{"$eq": ["$feedback_rate.rate_option", 5]}, 1, 0]
                        }
                    },
                }
            },
            {
                "$addFields": {
                    "total_count": {
                        "$add": [
                            "$rating_1",
                            "$rating_2",
                            "$rating_3",
                            "$rating_4",
                            "$rating_5",
                        ]
                    },
                    "weighted_sum": {
                        "$add": [
                            {"$multiply": ["$rating_1", 10]},
                            {"$multiply": ["$rating_2", 5]},
                            {"$multiply": ["$rating_4", -5]},
                            {"$multiply": ["$rating_5", -10]},
                        ]
                    },
                }
            },
            {
                "$addFields": {
                    "score": {
                        "$cond": {
                            "if": {"$gt": ["$total_count", 0]},
                            "then": {
                                "$multiply": [
                                    {
                                        "$divide": [
                                            {"$multiply": ["$weighted_sum", 100]},
                                            {"$multiply": ["$total_count", 10]},
                                        ]
                                    },
                                    1,
                                ]
                            },
                            "else": 0,
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$_id.branch_name",
                    "services": {
                        "$push": {
                            "service_name": "$_id.service_name",
                            "score": "$score",
                            "rating_1": "$rating_1",
                            "rating_2": "$rating_2",
                            "rating_3": "$rating_3",
                            "rating_4": "$rating_4",
                            "rating_5": "$rating_5",
                            "total": "$total_count",
                        }
                    },
                }
            },
            {"$project": {"_id": 0, "branch_name": "$_id", "services": 1}},
        ]

        return list(self.collection.aggregate(pipeline))
