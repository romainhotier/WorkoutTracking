""" Setup App """
import sys
import platform
import os
import logging
import pydantic
from typing import Optional

from flask import Flask, make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_pymongo import PyMongo

from pymongo import errors

from flaskr.database import mongo
from flaskr.enum import RunMode, Msg
import flaskr.workshop.router as workshop_router


class Response(pydantic.BaseModel):
    """ Server's Response

    - http_code: int = HttpCode.
    - msg: str = Global information for the user.
    - data: object = Data to be sent.
    - detail: object = Detail to be sent.
    """

    status: int
    msg: str
    data: object
    detail: object

    def format(self):
        """ Remove None data/detail. """
        return {k: v for k, v in self.dict().items() if v is not None}

    def sent(self):
        """ Return a Flask's Response """
        response = make_response(self.format(), self.status)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


class Error(pydantic.BaseModel):
    """ Error's Information

    - param: str = Parameter's name in api doc.
    - msg: str = Global information for the user.
    - value: object = Value get by the server.
    """

    param: str
    msg: str
    value: Optional[object]


# Cmd Line
def get_options_from_command_line(args):
    """ Catch command line options. Prod by Default

    Parameters
    ----------
    args: list
        All arguments in the command line.
        1st can be ["dev", "prod"].

    Returns
    -------
    dict
        Set env / debug / testing to update server config.
    """
    try:
        run_mode = args[1]
        match run_mode:
            case RunMode.Dev.value:
                return {"run_mode": run_mode, "env": "development", "debug": True, "testing": True}
            case RunMode.Prod.value:
                return {"run_mode": run_mode, "env": "production", "debug": False, "testing": False}
            case _:
                return {"run_mode": RunMode.Prod.value, "env": "production", "debug": False, "testing": False}
    except IndexError:
        return {"run_mode": RunMode.Prod.value, "env": "production", "debug": False, "testing": False}


# Check MongoDB is Up
def check_mongodb_up():
    """ Check if MongoDB is UP.

    Returns
    -------
    Any
        Close app if there is no connection.
    """
    try:
        mongo_client = PyMongo(app, serverSelectionTimeoutMS=2000).cx
        mongo_client.server_info()
        mongo_client.close()
        logger.info(" * MongoDB Up")
        pass
    except errors.ServerSelectionTimeoutError:
        logger.critical("Connexion to MongoDB Failed !!!")
        sys.exit()


# Files management
def get_storage_path():
    """ Set both FILES_STORAGE_PATH and FILES_TESTS_ORIGIN_PATH from platform used

    Returns
    -------
    tuple
        FILES_STORAGE_PATH, FILES_TESTS_ORIGIN_PATH.
    """
    system = platform.system()
    usr = os.getlogin()
    if usr == "rhr" and system == "Linux":  # Desktop pc for dev
        logger.critical("Welcome LinuxRHR, but need to set the env before !!!")
        sys.exit()
        #return "/home/rhr/Workspace/Python/Cookbook/Flask/_files/"
    elif usr == "ubuntu" and system == "Linux":  # Raspberry prod
        logger.critical("Welcome PI4, but need to set the env before !!!")
        sys.exit()
        #return "/home/ubuntu/Workspace/Storage/cookbook/"
    elif usr in ["romain.hotier", "root"] and system == "Darwin":  # Macbook Mirakl
        logger.info(" * System detected => Mac Mirakl")
        return ("/Users/romain.hotier/workspace/rhr/WorkoutTracking/files/",
                "/Users/romain.hotier/workspace/rhr/WorkoutTracking/tests/files/")
    else:
        logger.critical("Storage path can't be set !!! (unknown system)")
        sys.exit()


def create_root_storage_folders():
    """ Create root folders from app.FILES_STORAGE_PATH configuration. """
    try:
        os.mkdir(f'{app.config["FILES_STORAGE_PATH"]}')
    except (FileExistsError, OSError):
        pass
    collections = ["workshop"]
    for collection in collections:
        try:
            os.mkdir(f'{app.config["FILES_STORAGE_PATH"]}/{collection}')
        except (FileExistsError, OSError):
            pass


def create_storage_folder(parent: str):
    """ Catch command line options.

    Parameters
    ----------
    parent: collection/_id's item.
    """
    try:
        os.mkdir(f'{app.config["FILES_STORAGE_PATH"]}/{parent}')
    except (FileExistsError, OSError):
        pass


def check_file_exist(path: str):
    """ Check if file exist

    Returns
    -------
    bool
        If path exist.
    """
    return os.path.exists(path)


def delete_file(filepath: str):
    """ Delete file """
    try:
        os.remove(filepath)
    except OSError:
        pass


""" Logger """
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)
logger = logging.getLogger(__name__)

""" Define flask"""
app = Flask(__name__)

""" config """
app.config["ENV"] = "production"
app.config["JWT_SECRET_KEY"] = "super-secret-workoutTracking"
app.config["EXPIRATION_TOKEN"] = 5
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/workoutTracking"
app.config["RUN_MODE"] = ""
paths = get_storage_path()
app.config["FILES_STORAGE_PATH"] = paths[0]
app.config["FILES_TESTS_ORIGIN_PATH"] = paths[1]

""" CORS options"""
CORS(app)

""" Mongo """
check_mongodb_up()
mongo.init_app(app)

""" JWT for auth """
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

""" Register BleuPrint """
app.register_blueprint(workshop_router.apis)

""" Create Storage Folder and/or clean """
create_root_storage_folders()


@app.errorhandler(405)
def api_handler_405(err):
    """ Handle 405 errors. """
    return Response(status=405, msg=f'workoutTracking.{Msg.NotAllowed.value}', data=None, detail=err.description).sent()
