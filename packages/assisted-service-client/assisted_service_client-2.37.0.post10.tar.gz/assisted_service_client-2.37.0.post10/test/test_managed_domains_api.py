# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import assisted_service_client
from assisted_service_client.api.managed_domains_api import ManagedDomainsApi  # noqa: E501
from assisted_service_client.rest import ApiException


class TestManagedDomainsApi(unittest.TestCase):
    """ManagedDomainsApi unit test stubs"""

    def setUp(self):
        self.api = assisted_service_client.api.managed_domains_api.ManagedDomainsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_v2_list_managed_domains(self):
        """Test case for v2_list_managed_domains

        """
        pass


if __name__ == '__main__':
    unittest.main()
