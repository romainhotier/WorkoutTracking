import unittest
import requests

from tests import Server, File, WorkshopTest, ErrorMsg
from tests.test_workshop.DeleteWorkshopFiles import DeleteWorkshopFiles, DeleteWorkshopFilesRepBody
from tests.test_workshop.DeleteWorkshop import DeleteWorkshop, DeleteWorkshopRepBody


class TestDeleteWorkshopFiles(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_id_without(self):
        """ Without _id.

        Return
            400 - Bad Request from DeleteWorkshop.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = ""
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_workshop.id}').create()
        tc_workshop.add_files_in_mongo(files=[tc_file1])
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshopFiles.url1}/{tc_id}/{DeleteWorkshopFiles.url2}?' \
              f'{DeleteWorkshopFiles.param_filenames}[]={tc_file1.name}&'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, DeleteWorkshopFiles.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         DeleteWorkshopRepBody.detail_expected(param=DeleteWorkshop.param_id,
                                                               msg=ErrorMsg.MustBeAnObjectId.value,
                                                               value=DeleteWorkshopFiles.url2))
        """ check bdd """
        tc_workshop.check_data_by_id()
        """ check storage """
        tc_file1.check_file_storage(exist=True)

    def test_id_string_invalid(self):
        """ _id is an invalid string.

        Return
            400 - Bad Request.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = "invalid"
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_workshop.id}').create()
        tc_workshop.add_files_in_mongo(files=[tc_file1])
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshopFiles.url1}/{tc_id}/{DeleteWorkshopFiles.url2}?' \
              f'{DeleteWorkshopFiles.param_filenames}[]={tc_file1.name}&'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, DeleteWorkshopFiles.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         DeleteWorkshopFilesRepBody.detail_expected_error(param=DeleteWorkshopFiles.param_id,
                                                                          msg=ErrorMsg.MustBeAnObjectId.value,
                                                                          value=tc_id))
        """ check bdd """
        tc_workshop.check_data_by_id()
        """ check storage """
        tc_file1.check_file_storage(exist=True)

    def test_id_objectId_invalid(self):
        """ _id is an invalid ObjectId.

        Return
            404 - Not Found.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = "aaaaaaaaaaaaaaaaaaaaaaaa"
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_workshop.id}').create()
        tc_workshop.add_files_in_mongo(files=[tc_file1])
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshopFiles.url1}/{tc_id}/{DeleteWorkshopFiles.url2}?' \
              f'{DeleteWorkshopFiles.param_filenames}[]={tc_file1.name}&'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 404)
        self.assertEqual(response_body.msg, DeleteWorkshopFiles.msg_notFound)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         DeleteWorkshopFilesRepBody.detail_expected_error(param=DeleteWorkshopFiles.param_id,
                                                                          msg=ErrorMsg.DoesntExist.value,
                                                                          value=tc_id))
        """ check bdd """
        tc_workshop.check_data_by_id()
        """ check storage """
        tc_file1.check_file_storage(exist=True)

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestDeleteWorkshopFiles())
        Server.clean_tests_files()


if __name__ == '__main__':
    unittest.main()
