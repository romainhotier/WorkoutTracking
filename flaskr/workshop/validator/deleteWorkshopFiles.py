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
    - filenames: list = Workshop's filename to be deleted.

    """
    id: Optional[object] = pydantic.Field(alias='_id')
    filenames: Optional[list[str]]

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

    @pydantic.validator("filenames")
    @classmethod
    def filenames_validator(cls, value):
        """ Check filenames is an array of string not empty """
        if not isinstance(value, list):
            return abort(status=400,
                         description=flaskr.Error(param="filenames", value=value, msg=ErrorMsg.MustBeAList.value))
        if not value:
            return abort(status=400,
                         description=flaskr.Error(param="filenames", value=value,
                                                  msg=ErrorMsg.MustBeAListOfStringNotEmpty.value))
        for key in value:
            if key.strip() == "":
                return abort(status=400,
                             description=flaskr.Error(param="filenames", value=value,
                                                      msg=ErrorMsg.MustBeAListOfStringNotEmpty.value))
        return value

    def check_files_exist(self):
        for filename in self.filenames:
            if not flaskr.check_file_exist(f'{flaskr.app.config["FILES_STORAGE_PATH"]}workshop/{self.id}/{filename}'):
                return abort(status=400, description=flaskr.Error(param="filenames", value=filename,
                                                                  msg=ErrorMsg.DoesntExist.value))
