import unittest
import requests

from tests import Server, File, WorkshopTest, ErrorMsg
from tests.test_workshop.DeleteWorkshopFiles import DeleteWorkshopFiles, DeleteWorkshopFilesRepBody


class TestDeleteWorkshopFiles(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_filenames_without(self):
        """ Without filenames.

        Return
            400 - Bad Request.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = tc_workshop.id
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_id}').create()
        tc_workshop.add_files_in_mongo(files=[tc_file1])
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshopFiles.url1}/{tc_id}/{DeleteWorkshopFiles.url2}?'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, DeleteWorkshopFiles.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         DeleteWorkshopFilesRepBody.detail_expected_error(param=DeleteWorkshopFiles.param_filenames,
                                                                          msg=ErrorMsg.MustBeAListOfStringNotEmpty.value,
                                                                          value=[]))
        """ check bdd """
        tc_workshop.check_data_by_id()
        """ check storage """
        tc_file1.check_file_storage(exist=True)

    def test_filenames_string_invalid(self):
        """ filenames is an invalid string.

        Return
            400 - Bad Request.
        """
        """ env """
        tc_workshop = WorkshopTest().insert()
        tc_id = tc_workshop.id
        tc_file1 = File(name="qaRHR_text.txt", parent=f'workshop/{tc_id}').create()
        tc_workshop.add_files_in_mongo(files=[tc_file1])
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshopFiles.url1}/{tc_id}/{DeleteWorkshopFiles.url2}?' \
              f'{DeleteWorkshopFiles.param_filenames}[]=invalid&'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopFilesRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, DeleteWorkshopFiles.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         DeleteWorkshopFilesRepBody.detail_expected_error(param=DeleteWorkshopFiles.param_filenames,
                                                                          msg=ErrorMsg.DoesntExist.value,
                                                                          value="invalid"))
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
