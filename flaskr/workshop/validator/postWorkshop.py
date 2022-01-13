""" PostWorkshop Validator """
import pydantic
from typing import Optional

from flask import abort

import flaskr
from flaskr.enum import ErrorMsg
from flaskr.workshop import WorkshopCategories


class PostWorkshopValidator(pydantic.BaseModel):

    """ PostWorkshop Validator.
    - name: str = Workshop's Name.
    - description: str = Workshop's description.
    - categories = list[str] Workshop's category in ['cardio', 'fitness', 'strength'].
    """
    name: object
    description: Optional[object] = "Workshop's description"
    categories: Optional[object] = []

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
                                                      msg=ErrorMsg.MustBeInWorkShopCategory.value))
        return value

    @staticmethod
    def check_mandatory_fields(data):
        if "name" not in data:
            return abort(status=400,
                         description=flaskr.Error(param="name", msg=ErrorMsg.IsRequired.value))
