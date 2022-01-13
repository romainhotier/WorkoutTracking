""" Server information """
import os
import glob
import pydantic

from flaskr import app
from flaskr.database import mongo
from flaskr import Error
from flaskr.enum import Msg, ErrorMsg

from tests.test_workshop import WorkshopTest
from flaskr.workshop.model import WorkshopCategories


class Server(pydantic.BaseModel):
    """ Server to Test.

    - secure: str = Https or Http.
    - ip: str = Server's Ip.
    - port: str = Server's port.
    - main_url: str = Complete url for testing.
    """

    secure: str = "http"
    ip: str = "127.0.0.1"
    port: str = "5000"
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

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.storage_path = f'{Server.files_storage_path}{self.parent}/{self.name}'
        self.origin_path = f'{Server.files_origin_path}{self.name}'

    def dict(self):
        return self.__dict__

    def check_file_storage(self):
        assert os.path.exists(self.storage_path)


Server = Server()
