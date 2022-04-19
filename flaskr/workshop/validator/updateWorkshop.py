""" UpdateWorkshop Validator """
import pydantic
from typing import Optional
from bson import ObjectId

from flask import abort

import flaskr
from flaskr.database import mongo
from flaskr.enum import ErrorMsg
from flaskr.workshop import WorkshopCategories


class UpdateWorkshopValidator(pydantic.BaseModel):

    """ UpdateWorkshop Validator.
    - _id: str = Workshop's ObjectId.
    """
    id: Optional[object] = pydantic.Field(alias='_id')

    @pydantic.validator("id")
    @classmethod
    def id_validator(cls, value):
        """ Check Id is correct and exist """
        if isinstance(value, str):
            if len(value) == 24:
                item = mongo.db.workshop.find_one({"_id": ObjectId(value)})
                if item is None:
                    return abort(status=404,
                                 description=flaskr.Error(param="_id", msg=ErrorMsg.DoesntExist.value, value=value))
                return value
            else:
                return abort(status=400,
                             description=flaskr.Error(param="_id", value=value, msg=ErrorMsg.MustBeAnObjectId.value))
        else:
            return abort(status=400,
                         description=flaskr.Error(param="_id", value=value, msg=ErrorMsg.MustBeAnObjectId.value))


class UpdateWorkshopBodyValidator(pydantic.BaseModel):

    """ UpdateWorkshop Validator.
    - name: str = Workshop's Name.
    - description: str = Workshop's description.
    - categories = list[str] Workshop's category in ['cardio', 'fitness', 'strength'].
    """
    name: Optional[object]
    description: Optional[object]
    categories: Optional[object]

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

    @pydantic.validator("categories")
    @classmethod
    def categories_validator(cls, value):
        """ Type must be a WorkshopCategories enum. """
        if not isinstance(value, list):
            return abort(status=400,
                         description=flaskr.Error(param="categories", value=value, msg=ErrorMsg.MustBeAList.value))
        for key in value:
            if key not in WorkshopCategories.list():
                return abort(status=400,
                             description=flaskr.Error(param="categories", value=value,
                                                      msg=ErrorMsg.MustBeInWorkshopCategories.value))
        return value
