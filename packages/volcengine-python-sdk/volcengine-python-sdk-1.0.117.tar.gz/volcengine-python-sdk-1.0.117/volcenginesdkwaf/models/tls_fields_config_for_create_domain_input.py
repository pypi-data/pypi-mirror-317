# coding: utf-8

"""
    waf

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class TLSFieldsConfigForCreateDomainInput(object):
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
        'headers_config': 'HeadersConfigForCreateDomainInput'
    }

    attribute_map = {
        'headers_config': 'HeadersConfig'
    }

    def __init__(self, headers_config=None, _configuration=None):  # noqa: E501
        """TLSFieldsConfigForCreateDomainInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._headers_config = None
        self.discriminator = None

        if headers_config is not None:
            self.headers_config = headers_config

    @property
    def headers_config(self):
        """Gets the headers_config of this TLSFieldsConfigForCreateDomainInput.  # noqa: E501


        :return: The headers_config of this TLSFieldsConfigForCreateDomainInput.  # noqa: E501
        :rtype: HeadersConfigForCreateDomainInput
        """
        return self._headers_config

    @headers_config.setter
    def headers_config(self, headers_config):
        """Sets the headers_config of this TLSFieldsConfigForCreateDomainInput.


        :param headers_config: The headers_config of this TLSFieldsConfigForCreateDomainInput.  # noqa: E501
        :type: HeadersConfigForCreateDomainInput
        """

        self._headers_config = headers_config

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
        if issubclass(TLSFieldsConfigForCreateDomainInput, dict):
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
        if not isinstance(other, TLSFieldsConfigForCreateDomainInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TLSFieldsConfigForCreateDomainInput):
            return True

        return self.to_dict() != other.to_dict()
