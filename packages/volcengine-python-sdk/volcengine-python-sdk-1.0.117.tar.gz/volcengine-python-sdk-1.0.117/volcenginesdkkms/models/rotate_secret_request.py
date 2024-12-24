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


class RotateSecretRequest(object):
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
        'secret_name': 'str'
    }

    attribute_map = {
        'secret_name': 'SecretName'
    }

    def __init__(self, secret_name=None, _configuration=None):  # noqa: E501
        """RotateSecretRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._secret_name = None
        self.discriminator = None

        self.secret_name = secret_name

    @property
    def secret_name(self):
        """Gets the secret_name of this RotateSecretRequest.  # noqa: E501


        :return: The secret_name of this RotateSecretRequest.  # noqa: E501
        :rtype: str
        """
        return self._secret_name

    @secret_name.setter
    def secret_name(self, secret_name):
        """Sets the secret_name of this RotateSecretRequest.


        :param secret_name: The secret_name of this RotateSecretRequest.  # noqa: E501
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
        if issubclass(RotateSecretRequest, dict):
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
        if not isinstance(other, RotateSecretRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RotateSecretRequest):
            return True

        return self.to_dict() != other.to_dict()
