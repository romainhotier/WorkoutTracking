""" UpdateWorkshop API """
import copy

import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class UpdateWorkshop(object):
    url = "workshop"
    param_id = "_id"
    param_name = "name"
    param_description = "description"
    param_categories = "categories"
    msg_success = f'workoutTracking.workshop.updateWorkshop.{Msg.Success.value}'
    msg_badRequest = f'workoutTracking.workshop.{Msg.BadRequest.value}'
    msg_notFound = f'workoutTracking.workshop.{Msg.NotFound.value}'

    @staticmethod
    def workshop_update_from_body(workshop: WorkshopTest, body):
        data = copy.deepcopy(body)
        data_filtered = WorkshopTest(**data).dict()
        if "id" in data_filtered:
            data_filtered.pop("id")
        if "files" in data_filtered:
            data_filtered.pop("files")
        return workshop.update(**data_filtered)


class UpdateWorkshopRepBody(pydantic.BaseModel):

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
