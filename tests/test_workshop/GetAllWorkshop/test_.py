import unittest
import requests

from tests import Server, WorkshopTest
from tests.test_workshop.GetAllWorkshop import GetAllWorkshop, GetAllWorkshopRepBody


class TestGetAllWorkshop(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_api_ok(self):
        """ Default case.

        Return
            200 - All Workshop.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1").insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2").insert()
        """ call api """
        url = f'{Server.main_url}/{GetAllWorkshop.url}'
        response = requests.get(url, verify=False)
        response_body = GetAllWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 200)
        self.assertEqual(response_body.msg, GetAllWorkshop.msg_success)
        self.assertIn(GetAllWorkshopRepBody.data_expected(tc_workshop1), response_body.data)
        self.assertIn(GetAllWorkshopRepBody.data_expected(tc_workshop2), response_body.data)
        self.assertNotIn("detail", response_body)
        """ check bdd"""
        tc_workshop1.check_exist_by_id()
        tc_workshop2.check_exist_by_id()

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestGetAllWorkshop())


if __name__ == '__main__':
    unittest.main()
