""" Workshop routes """
from flask import Blueprint, request

import flaskr
from flaskr.enum import Msg
from flaskr.workshop import Workshop, DeleteWorkshopValidator, DeleteWorkshopFilesValidator, \
    GetAllWorkshopValidator, GetWorkshopValidator, PostWorkshopValidator, PostWorkshopFilesValidator

apis = Blueprint('workshop', __name__, url_prefix='/workshop')


@apis.route('/', methods=['GET'])
def get_all_workshop():
    """
    @api {get} /workshop  GetAllWorkshop
    @apiGroup Workshop
    @apiDescription Get Workshop ($AND between each parameter if sent)

    @apiParam (Query param) {String} [name] Workshop's name ($OR in search)
    @apiParam (Query param) {String} [description] Workshop's description ($OR in search)
    @apiParam (Query param) {String} [categories] Workshop's categories in ['cardio', 'fitness', 'strength']
                                                  ($AND in search)

    @apiExample {json} Example usage:
    GET http://127.0.0.1:5000/ingredient

    @apiSuccessExample {json} Success response:
    HTTPS 200
    {
        "status": 200,
        "msg": "workoutTracking.workshop.deleteWorkshop.success",
        "data": [{"description": "Workshop's description", "id": "61dc2a02dc8493a5f471d2fe",
                  "files": [], "name": "qaRHR_name1", "categories": []},
                  {"description": "Workshop's description", "id": "61dc2a02dc8493a5f471d2ff",
                  "files": [], "name": "qaRHR_name2", "categories": []}]
    }
    """
    args = request.args.to_dict(flat=False)
    if not args:
        workshops: list[Workshop] = Workshop().select_all()
    else:
        args_validated = GetAllWorkshopValidator(**args).dict(exclude_none=True)
        workshops: list[Workshop] = Workshop().select_all_by(args_validated)
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
                 "files": [], "name": "qaRHR_name1", "categories": []}
    }

    @apiErrorExample {json} Error response:
    HTTPS 400
    {
        "status": 404,
        "msg": "workoutTracking.workshop.notFound",
        "detail": {"msg": "Doesn't exist", "param": "_id","value": "aaaaaaaaaaaaaaaaaaaaaaaa"}
    }
    """
    GetWorkshopValidator(_id=_id)
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
    @apiParam (Body param) {Array} [categories=Empty_Array] Workshop's categories in ['cardio', 'fitness', 'strength']

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
        "data": {"categories": ["cardio"], "description": "qaRHR_description", "id": "61dc31e09aa1edbdfe1e5aa7",
                 "files": [], "name": "qaRHR_name"}
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
    PostWorkshopValidator().check_mandatory_fields(data)
    data_validated = PostWorkshopValidator(**data).dict()
    workshop: Workshop = Workshop(**data_validated).insert()
    return flaskr.Response(status=201, msg=f'workoutTracking.{apis.name}.postWorkshop.{Msg.Success.value}',
                           data=workshop, detail=None).sent()


@apis.route('/<_id>/files', methods=['POST'])
def post_workshop_files(_id):
    """
    @api {post} /workshop/<_id>/files  PostWorkshopFiles
    @apiGroup Workshop
    @apiDescription Add files to a workshop

    @apiParam (Query param) {String} _id Workshop's ObjectId
    @apiParam (Multipart/form-data) files Files

    @apiExample {json} Example usage:
    POST http://127.0.0.1:5000/workshop/<_id>/files
    files = [('files', open('pathToFile1', 'rb')),
             ('files', open('pathToFile2', 'rb'))]

    @apiSuccessExample {json} Success response:
    HTTPS 201
    {
        "status": 201,
        "msg": "workoutTracking.workshop.postWorkshopFiles.success",
        "data": {"categories": ["cardio"], "description": "qaRHR_description", "id": "61dc31e09aa1edbdfe1e5aa7",
                 "files": ["<files1Path>", "<files2Path>"], "name": "qaRHR_name"},
        "detail":{"files_added":["<files1AddedPath>","<files2AddedPath>"]
    }

    @apiErrorExample {json} Error response:
    HTTPS 400
    {
        "status": 404,
        "msg": "workoutTracking.workshop.notFound",
        "detail": {"msg": "Doesn't exist", "param": "_id","value": "aaaaaaaaaaaaaaaaaaaaaaaa"}
    }
    """
    PostWorkshopFilesValidator(_id=_id)
    flaskr.create_storage_folder(collection="workshop", _id=_id)
    files_url = []
    for file in request.files.getlist('files'):
        file.save(f'{flaskr.app.config["FILES_STORAGE_PATH"]}workshop/{_id}/{file.filename}')
        files_url.append(f'workshop/{_id}/{file.filename}')
    workshop: Workshop = Workshop(_id=_id).add_files(files_url)
    return flaskr.Response(status=201, msg=f'workoutTracking.{apis.name}.postWorkshopFiles.{Msg.Success.value}',
                           data=workshop, detail={"files_added": files_url}).sent()


@apis.route('/<_id>/files', methods=['DELETE'])
def delete_workshop_files(_id):
    """
    @api {delete} /workshop/<_id>/files?filename[x]=<filename>  DeleteWorkshopFiles
    @apiGroup Workshop
    @apiDescription Delete files to a workshop

    @apiParam (Query param) {String} _id Workshop's ObjectId
    @apiParam (Query param) {Array} filename File's name to be deleted.

    @apiExample {json} Example usage:
    DELETE http://127.0.0.1:5000/workshop/<_id>/files?filename[0]=<filename>

    @apiSuccessExample {json} Success response:
    HTTPS 200
    {
        "status": 200,
        "msg": "workoutTracking.workshop.deleteWorkshopFiles.success",
        "data": {"categories": ["cardio"], "description": "qaRHR_description", "id": "61dc31e09aa1edbdfe1e5aa7",
                 "files": ["<files1Path>", "<files2Path>"], "name": "qaRHR_name"},
        "detail":{"files_deleted":["<files1AddedPath>","<files2AddedPath>"]
    }

    @apiErrorExample {json} Error response:
    HTTPS 400
    {
        "status": 404,
        "msg": "workoutTracking.workshop.notFound",
        "detail": {"msg": "Doesn't exist", "param": "_id","value": "aaaaaaaaaaaaaaaaaaaaaaaa"}
    }
    """
    DeleteWorkshopFilesValidator(_id=_id)
    #with_calories = request.args.get(api.param_with_calories)

    #flaskr.create_storage_folder(collection="workshop", _id=_id)
    #files_url = []
    #for file in request.files.getlist('files'):
    #    file.save(f'{flaskr.app.config["FILES_STORAGE_PATH"]}workshop/{_id}/{file.filename}')
    #    files_url.append(f'workshop/{_id}/{file.filename}')
    #workshop: Workshop = Workshop(_id=_id).add_files(files_url)
    #return flaskr.Response(status=201, msg=f'workoutTracking.{apis.name}.postWorkshopFiles.{Msg.Success.value}', data=workshop, detail={"files_added": files_url}).sent()


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
                 "files": [], "name": "qaRHR_name1", "categories": []}
    }

    @apiErrorExample {json} Error response:
    HTTPS 400
    {
        "status": 404,
        "msg": "workoutTracking.workshop.notFound",
        "detail": {"msg": "Doesn't exist", "param": "_id","value": "aaaaaaaaaaaaaaaaaaaaaaaa"}
    }
    """
    DeleteWorkshopValidator(_id=_id)
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
