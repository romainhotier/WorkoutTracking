""" GetAllWorkshop Validator """
import pydantic
from typing import Optional

from flask import abort

import flaskr
from flaskr.enum import ErrorMsg
from flaskr.workshop import WorkshopCategories


class GetAllWorkshopValidator(pydantic.BaseModel):

    """ GetAllWorkshop Validator.
    - name: str = Workshop's Name.
    - description: str = Workshop's description.
    - categories = list[str] Workshop's category in ['cardio', 'fitness', 'strength'].
    """
    name: Optional[list[str]]
    description: Optional[list[str]]
    categories: Optional[list[str]]

    @pydantic.validator("name")
    @classmethod
    def name_validator(cls, values):
        """ Name must be a non empty String. """
        if "" in values:
            return abort(status=400, description=flaskr.Error(param="name", value=values,
                                                              msg=ErrorMsg.MustBeAStringNotEmpty.value))
        return values

    @pydantic.validator("description")
    @classmethod
    def description_validator(cls, values):
        """ Description must be a non empty String. """
        if "" in values:
            return abort(status=400, description=flaskr.Error(param="description", value=values,
                                                              msg=ErrorMsg.MustBeAStringNotEmpty.value))
        return values

    @pydantic.validator("categories")
    @classmethod
    def categories_validator(cls, values):
        """ Type must be a WorkshopCategories enum. """
        if not set(values).issubset(WorkshopCategories.list()):
            return abort(status=400, description=flaskr.Error(param="categories", value=values,
                                                              msg=ErrorMsg.MustBeInWorkshopCategories.value))
        return values
