import unittest
import requests

from tests import Server, WorkshopTest, ErrorMsg
from tests.test_workshop.DeleteWorkshop import DeleteWorkshop, DeleteWorkshopRepBody


class TestDeleteWorkshop(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_id_without(self):
        """ Without _id.

        Return
            405 - Method not Allowed.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1").insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2").insert()
        tc_id = ""
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshop.url}/{tc_id}'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 405)
        self.assertEqual(response_body.msg, DeleteWorkshop.msg_notAllowed)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail, ErrorMsg.MethodIsNotAllowed.value)
        """ check bdd"""
        tc_workshop1.check_data_by_id()
        tc_workshop2.check_data_by_id()

    def test_id_string_invalid(self):
        """ _id is an invalid string.

        Return
            400 - Bad Request.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1").insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2").insert()
        tc_id = "invalid"
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshop.url}/{tc_id}'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, DeleteWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         DeleteWorkshopRepBody.detail_expected(param=DeleteWorkshop.param_id,
                                                               msg=ErrorMsg.MustBeAnObjectId.value,
                                                               value=tc_id))
        """ check bdd"""
        tc_workshop1.check_data_by_id()
        tc_workshop2.check_data_by_id()

    def test_id_objectId_invalid(self):
        """ _id is an invalid ObjectId.

        Return
            404 - Not Found.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1").insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2").insert()
        tc_id = "aaaaaaaaaaaaaaaaaaaaaaaa"
        """ call api """
        url = f'{Server.main_url}/{DeleteWorkshop.url}/{tc_id}'
        response = requests.delete(url, verify=False)
        response_body = DeleteWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 404)
        self.assertEqual(response_body.msg, DeleteWorkshop.msg_notFound)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         DeleteWorkshopRepBody.detail_expected(param=DeleteWorkshop.param_id,
                                                               msg=ErrorMsg.DoesntExist.value,
                                                               value=tc_id))
        """ check bdd"""
        tc_workshop1.check_data_by_id()
        tc_workshop2.check_data_by_id()

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestDeleteWorkshop())


if __name__ == '__main__':
    unittest.main()
