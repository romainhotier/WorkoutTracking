""" Workshop Model """
import re
from bson import ObjectId

from tests import mongo
from flaskr.workshop.model import Workshop


class WorkshopTest(Workshop):

    def __init__(self, **kwargs):
        super(Workshop, self).__init__(**kwargs)
        self.id = str(ObjectId())
        self.name = "qaRHR_workshopName"
        self.description = "Workshop's description"
        self.type = []
        self.media = []
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def insert(self):
        """ Insert a WorkshopTest and return it. """
        data = self.dict()
        data.pop("id")
        query = mongo.db.workshop.insert_one(data)
        self.id = str(query.inserted_id)
        return self

    def delete(self):
        """ Delete a WorkshopTest. """
        mongo.db.workshop.delete_one({"_id": ObjectId(self.id)})

    def check_exist_by_id(self):
        """ Check a WorkshopTest exist by _id. """
        assert mongo.db.workshop.find_one({"_id": ObjectId(self.id)}) is not None

    def check_doesnt_exist_by_id(self):
        """ Check a WorkshopTest doesn't exist by _id. """
        assert mongo.db.workshop.find_one({"_id": ObjectId(self.id)}) is None

    @staticmethod
    def count():
        """ Count Workshop in bdd. """
        return mongo.db.workshop.count_documents({})

    @staticmethod
    def clean():
        """ Delete all WorkshopTest in bdd. """
        rgx = re.compile('.*qaRHR.*', re.IGNORECASE)
        mongo.db.workshop.delete_many({"name": {"$regex": rgx}})