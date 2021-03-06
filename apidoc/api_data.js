define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "../WorkoutTracking/apidoc/main.js",
    "group": "/Users/romain.hotier/workspace/rhr/WorkoutTracking/apidoc/main.js",
    "groupTitle": "/Users/romain.hotier/workspace/rhr/WorkoutTracking/apidoc/main.js",
    "name": ""
  },
  {
    "type": "delete",
    "url": "/workshop/<_id>",
    "title": "DeleteWorkshop",
    "group": "Workshop",
    "description": "<p>Delete a Workshop by it's ObjectId</p>",
    "parameter": {
      "fields": {
        "Query param": [
          {
            "group": "Query param",
            "type": "String",
            "optional": false,
            "field": "_id",
            "description": "<p>Workshop's ObjectId</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Example usage:",
        "content": "DELETE http://127.0.0.1:5000/workshop/<_id>",
        "type": "json"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success response:",
          "content": "HTTPS 200\n{\n    \"status\": 200,\n    \"msg\": \"workoutTracking.workshop.deleteWorkshop.success\",\n    \"data\": {\"description\": \"Workshop's description\", \"id\": \"61dc2a02dc8493a5f471d2fe\",\n              \"media\": [], \"name\": \"qaRHR_name1\", \"category\": []}\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error response:",
          "content": "HTTPS 400\n{\n    \"status\": 404,\n    \"msg\": \"workoutTracking.workshop.notFound\",\n    \"detail\": {\"msg\": \"Doesn't exist\", \"param\": \"_id\",\"value\": \"aaaaaaaaaaaaaaaaaaaaaaaa\"}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "../WorkoutTracking/flaskr/workshop/router.py",
    "groupTitle": "Workshop",
    "name": "DeleteWorkshop_id"
  },
  {
    "type": "get",
    "url": "/workshop",
    "title": "GetAllWorkshop",
    "group": "Workshop",
    "description": "<p>Get Workshop ($AND between each parameter if sent)</p>",
    "parameter": {
      "fields": {
        "Query param": [
          {
            "group": "Query param",
            "type": "String",
            "optional": true,
            "field": "name",
            "description": "<p>Workshop's name ($OR in search)</p>"
          },
          {
            "group": "Query param",
            "type": "String",
            "optional": true,
            "field": "description",
            "description": "<p>Workshop's description ($OR in search)</p>"
          },
          {
            "group": "Query param",
            "type": "String",
            "optional": true,
            "field": "category",
            "description": "<p>Workshop's category in ['cardio', 'fitness', 'strength'] ($AND in search)</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Example usage:",
        "content": "GET http://127.0.0.1:5000/ingredient",
        "type": "json"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success response:",
          "content": "HTTPS 200\n{\n    \"status\": 200,\n    \"msg\": \"workoutTracking.workshop.deleteWorkshop.success\",\n    \"data\": [{\"description\": \"Workshop's description\", \"id\": \"61dc2a02dc8493a5f471d2fe\",\n              \"media\": [], \"name\": \"qaRHR_name1\", \"category\": []},\n              {\"description\": \"Workshop's description\", \"id\": \"61dc2a02dc8493a5f471d2ff\",\n              \"media\": [], \"name\": \"qaRHR_name2\", \"category\": []}]\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "../WorkoutTracking/flaskr/workshop/router.py",
    "groupTitle": "Workshop",
    "name": "GetWorkshop"
  },
  {
    "type": "get",
    "url": "/workshop/<_id>",
    "title": "GetWorkshop",
    "group": "Workshop",
    "description": "<p>Get a workshop by it's ObjectId</p>",
    "parameter": {
      "fields": {
        "Query param": [
          {
            "group": "Query param",
            "type": "String",
            "optional": false,
            "field": "_id",
            "description": "<p>Workshop's ObjectId</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Example usage:",
        "content": "GET http://127.0.0.1:5000/workshop/<_id>",
        "type": "json"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success response:",
          "content": "HTTPS 200\n{\n    \"status\": 200,\n    \"msg\": \"workoutTracking.workshop.deleteWorkshop.success\",\n    \"data\": {\"description\": \"Workshop's description\", \"id\": \"61dc2a02dc8493a5f471d2fe\",\n              \"media\": [], \"name\": \"qaRHR_name1\", \"category\": []}\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error response:",
          "content": "HTTPS 400\n{\n    \"status\": 404,\n    \"msg\": \"workoutTracking.workshop.notFound\",\n    \"detail\": {\"msg\": \"Doesn't exist\", \"param\": \"_id\",\"value\": \"aaaaaaaaaaaaaaaaaaaaaaaa\"}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "../WorkoutTracking/flaskr/workshop/router.py",
    "groupTitle": "Workshop",
    "name": "GetWorkshop_id"
  },
  {
    "type": "post",
    "url": "/workshop",
    "title": "PostWorkshop",
    "group": "Workshop",
    "description": "<p>Create a Workshop</p>",
    "parameter": {
      "fields": {
        "Body param": [
          {
            "group": "Body param",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Workshop's name</p>"
          },
          {
            "group": "Body param",
            "type": "String",
            "optional": true,
            "field": "description",
            "defaultValue": "Workshop's description",
            "description": "<p>Workshop's description</p>"
          },
          {
            "group": "Body param",
            "type": "Array",
            "optional": true,
            "field": "category",
            "defaultValue": "Empty_Array",
            "description": "<p>Workshop's category in ['cardio', 'fitness', 'strength']</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Example usage:",
        "content": "POST http://127.0.0.1:5000/workshop\n{\n    \"name\": <name>,\n    \"description\": <description>,\n    \"type\": [\"cardio\", \"fitness\"],\n}",
        "type": "json"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success response:",
          "content": "HTTPS 201\n{\n    \"status\": 201,\n    \"msg\": \"workoutTracking.workshop.postWorkshop.success\",\n    \"data\": {\"category\": [\"cardio\"], \"description\": \"qaRHR_description\", \"id\": \"61dc31e09aa1edbdfe1e5aa7\",\n             \"media\": [], \"name\": \"qaRHR_name\"}\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error response:",
          "content": "HTTPS 400\n{\n    \"status\": 400,\n    \"msg\": \"workoutTracking.workshop.badRequest\",\n    \"detail\": {\"msg\": \"Must be a String not empty\", \"param\": \"name\", \"value\": \"\"}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "../WorkoutTracking/flaskr/workshop/router.py",
    "groupTitle": "Workshop",
    "name": "PostWorkshop"
  }
] });
