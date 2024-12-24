# coding: utf-8

"""
    SendX REST API

    # Introduction SendX is an email marketing product. It helps you convert website visitors to customers, send them promotional emails, engage with them using drip sequences and craft custom journeys using powerful but simple automations. The SendX API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs. The SendX Rest API doesn’t support bulk updates. You can work on only one object per request. <br> 

    The version of the OpenAPI document: 1.0.0
    Contact: support@sendx.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sendx_python_sdk.api.webhook_api import WebhookApi


class TestWebhookApi(unittest.TestCase):
    """WebhookApi unit test stubs"""

    def setUp(self) -> None:
        self.api = WebhookApi()

    def tearDown(self) -> None:
        pass

    def test_create_team_webhook(self) -> None:
        """Test case for create_team_webhook

        Create TeamWebhook
        """
        pass

    def test_delete_team_webhook(self) -> None:
        """Test case for delete_team_webhook

        Delete Team Webhook
        """
        pass

    def test_get_all_team_webhook(self) -> None:
        """Test case for get_all_team_webhook

        Get All team Webhook
        """
        pass

    def test_get_team_webhook(self) -> None:
        """Test case for get_team_webhook

        Get TeamWebhook
        """
        pass

    def test_update_team_webhook(self) -> None:
        """Test case for update_team_webhook

        Update Team Webhook
        """
        pass


if __name__ == '__main__':
    unittest.main()
