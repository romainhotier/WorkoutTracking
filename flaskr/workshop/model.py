""" Workshop Model """
import pydantic
from typing import Optional

import re
from enum import Enum
from bson import ObjectId
from flask import abort

import flaskr
from flaskr.database import mongo
from flaskr.enum import ErrorMsg


class WorkshopType(Enum):
    """ Workshop's type """
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
    - category = list[str] Workshop's category in ['cardio', 'fitness', 'strength'].
    - media = list[str] Workshop's media.
    """

    id: Optional[object] = pydantic.Field(alias='_id')
    name: Optional[object] = None
    description: Optional[object] = "Workshop's description"
    category: Optional[object] = []
    media: Optional[object] = []

    @pydantic.validator("id")
    @classmethod
    def id_validator(cls, value):
        """ Cast _id to id:str. """
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, str):
            if len(value) == 24:
                return value
            else:
                return abort(status=400,
                             description=flaskr.Error(param="_id", value=value, msg=ErrorMsg.MustBeAnObjectId.value))

    @pydantic.validator("name")
    @classmethod
    def name_validator(cls, value):
        """ Name must be a non empty String. """
        if value is None:
            return abort(status=400,
                         description=flaskr.Error(param="name", value=value, msg=ErrorMsg.IsRequired.value))
        if not isinstance(value, str):
            return abort(status=400,
                         description=flaskr.Error(param="name", value=value, msg=ErrorMsg.MustBeAString.value))
        if value.strip() == "":
            return abort(status=400,
                         description=flaskr.Error(param="name", value=value, msg=ErrorMsg.MustBeAStringNotEmpty.value))
        return value

    @pydantic.validator("description")
    @classmethod
    def description_validator(cls, value):
        """ Description must be a non empty String. """
        if not isinstance(value, str):
            return abort(status=400,
                         description=flaskr.Error(param="description", value=value, msg=ErrorMsg.MustBeAString.value))
        if value.strip() == "":
            return abort(status=400,
                         description=flaskr.Error(param="description", value=value,
                                                  msg=ErrorMsg.MustBeAStringNotEmpty.value))
        return value

    @pydantic.validator("category")
    @classmethod
    def category_validator(cls, value):
        """ Type must be a WorkshopType enum. """
        if not isinstance(value, list):
            return abort(status=400,
                         description=flaskr.Error(param="category", value=value, msg=ErrorMsg.MustBeAList.value))
        for key in value:
            if key not in WorkshopType.list():
                return abort(status=400,
                             description=flaskr.Error(param="category", value=value,
                                                      msg=ErrorMsg.MustBeInWorkShopCategory.value))
        return value

    @pydantic.validator("media")
    @classmethod
    def media_validator(cls, value):
        """ Media can't be edited through the model. """
        if not isinstance(value, list):
            return []
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
            elif key == "category":
                search["$expr"] = {"$setIsSubset": [values, "$category"]}
                pass
        for item in mongo.db.workshop.find(search):
            workshops.append(Workshop(**item))
        return workshops

    def select_one_by_id(self):
        """ Return a Workshop. """
        item = mongo.db.workshop.find_one({"_id": ObjectId(self.id)})
        if item is None:
            return abort(status=404,
                         description=flaskr.Error(param="_id", msg=ErrorMsg.DoesntExist.value, value=self.id))
        return Workshop(**item)

    def delete(self):
        """ Delete a Workshop and return it. """
        item = mongo.db.workshop.find_one({"_id": ObjectId(self.id)})
        if item is None:
            return abort(status=404,
                         description=flaskr.Error(param="_id", msg=ErrorMsg.DoesntExist.value, value=self.id))
        mongo.db.workshop.delete_one({"_id": ObjectId(self.id)})
        return Workshop(**item)
