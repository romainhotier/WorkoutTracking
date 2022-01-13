""" PostWorkshop API """
import copy

import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class PostWorkshop(object):
    url = "workshop"
    param_name = "name"
    param_description = "description"
    param_categories = "categories"
    msg_success = f'workoutTracking.workshop.postWorkshop.{Msg.Success.value}'
    msg_badRequest = f'workoutTracking.workshop.{Msg.BadRequest.value}'

    @staticmethod
    def workshop_set_from_body(body):
        data = copy.deepcopy(body)
        if "_id" in data:
            data.pop("_id")
        if "files" in data:
            data.pop("files")
        return WorkshopTest(**data)


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
