# coding: utf-8

"""
    cdn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DeleteSharedConfigRequest(object):
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
        'config_name': 'str'
    }

    attribute_map = {
        'config_name': 'ConfigName'
    }

    def __init__(self, config_name=None, _configuration=None):  # noqa: E501
        """DeleteSharedConfigRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._config_name = None
        self.discriminator = None

        self.config_name = config_name

    @property
    def config_name(self):
        """Gets the config_name of this DeleteSharedConfigRequest.  # noqa: E501


        :return: The config_name of this DeleteSharedConfigRequest.  # noqa: E501
        :rtype: str
        """
        return self._config_name

    @config_name.setter
    def config_name(self, config_name):
        """Sets the config_name of this DeleteSharedConfigRequest.


        :param config_name: The config_name of this DeleteSharedConfigRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and config_name is None:
            raise ValueError("Invalid value for `config_name`, must not be `None`")  # noqa: E501

        self._config_name = config_name

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
        if issubclass(DeleteSharedConfigRequest, dict):
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
        if not isinstance(other, DeleteSharedConfigRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeleteSharedConfigRequest):
            return True

        return self.to_dict() != other.to_dict()
