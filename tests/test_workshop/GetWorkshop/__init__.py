""" GetWorkshop API """
import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class GetWorkshop(object):
    url = "workshop"
    param_id = "_id"
    msg_success = f'workoutTracking.workshop.getWorkshop.{Msg.Success.value}'
    msg_badRequest = f'workoutTracking.workshop.{Msg.BadRequest.value}'
    msg_notFound = f'workoutTracking.workshop.{Msg.NotFound.value}'
    msg_notAllowed = f'workoutTracking.{Msg.NotAllowed.value}'


class GetWorkshopRepBody(pydantic.BaseModel):

    status: int
    msg: str
    data: Optional[WorkshopTest]
    detail: Optional[object]

    @staticmethod
    def data_expected(workshop):
        return workshop.dict()

    @staticmethod
    def detail_expected(**error):
        return Error(**error)
