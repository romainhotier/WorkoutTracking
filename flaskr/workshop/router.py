""" Workshop routes """
from flask import Blueprint, request, abort

import flaskr
from flaskr.enum import Msg, ErrorMsg
from flaskr.workshop import Workshop, WorkshopType

apis = Blueprint('workshop', __name__, url_prefix='/workshop')


@apis.route('/', methods=['GET'])
def get_all_workshop():
    """
    @api {get} /workshop  GetAllWorkshop
    @apiGroup Workshop
    @apiDescription Get Workshop ($AND between each parameter if sent)

    @apiParam (Query param) {String} [name] Workshop's name ($OR in search)
    @apiParam (Query param) {String} [description] Workshop's description ($OR in search)
    @apiParam (Query param) {String} [category] Workshop's category in ['cardio', 'fitness', 'strength']
                                                ($AND in search)

    @apiExample {json} Example usage:
    GET http://127.0.0.1:5000/ingredient

    @apiSuccessExample {json} Success response:
    HTTPS 200
    {
        "status": 200,
        "msg": "workoutTracking.workshop.deleteWorkshop.success",
        "data": [{"description": "Workshop's description", "id": "61dc2a02dc8493a5f471d2fe",
                  "media": [], "name": "qaRHR_name1", "category": []},
                  {"description": "Workshop's description", "id": "61dc2a02dc8493a5f471d2ff",
                  "media": [], "name": "qaRHR_name2", "category": []}]
    }
    """
    args = request.args.to_dict(flat=False)
    if not args:
        workshops: list[Workshop] = Workshop().select_all()
    else:
        if ("category" in args) and (not set(args["category"]).issubset(WorkshopType.list())):
            return abort(status=400, description=flaskr.Error(param="category",
                                                              msg=ErrorMsg.MustBeInWorkShopCategory.value,
                                                              value=args["category"]))
        workshops: list[Workshop] = Workshop().select_all_by(args)
    return flaskr.Response(status=200, msg=f'workoutTracking.{apis.name}.getAllWorkshop.{Msg.Success.value}',
                           data=workshops, detail=None).sent()


@apis.route('/<_id>', methods=['GET'])
def get_workshop(_id):
    """
    @api {get} /workshop/<_id>  GetWorkshop
    @apiGroup Workshop
    @apiDescription Get a workshop by it's ObjectId

    @apiParam (Query param) {String} _id Workshop's ObjectId

    @apiExample {json} Example usage:
    GET http://127.0.0.1:5000/workshop/<_id>

    @apiSuccessExample {json} Success response:
    HTTPS 200
    {
        "status": 200,
        "msg": "workoutTracking.workshop.deleteWorkshop.success",
        "data": {"description": "Workshop's description", "id": "61dc2a02dc8493a5f471d2fe",
                  "media": [], "name": "qaRHR_name1", "category": []}
    }

    @apiErrorExample {json} Error response:
    HTTPS 400
    {
        "status": 404,
        "msg": "workoutTracking.workshop.notFound",
        "detail": {"msg": "Doesn't exist", "param": "_id","value": "aaaaaaaaaaaaaaaaaaaaaaaa"}
    }
    """
    workshop: Workshop = Workshop(_id=_id).select_one_by_id()
    return flaskr.Response(status=200, msg=f'workoutTracking.{apis.name}.getWorkshop.{Msg.Success.value}',
                           data=workshop, detail=None).sent()


@apis.route('', methods=['POST'])
def post_workshop():
    """
    @api {post} /workshop  PostWorkshop
    @apiGroup Workshop
    @apiDescription Create a Workshop

    @apiParam (Body param) {String} name Workshop's name
    @apiParam (Body param) {String} [description="Workshop's description"] Workshop's description
    @apiParam (Body param) {Array} [category=Empty_Array] Workshop's category in ['cardio', 'fitness', 'strength']

    @apiExample {json} Example usage:
    POST http://127.0.0.1:5000/workshop
    {
        "name": <name>,
        "description": <description>,
        "type": ["cardio", "fitness"],
    }

    @apiSuccessExample {json} Success response:
    HTTPS 201
    {
        "status": 201,
        "msg": "workoutTracking.workshop.postWorkshop.success",
        "data": {"category": ["cardio"], "description": "qaRHR_description", "id": "61dc31e09aa1edbdfe1e5aa7",
                 "media": [], "name": "qaRHR_name"}
    }

    @apiErrorExample {json} Error response:
    HTTPS 400
    {
        "status": 400,
        "msg": "workoutTracking.workshop.badRequest",
        "detail": {"msg": "Must be a String not empty", "param": "name", "value": ""}
    }
    """
    data = request.json
    if "name" not in data:
        return abort(status=400, description=flaskr.Error(param="name", msg=ErrorMsg.IsRequired.value))
    if "_id" in data:
        data.pop("_id")
    if "media" in data:
        data.pop("media")
    workshop: Workshop = Workshop(**data).insert()
    return flaskr.Response(status=201, msg=f'workoutTracking.{apis.name}.postWorkshop.{Msg.Success.value}',
                           data=workshop, detail=None).sent()


@apis.route('/<_id>', methods=['DELETE'])
def delete_workshop(_id):
    """
    @api {delete} /workshop/<_id>  DeleteWorkshop
    @apiGroup Workshop
    @apiDescription Delete a Workshop by it's ObjectId

    @apiParam (Query param) {String} _id Workshop's ObjectId

    @apiExample {json} Example usage:
    DELETE http://127.0.0.1:5000/workshop/<_id>

    @apiSuccessExample {json} Success response:
    HTTPS 200
    {
        "status": 200,
        "msg": "workoutTracking.workshop.deleteWorkshop.success",
        "data": {"description": "Workshop's description", "id": "61dc2a02dc8493a5f471d2fe",
                  "media": [], "name": "qaRHR_name1", "category": []}
    }

    @apiErrorExample {json} Error response:
    HTTPS 400
    {
        "status": 404,
        "msg": "workoutTracking.workshop.notFound",
        "detail": {"msg": "Doesn't exist", "param": "_id","value": "aaaaaaaaaaaaaaaaaaaaaaaa"}
    }
    """
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
