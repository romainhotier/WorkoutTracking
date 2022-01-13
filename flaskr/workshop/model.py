""" Workshop Model """
import pydantic
from typing import Optional

import re
from enum import Enum
from bson import ObjectId

from flaskr.database import mongo


class WorkshopCategories(Enum):
    """ Workshop's categories """
    Strength = "strength"
    Cardio = "cardio"
    Fitness = "fitness"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Workshop(pydantic.BaseModel):
    """ Workshop Information.

    - id: ObjectId = Workshop's ObjectId in MongoDb.
    - name: str = Workshop's Name.
    - description: str = Workshop's description.
    - categories = list[str] Workshop's category in ['cardio', 'fitness', 'strength'].
    - files = list[str] Workshop's media.
    """

    id: Optional[object] = pydantic.Field(alias='_id')
    name: Optional[str]
    description: Optional[str]
    categories: Optional[list[str]]
    files: Optional[list[str]] = []

    @pydantic.validator("id")
    @classmethod
    def id_validator(cls, value):
        """ Cast _id to id:str. """
        if isinstance(value, ObjectId):
            return str(value)
        else:
            return value

    def insert(self):
        """ Insert a Workshop and return it. """
        data = self.dict()
        data.pop("id")
        query = mongo.db.workshop.insert_one(data)
        self.id = str(query.inserted_id)
        return self

    @staticmethod
    def select_all():
        """ Return all Workshops. """
        workshops: list[Workshop] = []
        for item in mongo.db.workshop.find():
            workshops.append(Workshop(**item))
        return workshops

    @staticmethod
    def select_all_by(args):
        """ Return all Workshops. """
        search = {}
        workshops: list[Workshop] = []
        for key, values in args.items():
            if key in ["name", "description"]:
                search[key] = {"$in": [re.compile('.*{0}.*'.format(value), re.IGNORECASE) for value in values]}
            elif key == "categories":
                search["$expr"] = {"$setIsSubset": [values, "$categories"]}
                pass
        for item in mongo.db.workshop.find(search):
            workshops.append(Workshop(**item))
        return workshops

    def select_one_by_id(self):
        """ Return a Workshop. """
        item = mongo.db.workshop.find_one({"_id": ObjectId(self.id)})
        return Workshop(**item)

    def update(self, data: dict):
        """ Update a Workshop """
        mongo.db.workshop.update_one({"_id": ObjectId(self.id)}, {'$set': data})
        item = mongo.db.workshop.find_one({"_id": ObjectId(self.id)})
        return Workshop(**item)

    def add_files(self, files: list):
        """ Add files url to a Workshop """
        for file in files:
            mongo.db.workshop.update_one({"_id": ObjectId(self.id)}, {'$push': {"files": file}})
        item = mongo.db.workshop.find_one({"_id": ObjectId(self.id)})
        return Workshop(**item)

    def delete(self):
        """ Delete a Workshop and return it. """
        item = mongo.db.workshop.find_one({"_id": ObjectId(self.id)})
        mongo.db.workshop.delete_one({"_id": ObjectId(self.id)})
        return Workshop(**item)
