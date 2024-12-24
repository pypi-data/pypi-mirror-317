# coding: utf-8

"""
    kafka

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeConsumedTopicsResponse(object):
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
        'accumulation': 'int',
        'consumed_topics_info': 'list[ConsumedTopicsInfoForDescribeConsumedTopicsOutput]',
        'total': 'int'
    }

    attribute_map = {
        'accumulation': 'Accumulation',
        'consumed_topics_info': 'ConsumedTopicsInfo',
        'total': 'Total'
    }

    def __init__(self, accumulation=None, consumed_topics_info=None, total=None, _configuration=None):  # noqa: E501
        """DescribeConsumedTopicsResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._accumulation = None
        self._consumed_topics_info = None
        self._total = None
        self.discriminator = None

        if accumulation is not None:
            self.accumulation = accumulation
        if consumed_topics_info is not None:
            self.consumed_topics_info = consumed_topics_info
        if total is not None:
            self.total = total

    @property
    def accumulation(self):
        """Gets the accumulation of this DescribeConsumedTopicsResponse.  # noqa: E501


        :return: The accumulation of this DescribeConsumedTopicsResponse.  # noqa: E501
        :rtype: int
        """
        return self._accumulation

    @accumulation.setter
    def accumulation(self, accumulation):
        """Sets the accumulation of this DescribeConsumedTopicsResponse.


        :param accumulation: The accumulation of this DescribeConsumedTopicsResponse.  # noqa: E501
        :type: int
        """

        self._accumulation = accumulation

    @property
    def consumed_topics_info(self):
        """Gets the consumed_topics_info of this DescribeConsumedTopicsResponse.  # noqa: E501


        :return: The consumed_topics_info of this DescribeConsumedTopicsResponse.  # noqa: E501
        :rtype: list[ConsumedTopicsInfoForDescribeConsumedTopicsOutput]
        """
        return self._consumed_topics_info

    @consumed_topics_info.setter
    def consumed_topics_info(self, consumed_topics_info):
        """Sets the consumed_topics_info of this DescribeConsumedTopicsResponse.


        :param consumed_topics_info: The consumed_topics_info of this DescribeConsumedTopicsResponse.  # noqa: E501
        :type: list[ConsumedTopicsInfoForDescribeConsumedTopicsOutput]
        """

        self._consumed_topics_info = consumed_topics_info

    @property
    def total(self):
        """Gets the total of this DescribeConsumedTopicsResponse.  # noqa: E501


        :return: The total of this DescribeConsumedTopicsResponse.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this DescribeConsumedTopicsResponse.


        :param total: The total of this DescribeConsumedTopicsResponse.  # noqa: E501
        :type: int
        """

        self._total = total

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
        if issubclass(DescribeConsumedTopicsResponse, dict):
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
        if not isinstance(other, DescribeConsumedTopicsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeConsumedTopicsResponse):
            return True

        return self.to_dict() != other.to_dict()
