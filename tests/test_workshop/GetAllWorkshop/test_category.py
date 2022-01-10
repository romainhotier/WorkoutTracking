import unittest
import requests

from tests import Server, WorkshopTest, WorkshopType, ErrorMsg
from tests.test_workshop.GetAllWorkshop import GetAllWorkshop, GetAllWorkshopRepBody


class TestGetAllWorkshop(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_category_without(self):
        """ Without category.

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

    def test_category_string_empty(self):
        """ category is an empty string.

        Return
            200 - All Workshop.
        """
        """ env """
        WorkshopTest(name="qaRHR_name1", category=WorkshopType.list()).insert()
        WorkshopTest(name="qaRHR_name2", category=[WorkshopType.Fitness.value]).insert()
        """ call api """
        url = f'{Server.main_url}/{GetAllWorkshop.url}?{GetAllWorkshop.param_category}='
        response = requests.get(url, verify=False)
        response_body = GetAllWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, GetAllWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         GetAllWorkshopRepBody.detail_expected(param=GetAllWorkshop.param_category,
                                                               msg=ErrorMsg.MustBeInWorkShopCategory.value,
                                                               value=[""]))

    def test_category_string(self):
        """ category is a string.

        Return
            200 - All Workshop.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1", category=WorkshopType.list()).insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2", category=[WorkshopType.Fitness.value]).insert()
        """ call api """
        url = f'{Server.main_url}/{GetAllWorkshop.url}?{GetAllWorkshop.param_category}={WorkshopType.Cardio.value}'
        response = requests.get(url, verify=False)
        response_body = GetAllWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 200)
        self.assertEqual(response_body.msg, GetAllWorkshop.msg_success)
        self.assertIn(GetAllWorkshopRepBody.data_expected(tc_workshop1), response_body.data)
        self.assertNotIn(GetAllWorkshopRepBody.data_expected(tc_workshop2), response_body.data)
        self.assertNotIn("detail", response_body)

    def test_category_string_multiple(self):
        """ category is a string several times.

        Return
            200 - All Workshop.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1", category=WorkshopType.list()).insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2", category=[WorkshopType.Fitness.value]).insert()
        tc_workshop3 = WorkshopTest(name="qaRHR_name3", category=[WorkshopType.Cardio.value,
                                                                  WorkshopType.Strength.value]).insert()
        tc_workshop4 = WorkshopTest(name="qaRHR_name3", category=[WorkshopType.Fitness.value,
                                                                  WorkshopType.Cardio.value]).insert()
        """ call api """
        url = f'{Server.main_url}/{GetAllWorkshop.url}?' \
              f'{GetAllWorkshop.param_category}={WorkshopType.Cardio.value}&' \
              f'{GetAllWorkshop.param_category}={WorkshopType.Fitness.value}'
        response = requests.get(url, verify=False)
        response_body = GetAllWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 200)
        self.assertEqual(response_body.msg, GetAllWorkshop.msg_success)
        self.assertIn(GetAllWorkshopRepBody.data_expected(tc_workshop1), response_body.data)
        self.assertNotIn(GetAllWorkshopRepBody.data_expected(tc_workshop2), response_body.data)
        self.assertNotIn(GetAllWorkshopRepBody.data_expected(tc_workshop3), response_body.data)
        self.assertIn(GetAllWorkshopRepBody.data_expected(tc_workshop4), response_body.data)
        self.assertNotIn("detail", response_body)

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestGetAllWorkshop())


if __name__ == '__main__':
    unittest.main()
