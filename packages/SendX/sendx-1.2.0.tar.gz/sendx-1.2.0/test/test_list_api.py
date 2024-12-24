# coding: utf-8

"""
    SendX REST API

    # Introduction The SendX API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs. The SendX Rest API doesn’t support bulk updates. You can work on only one object per request. <br> 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sendx_python_sdk.api.list_api import ListApi


class TestListApi(unittest.TestCase):
    """ListApi unit test stubs"""

    def setUp(self) -> None:
        self.api = ListApi()

    def tearDown(self) -> None:
        pass

    def test_create_list(self) -> None:
        """Test case for create_list

        Create List
        """
        pass

    def test_delete_list(self) -> None:
        """Test case for delete_list

        Delete List
        """
        pass

    def test_get_all_lists(self) -> None:
        """Test case for get_all_lists

        Get All Lists
        """
        pass

    def test_get_list_by_id(self) -> None:
        """Test case for get_list_by_id

        Get List
        """
        pass

    def test_update_list(self) -> None:
        """Test case for update_list

        Update List
        """
        pass


if __name__ == '__main__':
    unittest.main()
