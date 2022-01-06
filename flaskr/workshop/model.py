""" Workshop Model """
import pydantic
from typing import Optional

from bson import ObjectId
from flask import abort

import flaskr
from flaskr.database import mongo
from flaskr.enum import ErrorMsg


class Workshop(pydantic.BaseModel):
    """ Workshop Information.

    - id: ObjectId = Workshop's ObjectId in MongoDb.
    - name: str = Workshop's Name. (Unique)
    - description: str = Workshop's description.
    - type = list[str] Workshop's type.
    - media = list[str] Workshop's media.
    """

    id: Optional[object] = pydantic.Field(alias='_id')
    name: Optional[object] = None
    description: Optional[object] = "Workshop's description"
    type: Optional[list[object]] = []
    media: Optional[list[object]] = []

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
        if value is None:
            return abort(status=400,
                         description=flaskr.Error(param="description", value=value, msg=ErrorMsg.IsRequired.value))
        if not isinstance(value, str):
            return abort(status=400,
                         description=flaskr.Error(param="description", value=value, msg=ErrorMsg.MustBeAString.value))
        if value.strip() == "":
            return abort(status=400,
                         description=flaskr.Error(param="description", value=value,
                                                  msg=ErrorMsg.MustBeAStringNotEmpty.value))
        return value

    @staticmethod
    def select_all():
        """ Return all Workshops. """
        workshops: list[Workshop] = []
        for item in mongo.db.workshop.find():
            workshops.append(Workshop(**item))
        return workshops

    @staticmethod
    def insert(data):
        """ Insert a Workshop and return it.

        - name is mandatory.
        """
        if "name" not in data.keys():
            return abort(status=400, description=flaskr.Error(param="name", msg=ErrorMsg.IsRequired.value))
        try:
            data.pop("_id")
        finally:
            workshop = Workshop(**data)
            query = mongo.db.workshop.insert_one(workshop.dict(exclude_none=True))
            workshop.id = str(query.inserted_id)
            return workshop

    def delete(self):
        """ Delete a Workshop and return it. """
        item = mongo.db.workshop.find_one({"_id": ObjectId(self.id)})
        if item is None:
            return abort(status=404,
                         description=flaskr.Error(param="_id", msg=ErrorMsg.DoesntExist.value, value=self.id))
        mongo.db.workshop.delete_one({"_id": ObjectId(self.id)})
        return Workshop(**item)
