""" Server information """
import pydantic

from flaskr.database import mongo
from flaskr import Error
from flaskr.enum import Msg, ErrorMsg

from tests.test_workshop import WorkshopTest


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


Server = Server()
