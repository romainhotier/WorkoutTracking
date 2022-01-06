""" GetAllWorkshop API """
import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class GetAllWorkshop(object):
    url = "workshop"
    msg_success = f'workoutTracking.workshop.getAllWorkshop.{Msg.Success.value}'


class GetAllWorkshopRepBody(pydantic.BaseModel):

    status: int
    msg: str
    data: Optional[list[WorkshopTest]]
    detail: Optional[Error]

    @staticmethod
    def data_expected(workshop):
        return workshop.dict()
