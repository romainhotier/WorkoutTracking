""" Workshop routes """
from flask import Blueprint, request

import flaskr
from flaskr.enum import Msg
from flaskr.workshop import Workshop

apis = Blueprint('workshop', __name__, url_prefix='/workshop')


@apis.route('/', methods=['GET'])
def get_all_workshop():
    """ Get all Workshops in the Database. """
    workshops: list[Workshop] = Workshop().select_all()
    return flaskr.Response(status=200, msg=f'workoutTracking.{apis.name}.getAllWorkshop.{Msg.Success.value}',
                           data=workshops, detail=None).sent()


@apis.route('', methods=['POST'])
def post_workshop():
    """ Insert a Workshop in the Database. """
    workshop: Workshop = Workshop().insert(request.json)
    return flaskr.Response(status=200, msg=f'workoutTracking.{apis.name}.postWorkshop.{Msg.Success.value}',
                           data=workshop, detail=None).sent()


@apis.route('/<_id>', methods=['DELETE'])
def delete_workshop(_id):
    """ Delete a Workshop from the Database. """
    workshop: Workshop = Workshop(_id=_id).delete()
    return flaskr.Response(status=200, msg=f'workoutTracking.{apis.name}.deleteWorkshop.{Msg.Success.value}',
                           data=workshop, detail=None).sent()


@apis.errorhandler(400)
def api_handler_400(err):
    """ Handle 400 errors. """
    return flaskr.Response(status=400, msg=f'workoutTracking.{apis.name}.{Msg.BadRequest.value}',
                           data=None, detail=err.description).sent()


@apis.errorhandler(404)
def api_handler_404(err):
    """ Handle 404 errors. """
    return flaskr.Response(status=404, msg=f'workoutTracking.{apis.name}.{Msg.NotFound.value}',
                           data=None, detail=err.description).sent()
