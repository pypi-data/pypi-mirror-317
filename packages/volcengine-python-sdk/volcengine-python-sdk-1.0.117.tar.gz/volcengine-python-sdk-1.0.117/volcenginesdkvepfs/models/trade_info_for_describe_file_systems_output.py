# coding: utf-8

"""
    vepfs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class TradeInfoForDescribeFileSystemsOutput(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'account_id': 'str',
        'customer_name': 'str',
        'identity': 'str',
        'is_test': 'bool'
    }

    attribute_map = {
        'account_id': 'AccountId',
        'customer_name': 'CustomerName',
        'identity': 'Identity',
        'is_test': 'IsTest'
    }

    def __init__(self, account_id=None, customer_name=None, identity=None, is_test=None, _configuration=None):  # noqa: E501
        """TradeInfoForDescribeFileSystemsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._account_id = None
        self._customer_name = None
        self._identity = None
        self._is_test = None
        self.discriminator = None

        if account_id is not None:
            self.account_id = account_id
        if customer_name is not None:
            self.customer_name = customer_name
        if identity is not None:
            self.identity = identity
        if is_test is not None:
            self.is_test = is_test

    @property
    def account_id(self):
        """Gets the account_id of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501


        :return: The account_id of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this TradeInfoForDescribeFileSystemsOutput.


        :param account_id: The account_id of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def customer_name(self):
        """Gets the customer_name of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501


        :return: The customer_name of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :rtype: str
        """
        return self._customer_name

    @customer_name.setter
    def customer_name(self, customer_name):
        """Sets the customer_name of this TradeInfoForDescribeFileSystemsOutput.


        :param customer_name: The customer_name of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :type: str
        """

        self._customer_name = customer_name

    @property
    def identity(self):
        """Gets the identity of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501


        :return: The identity of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :rtype: str
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """Sets the identity of this TradeInfoForDescribeFileSystemsOutput.


        :param identity: The identity of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :type: str
        """

        self._identity = identity

    @property
    def is_test(self):
        """Gets the is_test of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501


        :return: The is_test of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :rtype: bool
        """
        return self._is_test

    @is_test.setter
    def is_test(self, is_test):
        """Sets the is_test of this TradeInfoForDescribeFileSystemsOutput.


        :param is_test: The is_test of this TradeInfoForDescribeFileSystemsOutput.  # noqa: E501
        :type: bool
        """

        self._is_test = is_test

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TradeInfoForDescribeFileSystemsOutput, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TradeInfoForDescribeFileSystemsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TradeInfoForDescribeFileSystemsOutput):
            return True

        return self.to_dict() != other.to_dict()
