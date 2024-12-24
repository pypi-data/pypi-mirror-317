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


class CommonMatchListForDescribeSharedConfigOutput(object):
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
        'common_type': 'CommonTypeForDescribeSharedConfigOutput'
    }

    attribute_map = {
        'common_type': 'CommonType'
    }

    def __init__(self, common_type=None, _configuration=None):  # noqa: E501
        """CommonMatchListForDescribeSharedConfigOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._common_type = None
        self.discriminator = None

        if common_type is not None:
            self.common_type = common_type

    @property
    def common_type(self):
        """Gets the common_type of this CommonMatchListForDescribeSharedConfigOutput.  # noqa: E501


        :return: The common_type of this CommonMatchListForDescribeSharedConfigOutput.  # noqa: E501
        :rtype: CommonTypeForDescribeSharedConfigOutput
        """
        return self._common_type

    @common_type.setter
    def common_type(self, common_type):
        """Sets the common_type of this CommonMatchListForDescribeSharedConfigOutput.


        :param common_type: The common_type of this CommonMatchListForDescribeSharedConfigOutput.  # noqa: E501
        :type: CommonTypeForDescribeSharedConfigOutput
        """

        self._common_type = common_type

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
        if issubclass(CommonMatchListForDescribeSharedConfigOutput, dict):
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
        if not isinstance(other, CommonMatchListForDescribeSharedConfigOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CommonMatchListForDescribeSharedConfigOutput):
            return True

        return self.to_dict() != other.to_dict()
