""" PostWorkshop API """
import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class PostWorkshop(object):
    url = "workshop"
    param_name = "name"
    param_description = "description"
    msg_success = f'workoutTracking.workshop.postWorkshop.{Msg.Success.value}'
    msg_badRequest = f'workoutTracking.workshop.{Msg.BadRequest.value}'


class PostWorkshopRepBody(pydantic.BaseModel):

    status: int
    msg: str
    data: Optional[WorkshopTest]
    detail: Optional[Error]

    def get_id(self):
        return self.data.id

    @staticmethod
    def data_expected(workshop):
        return workshop.dict()

    @staticmethod
    def detail_expected(**error):
        return Error(**error)
