import unittest
import requests

from tests import Server, File, WorkshopTest, ErrorMsg
from tests.test_workshop.PostWorkshopFiles import PostWorkshopFiles, PostWorkshopFilesRepBody


class TestPostWorkshopFiles(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_id_without(self):
        """ Without _id.

        Return
            405 - Method not Allowed.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = ""
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_id}')
        tc_file2 = File(name="qaRHR_image.png", parent=f'workshop/{tc_id}')
        tc_files = [('files', open(tc_file1.origin_path, 'rb')),
                    ('files', open(tc_file2.origin_path, 'rb'))]
        """ call api """
        url = f'{Server.main_url}/{PostWorkshopFiles.url1}/{tc_id}/{PostWorkshopFiles.url2}'
        response = requests.post(url, files=tc_files, verify=False)
        response_body = PostWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 405)
        self.assertEqual(response_body.msg, PostWorkshopFiles.msg_notAllowed_root)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail, ErrorMsg.MethodIsNotAllowed.value)
        """ check bdd """
        tc_workshop.check_data_by_id()
        """ check storage """
        tc_file1.check_file_storage(exist=False)
        tc_file2.check_file_storage(exist=False)

    def test_id_string_invalid(self):
        """ _id is an invalid string.

        Return
            400 - Bad Request.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = "invalid"
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_id}')
        tc_file2 = File(name="qaRHR_image.png", parent=f'workshop/{tc_id}')
        tc_files = [('files', open(tc_file1.origin_path, 'rb')),
                    ('files', open(tc_file2.origin_path, 'rb'))]
        """ call api """
        url = f'{Server.main_url}/{PostWorkshopFiles.url1}/{tc_id}/{PostWorkshopFiles.url2}'
        response = requests.post(url, files=tc_files, verify=False)
        response_body = PostWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, PostWorkshopFiles.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         PostWorkshopFilesRepBody.detail_expected_error(param=PostWorkshopFiles.param_id,
                                                                        msg=ErrorMsg.MustBeAnObjectId.value,
                                                                        value=tc_id))
        """ check bdd """
        tc_workshop.check_data_by_id()
        """ check storage """
        tc_file1.check_file_storage(exist=False)
        tc_file2.check_file_storage(exist=False)

    def test_id_objectId_invalid(self):
        """ _id is an invalid ObjectId.

        Return
            404 - Not Found.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = "aaaaaaaaaaaaaaaaaaaaaaaa"
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_id}')
        tc_file2 = File(name="qaRHR_image.png", parent=f'workshop/{tc_id}')
        tc_files = [('files', open(tc_file1.origin_path, 'rb')),
                    ('files', open(tc_file2.origin_path, 'rb'))]
        """ call api """
        url = f'{Server.main_url}/{PostWorkshopFiles.url1}/{tc_id}/{PostWorkshopFiles.url2}'
        response = requests.post(url, files=tc_files, verify=False)
        response_body = PostWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 404)
        self.assertEqual(response_body.msg, PostWorkshopFiles.msg_notFound)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         PostWorkshopFilesRepBody.detail_expected_error(param=PostWorkshopFiles.param_id,
                                                                        msg=ErrorMsg.DoesntExist.value,
                                                                        value=tc_id))
        """ check bdd """
        tc_workshop.check_data_by_id()
        """ check storage """
        tc_file1.check_file_storage(exist=False)
        tc_file2.check_file_storage(exist=False)

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestPostWorkshopFiles())
        Server.clean_tests_files()


if __name__ == '__main__':
    unittest.main()
