import unittest
import requests

from tests import Server, WorkshopTest, WorkshopCategories, ErrorMsg
from tests.test_workshop.PostWorkshop import PostWorkshop, PostWorkshopRepBody


class TestPostWorkshop(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def type_category_without(self):
        """ Without category.

        Return
            201 - Workshop Created.
        """
        """ env """
        body = {PostWorkshop.param_name: "qaRHR_workshopName"}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        tc_workshop: WorkshopTest = PostWorkshop().workshop_set_from_body(body).set_id(response_body.get_id())
        """ assert """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 200)
        self.assertEqual(response_body.msg, PostWorkshop.msg_success)
        self.assertEqual(response_body.data, PostWorkshopRepBody.data_expected(tc_workshop))
        self.assertNotIn("detail", response_body)
        """ check bdd"""
        tc_workshop.check_exist_by_id()

    def type_category_null(self):
        """ category is None.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: "qaRHR_workshopName",
                PostWorkshop.param_categories: None}
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
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_categories,
                                                             msg=ErrorMsg.MustBeAList.value,
                                                             value=body[PostWorkshop.param_categories]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def type_category_string_empty(self):
        """ category is an empty string.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: "qaRHR_workshopName",
                PostWorkshop.param_categories: ""}
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
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_categories,
                                                             msg=ErrorMsg.MustBeAList.value,
                                                             value=body[PostWorkshop.param_categories]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def type_category_string(self):
        """ category is a string.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: "qaRHR_workshopName",
                PostWorkshop.param_categories: "invalid"}
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
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_categories,
                                                             msg=ErrorMsg.MustBeAList.value,
                                                             value=body[PostWorkshop.param_categories]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def type_category_list_empty(self):
        """ category is an empty list.

        Return
            200 - Workshop Created.
        """
        """ env """
        body = {PostWorkshop.param_name: "qaRHR_workshopName",
                PostWorkshop.param_categories: []}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        tc_workshop: WorkshopTest = PostWorkshop().workshop_set_from_body(body).set_id(response_body.get_id())
        """ assert """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 200)
        self.assertEqual(response_body.msg, PostWorkshop.msg_success)
        self.assertEqual(response_body.data, PostWorkshopRepBody.data_expected(tc_workshop))
        self.assertNotIn("detail", response_body)
        """ check bdd"""
        tc_workshop.check_exist_by_id()

    def type_category_list_invalid(self):
        """ category is an invalid list.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: "qaRHR_workshopName",
                PostWorkshop.param_categories: ["invalid", WorkshopCategories.Cardio.value]}
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
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_categories,
                                                             msg=ErrorMsg.MustBeInWorkshopCategories.value,
                                                             value=body[PostWorkshop.param_categories]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    def type_category_list_valid(self):
        """ category is a valid list.

        Return
            200 - Workshop Created.
        """
        """ env """
        body = {PostWorkshop.param_name: "qaRHR_workshopName",
                PostWorkshop.param_categories: WorkshopCategories.list()}
        """ call api """
        url = f'{Server.main_url}/{PostWorkshop.url}'
        response = requests.post(url, json=body, verify=False)
        response_body = PostWorkshopRepBody(**response.json())
        tc_workshop: WorkshopTest = PostWorkshop().workshop_set_from_body(body).set_id(response_body.get_id())
        """ assert """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 200)
        self.assertEqual(response_body.msg, PostWorkshop.msg_success)
        self.assertEqual(response_body.data, PostWorkshopRepBody.data_expected(tc_workshop))
        self.assertNotIn("detail", response_body)
        """ check bdd"""
        tc_workshop.check_exist_by_id()

    def type_category_dict(self):
        """ category is a dict.

        Return
            400 - Bad Request.
        """
        """ env """
        count_before = WorkshopTest().count()
        body = {PostWorkshop.param_name: "qaRHR_workshopName",
                PostWorkshop.param_categories: {}}
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
                         PostWorkshopRepBody.detail_expected(param=PostWorkshop.param_categories,
                                                             msg=ErrorMsg.MustBeAList.value,
                                                             value=body[PostWorkshop.param_categories]))
        """ check bdd"""
        self.assertEqual(count_before, WorkshopTest().count())

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestPostWorkshop())


if __name__ == '__main__':
    unittest.main()
