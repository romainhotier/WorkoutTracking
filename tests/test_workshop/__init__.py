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
        self.categories = []
        self.files = []
        for k, v in kwargs.items():
            try:
                self.__setattr__(k, v)
            except ValueError:
                pass

    def set_id(self, _id):
        self.id = _id
        return self

    def update(self, **kwargs):
        for k, v in kwargs.items():
            try:
                self.__setattr__(k, v)
            except ValueError:
                pass
        return self

    def add_files(self, files: list):
        self.files = self.files + [f'{file.parent}/{file.name}' for file in files]
        return self

    def add_files_in_mongo(self, files: list):
        self.files = self.files + [f'{file.parent}/{file.name}' for file in files]
        for file in files:
            mongo.db.workshop.update_one({"_id": ObjectId(self.id)}, {'$push': {"files": f'{file.parent}/{file.name}'}})
        return self

    def delete_files(self, files: list):
        for file in files:
            self.files.remove(f'{file.parent}/{file.name}')
        return self

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

    def check_doesnt_exist_by_name(self):
        """ Check a WorkshopTest doesn't exist by name. """
        assert mongo.db.workshop.find_one({"name": self.name}) is None

    def check_data_by_id(self):
        """ Check WorkshopTest's data from Mongo by _id. """
        assert self == WorkshopTest(**mongo.db.workshop.find_one({"_id": ObjectId(self.id)})).set_id(self.id)

    @staticmethod
    def count():
        """ Count Workshop in bdd. """
        return mongo.db.workshop.count_documents({})

    @staticmethod
    def clean():
        """ Delete all WorkshopTest in bdd. """
        rgx = re.compile('.*qaRHR.*', re.IGNORECASE)
        mongo.db.workshop.delete_many({"name": {"$regex": rgx}})
