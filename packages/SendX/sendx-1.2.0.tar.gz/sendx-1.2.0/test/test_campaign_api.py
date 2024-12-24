# coding: utf-8

"""
    SendX REST API

    # Introduction The SendX API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs. The SendX Rest API doesn’t support bulk updates. You can work on only one object per request. <br> 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sendx_python_sdk.api.campaign_api import CampaignApi


class TestCampaignApi(unittest.TestCase):
    """CampaignApi unit test stubs"""

    def setUp(self) -> None:
        self.api = CampaignApi()

    def tearDown(self) -> None:
        pass

    def test_create_campaign(self) -> None:
        """Test case for create_campaign

        Create Campaign
        """
        pass

    def test_delete_campaign(self) -> None:
        """Test case for delete_campaign

        Delete Campaign
        """
        pass

    def test_edit_campaign(self) -> None:
        """Test case for edit_campaign

        Edit Campaign
        """
        pass

    def test_get_all_campaigns(self) -> None:
        """Test case for get_all_campaigns

        Get All Campaigns
        """
        pass

    def test_get_campaign_by_id(self) -> None:
        """Test case for get_campaign_by_id

        Get Campaign By Id
        """
        pass


if __name__ == '__main__':
    unittest.main()
