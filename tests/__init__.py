""" Server information """
import os
import shutil
import glob
import pydantic

import flaskr
from flaskr import app
from flaskr.database import mongo  # use for test model
from flaskr import Error  # usr for api model
from flaskr.enum import Msg, ErrorMsg  # use for api model

from tests.test_workshop import WorkshopTest
from flaskr.workshop.model import WorkshopCategories


class Server(pydantic.BaseModel):
    """ Server to Test.

    - secure: str = Https or Http.
    - ip: str = Server's Ip.
    - port: str = Server's port.
    - main_url: str = Complete url for testing.
    - files_storage_path: str = Complete url for testing.
    - files_origin_path: str = Complete url for testing.
    """

    secure: str = "http"
    ip: str = "127.0.0.1"
    port: str = "5001"
    main_url: str = f'{secure}://{ip}:{port}'
    files_storage_path: str = app.config["FILES_STORAGE_PATH"]
    files_origin_path: str = app.config["FILES_TESTS_ORIGIN_PATH"]

    @staticmethod
    def clean_tests_files():
        for f in glob.glob(f'{app.config["FILES_STORAGE_PATH"]}**/qaRHR*', recursive=True):
            os.remove(f)
        for dirpath, dirnames, filenames in os.walk(app.config["FILES_STORAGE_PATH"]):
            try:
                os.rmdir(dirpath)
            except OSError:
                pass


class File(object):

    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.storage_path = f'{Server.files_storage_path}{self.parent}/{self.name}'
        self.origin_path = f'{Server.files_origin_path}{self.name}'

    def dict(self):
        return self.__dict__

    def check_file_storage(self, exist: bool):
        assert os.path.exists(self.storage_path) is exist

    def create(self):
        flaskr.create_storage_folder(parent=self.parent)
        try:
            shutil.copyfile(self.origin_path, self.storage_path)
            return self
        except (FileExistsError, OSError):
            pass


Server = Server()
flaskr.create_root_storage_folders()
