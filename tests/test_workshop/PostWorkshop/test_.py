import unittest
import requests

from tests import Server, WorkshopTest, WorkshopCategories
from tests.test_workshop.PostWorkshop import PostWorkshop, PostWorkshopRepBody


class TestPostWorkshop(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_api_ok(self):
        """ Default case.

        Return
            201 - Workshop Created.
        """
        """ env """
        body = {PostWorkshop.param_name: "qaRHR_name"}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        tc_workshop: WorkshopTest = PostWorkshop().workshop_set_from_body(body).set_id(response_body.get_id())
        """ assert """
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 201)
        self.assertEqual(response_body.msg, PostWorkshop.msg_success)
        self.assertEqual(response_body.data, PostWorkshopRepBody.data_expected(tc_workshop))
        self.assertNotIn("detail", response_body)
        """ check bdd"""
        tc_workshop.check_exist_by_id()

    def test_api_all_keys(self):
        """ All key case.

        Return
            201 - Workshop Created.
        """
        """ env """
        body = {"_id": "qaRHR_id",
                PostWorkshop.param_name: "qaRHR_name",
                PostWorkshop.param_description: "qaRHR_description",
                PostWorkshop.param_categories: [WorkshopCategories.Cardio.value],
                "files": ["invalid"],
                "invalid": "invalid"}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        tc_workshop: WorkshopTest = PostWorkshop().workshop_set_from_body(body).set_id(response_body.get_id())
        """ assert """
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 201)
        self.assertEqual(response_body.msg, PostWorkshop.msg_success)
        self.assertEqual(response_body.data, PostWorkshopRepBody.data_expected(tc_workshop))
        self.assertNotIn("detail", response_body)
        """ check bdd"""
        tc_workshop.check_exist_by_id()

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestPostWorkshop())


if __name__ == '__main__':
    unittest.main()
