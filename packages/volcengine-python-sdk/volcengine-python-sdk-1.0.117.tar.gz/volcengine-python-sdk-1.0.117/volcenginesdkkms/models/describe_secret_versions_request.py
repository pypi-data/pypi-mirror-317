# coding: utf-8

"""
    kms

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeSecretVersionsRequest(object):
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
        'current_page': 'int',
        'page_size': 'int',
        'secret_name': 'str'
    }

    attribute_map = {
        'current_page': 'CurrentPage',
        'page_size': 'PageSize',
        'secret_name': 'SecretName'
    }

    def __init__(self, current_page=None, page_size=None, secret_name=None, _configuration=None):  # noqa: E501
        """DescribeSecretVersionsRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._current_page = None
        self._page_size = None
        self._secret_name = None
        self.discriminator = None

        if current_page is not None:
            self.current_page = current_page
        if page_size is not None:
            self.page_size = page_size
        self.secret_name = secret_name

    @property
    def current_page(self):
        """Gets the current_page of this DescribeSecretVersionsRequest.  # noqa: E501


        :return: The current_page of this DescribeSecretVersionsRequest.  # noqa: E501
        :rtype: int
        """
        return self._current_page

    @current_page.setter
    def current_page(self, current_page):
        """Sets the current_page of this DescribeSecretVersionsRequest.


        :param current_page: The current_page of this DescribeSecretVersionsRequest.  # noqa: E501
        :type: int
        """
        if (self._configuration.client_side_validation and
                current_page is not None and current_page < 1):  # noqa: E501
            raise ValueError("Invalid value for `current_page`, must be a value greater than or equal to `1`")  # noqa: E501

        self._current_page = current_page

    @property
    def page_size(self):
        """Gets the page_size of this DescribeSecretVersionsRequest.  # noqa: E501


        :return: The page_size of this DescribeSecretVersionsRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this DescribeSecretVersionsRequest.


        :param page_size: The page_size of this DescribeSecretVersionsRequest.  # noqa: E501
        :type: int
        """
        if (self._configuration.client_side_validation and
                page_size is not None and page_size > 100):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value less than or equal to `100`")  # noqa: E501
        if (self._configuration.client_side_validation and
                page_size is not None and page_size < 1):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value greater than or equal to `1`")  # noqa: E501

        self._page_size = page_size

    @property
    def secret_name(self):
        """Gets the secret_name of this DescribeSecretVersionsRequest.  # noqa: E501


        :return: The secret_name of this DescribeSecretVersionsRequest.  # noqa: E501
        :rtype: str
        """
        return self._secret_name

    @secret_name.setter
    def secret_name(self, secret_name):
        """Sets the secret_name of this DescribeSecretVersionsRequest.


        :param secret_name: The secret_name of this DescribeSecretVersionsRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and secret_name is None:
            raise ValueError("Invalid value for `secret_name`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                secret_name is not None and len(secret_name) > 31):
            raise ValueError("Invalid value for `secret_name`, length must be less than or equal to `31`")  # noqa: E501
        if (self._configuration.client_side_validation and
                secret_name is not None and len(secret_name) < 2):
            raise ValueError("Invalid value for `secret_name`, length must be greater than or equal to `2`")  # noqa: E501

        self._secret_name = secret_name

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
        if issubclass(DescribeSecretVersionsRequest, dict):
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
        if not isinstance(other, DescribeSecretVersionsRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeSecretVersionsRequest):
            return True

        return self.to_dict() != other.to_dict()
