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

from sendx_python_sdk.models.identify_response import IdentifyResponse

class TestIdentifyResponse(unittest.TestCase):
    """IdentifyResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> IdentifyResponse:
        """Test IdentifyResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `IdentifyResponse`
        """
        model = IdentifyResponse()
        if include_optional:
            return IdentifyResponse(
                status = '',
                message = '',
                data = sendx_python_sdk.models.contact.Contact(
                    id = 'a1b2c3d4e5', 
                    first_name = 'Jane', 
                    last_name = 'Doe', 
                    email = 'jane.doe@example.com', 
                    company = 'Tech Solutions Inc.', 
                    custom_fields = {"1":"VIP","2":"Special Offer Subscriber"}, 
                    unsubscribed = False, 
                    bounced = False, 
                    spam = False, 
                    created = '2024-10-08T09:30Z', 
                    updated = '2024-10-08T12:45Z', 
                    blocked = False, 
                    dropped = False, 
                    ltv = 5000, 
                    contact_source = 8, 
                    last_tracked_ip = '192.168.0.1', 
                    lists = ["sendx123","sendx233"], 
                    tags = ["223","3232"], )
            )
        else:
            return IdentifyResponse(
        )
        """

    def testIdentifyResponse(self):
        """Test IdentifyResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
