""" Setup App """
import sys
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
from flaskr.enum import Msg
import flaskr.workshop.router as workshop_router

""" Define flask"""
app = Flask(__name__)

""" config """
app.config["ENV"] = "production"
app.config["JWT_SECRET_KEY"] = "super-secret-workoutTracking"
app.config["EXPIRATION_TOKEN"] = 5
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/workoutTracking"

""" CORS options"""
CORS(app)

""" Mongo """
mongo.init_app(app)

""" JWT for auth """
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

""" Logger """
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)
logger = logging.getLogger(__name__)

""" Register BleuPrint """
app.register_blueprint(workshop_router.apis)


@app.errorhandler(405)
def api_handler_405(err):
    """ Handle 405 errors. """
    return Response(status=405, msg=f'workoutTracking.{Msg.NotAllowed.value}', data=None, detail=err.description).sent()


def get_options_from_command_line(args):
    """ Catch command line options.

    Parameters
    ----------
    args: list
        All arguments in the command line.
        1st can be ["test", "dev", "prod"].

    Returns
    -------
    dict
        Set env / debug / testing to update server config.
    """
    try:
        mode = args[1]
        match mode:
            case "test":
                return {"env": "development", "debug": True, "testing": True}
            case "dev":
                return {"env": "development", "debug": True, "testing": False}
            case "prod":
                return {"env": "production", "debug": False, "testing": False}
            case _:
                return {"env": "production", "debug": False, "testing": False}
    except IndexError:
        return {"env": "production", "debug": False, "testing": False}


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
        pass
    except errors.ServerSelectionTimeoutError:
        logger.critical("Connexion to MongoDB Failed !!!")
        sys.exit()


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
        return {k: v for k, v in self.dict().items() if v}

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
