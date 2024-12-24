# coding: utf-8

"""
    cv20240606

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class AlgorithmBaseRespForHairStyleOutput(object):
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
        'status_code': 'int',
        'status_message': 'str'
    }

    attribute_map = {
        'status_code': 'status_code',
        'status_message': 'status_message'
    }

    def __init__(self, status_code=None, status_message=None, _configuration=None):  # noqa: E501
        """AlgorithmBaseRespForHairStyleOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._status_code = None
        self._status_message = None
        self.discriminator = None

        if status_code is not None:
            self.status_code = status_code
        if status_message is not None:
            self.status_message = status_message

    @property
    def status_code(self):
        """Gets the status_code of this AlgorithmBaseRespForHairStyleOutput.  # noqa: E501


        :return: The status_code of this AlgorithmBaseRespForHairStyleOutput.  # noqa: E501
        :rtype: int
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """Sets the status_code of this AlgorithmBaseRespForHairStyleOutput.


        :param status_code: The status_code of this AlgorithmBaseRespForHairStyleOutput.  # noqa: E501
        :type: int
        """

        self._status_code = status_code

    @property
    def status_message(self):
        """Gets the status_message of this AlgorithmBaseRespForHairStyleOutput.  # noqa: E501


        :return: The status_message of this AlgorithmBaseRespForHairStyleOutput.  # noqa: E501
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """Sets the status_message of this AlgorithmBaseRespForHairStyleOutput.


        :param status_message: The status_message of this AlgorithmBaseRespForHairStyleOutput.  # noqa: E501
        :type: str
        """

        self._status_message = status_message

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
        if issubclass(AlgorithmBaseRespForHairStyleOutput, dict):
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
        if not isinstance(other, AlgorithmBaseRespForHairStyleOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AlgorithmBaseRespForHairStyleOutput):
            return True

        return self.to_dict() != other.to_dict()
