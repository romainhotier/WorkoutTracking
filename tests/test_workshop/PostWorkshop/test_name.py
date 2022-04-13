import unittest
import requests

from tests import Server, WorkshopTest, ErrorMsg
from tests.test_workshop.PostWorkshop import PostWorkshop, PostWorkshopRepBody


class TestPostWorkshop(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_name_without(self):
        """ Without name.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, PostWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_name,
                                                             msg=ErrorMsg.IsRequired.value))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def test_name_null(self):
        """ name is None.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: None}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, PostWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_name,
                                                             msg=ErrorMsg.IsRequired.value,
                                                             value=body[PostWorkshop.param_name]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def test_name_string_empty(self):
        """ name is an empty string.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: ""}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, PostWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_name,
                                                             msg=ErrorMsg.MustBeAStringNotEmpty.value,
                                                             value=body[PostWorkshop.param_name]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def test_name_string(self):
        """ name is a string.

        Return
            201 - Workshop Created.
        """
        """ env """
        body = {PostWorkshop.param_name: "qaRHR_invalid"}
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
        tc_workshop.check_data_by_id()

    def test_name_list(self):
        """ name is a list.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: []}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, PostWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_name,
                                                             msg=ErrorMsg.MustBeAString.value,
                                                             value=body[PostWorkshop.param_name]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def test_name_dict(self):
        """ name is a dict.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: {}}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, PostWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_name,
                                                             msg=ErrorMsg.MustBeAString.value,
                                                             value=body[PostWorkshop.param_name]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestPostWorkshop())


if __name__ == '__main__':
    unittest.main()
