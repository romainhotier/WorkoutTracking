""" GetAllWorkshop API """
import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class GetAllWorkshop(object):
    url = "workshop"
    param_name = "name"
    param_description = "description"
    param_categories = "categories"
    msg_success = f'workoutTracking.workshop.getAllWorkshop.{Msg.Success.value}'
    msg_badRequest = f'workoutTracking.workshop.{Msg.BadRequest.value}'


class GetAllWorkshopRepBody(pydantic.BaseModel):

    status: int
    msg: str
    data: Optional[list[WorkshopTest]]
    detail: Optional[Error]

    @staticmethod
    def data_expected(workshop):
        return workshop.dict()

    @staticmethod
    def detail_expected(**error):
        return Error(**error)
