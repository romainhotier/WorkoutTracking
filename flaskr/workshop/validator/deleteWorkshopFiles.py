""" DeleteWorkshopFiles Validator """
import pydantic
from typing import Optional
from bson import ObjectId

from flask import abort

import flaskr
from flaskr.database import mongo
from flaskr.enum import ErrorMsg


class DeleteWorkshopFilesValidator(pydantic.BaseModel):

    """ DeleteWorkshopFiles Validator.
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
