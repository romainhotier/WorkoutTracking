""" PostWorkshopFiles API """
import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class PostWorkshopFiles(object):
    url1 = "workshop"
    url2 = "files"
    msg_success = f'workoutTracking.workshop.postWorkshopFiles.{Msg.Success.value}'
    msg_badRequest = f'workoutTracking.workshop.{Msg.BadRequest.value}'


class PostWorkshopFilesRepBody(pydantic.BaseModel):

    status: int
    msg: str
    data: Optional[WorkshopTest]
    detail: Optional[object]

    @staticmethod
    def data_expected(workshop):
        return workshop.dict()

    @staticmethod
    def detail_expected_success(_id: str, files: list):
        return {'files_added': [f'workshop/{_id}/{file.name}' for file in files]}

    @staticmethod
    def detail_expected_error(**error):
        return Error(**error)
