""" DeleteWorkshopFiles API """
import pydantic
from typing import Optional

from tests import WorkshopTest, Msg, Error


class DeleteWorkshopFiles(object):
    url1 = "workshop"
    url2 = "files"
    param_id = "_id"
    param_filenames = "filenames"
    msg_success = f'workoutTracking.workshop.deleteWorkshopFiles.{Msg.Success.value}'
    msg_badRequest = f'workoutTracking.workshop.{Msg.BadRequest.value}'
    msg_notFound = f'workoutTracking.workshop.{Msg.NotFound.value}'


class DeleteWorkshopFilesRepBody(pydantic.BaseModel):

    status: int
    msg: str
    data: Optional[WorkshopTest]
    detail: Optional[object]

    @staticmethod
    def data_expected(workshop):
        return workshop.dict()

    @staticmethod
    def detail_expected_success(files: list):
        return {'files_deleted': [f'{file.parent}/{file.name}' for file in files]}

    @staticmethod
    def detail_expected_error(**error):
        return Error(**error)
