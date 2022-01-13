import unittest
import requests

from tests import Server, WorkshopTest, ErrorMsg
from tests.test_workshop.GetAllWorkshop import GetAllWorkshop, GetAllWorkshopRepBody


class TestGetAllWorkshop(unittest.TestCase):

    def setUp(self):
        WorkshopTest().clean()

    def test_description_without(self):
        """ Without description.

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

    def test_description_string_empty(self):
        """ description is an empty string.

        Return
            200 - All Workshop.
        """
        """ env """
        WorkshopTest(name="qaRHR_name1").insert()
        WorkshopTest(name="qaRHR_name2").insert()
        """ call api """
        url = f'{Server.main_url}/{GetAllWorkshop.url}?{GetAllWorkshop.param_description}='
        response = requests.get(url, verify=False)
        response_body = GetAllWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 400)
        self.assertEqual(response_body.msg, GetAllWorkshop.msg_badRequest)
        self.assertNotIn("data", response_body)
        self.assertEqual(response_body.detail,
                         GetAllWorkshopRepBody.detail_expected(param=GetAllWorkshop.param_description,
                                                               msg=ErrorMsg.MustBeAStringNotEmpty.value,
                                                               value=[""]))

    def test_description_string(self):
        """ description is a string.

        Return
            200 - All Workshop.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1", description="desc1").insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2", description="desc2").insert()
        """ call api """
        url = f'{Server.main_url}/{GetAllWorkshop.url}?{GetAllWorkshop.param_description}=desc1'
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

    def test_description_string_multiple(self):
        """ description is a string several times.

        Return
            200 - All Workshop.
        """
        """ env """
        tc_workshop1 = WorkshopTest(name="qaRHR_name1", description="desc1").insert()
        tc_workshop2 = WorkshopTest(name="qaRHR_name2", description="desc2").insert()
        tc_workshop3 = WorkshopTest(name="qaRHR_name3", description="desc3").insert()
        """ call api """
        url = f'{Server.main_url}/{GetAllWorkshop.url}?{GetAllWorkshop.param_description}=desc1' \
              f'&{GetAllWorkshop.param_description}=desc3'
        response = requests.get(url, verify=False)
        response_body = GetAllWorkshopRepBody(**response.json())
        """ assert """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response_body.status, 200)
        self.assertEqual(response_body.msg, GetAllWorkshop.msg_success)
        self.assertIn(GetAllWorkshopRepBody.data_expected(tc_workshop1), response_body.data)
        self.assertNotIn(GetAllWorkshopRepBody.data_expected(tc_workshop2), response_body.data)
        self.assertIn(GetAllWorkshopRepBody.data_expected(tc_workshop3), response_body.data)
        self.assertNotIn("detail", response_body)

    @classmethod
    def tearDownClass(cls):
        cls.setUp(TestGetAllWorkshop())


if __name__ == '__main__':
    unittest.main()
