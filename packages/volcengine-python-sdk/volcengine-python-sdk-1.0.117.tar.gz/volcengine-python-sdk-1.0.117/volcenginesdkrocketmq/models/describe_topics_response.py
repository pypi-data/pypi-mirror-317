# coding: utf-8

"""
    rocketmq

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeTopicsResponse(object):
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
        'instance_id': 'str',
        'topics_info': 'list[TopicsInfoForDescribeTopicsOutput]',
        'total': 'int'
    }

    attribute_map = {
        'instance_id': 'InstanceId',
        'topics_info': 'TopicsInfo',
        'total': 'Total'
    }

    def __init__(self, instance_id=None, topics_info=None, total=None, _configuration=None):  # noqa: E501
        """DescribeTopicsResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._instance_id = None
        self._topics_info = None
        self._total = None
        self.discriminator = None

        if instance_id is not None:
            self.instance_id = instance_id
        if topics_info is not None:
            self.topics_info = topics_info
        if total is not None:
            self.total = total

    @property
    def instance_id(self):
        """Gets the instance_id of this DescribeTopicsResponse.  # noqa: E501


        :return: The instance_id of this DescribeTopicsResponse.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this DescribeTopicsResponse.


        :param instance_id: The instance_id of this DescribeTopicsResponse.  # noqa: E501
        :type: str
        """

        self._instance_id = instance_id

    @property
    def topics_info(self):
        """Gets the topics_info of this DescribeTopicsResponse.  # noqa: E501


        :return: The topics_info of this DescribeTopicsResponse.  # noqa: E501
        :rtype: list[TopicsInfoForDescribeTopicsOutput]
        """
        return self._topics_info

    @topics_info.setter
    def topics_info(self, topics_info):
        """Sets the topics_info of this DescribeTopicsResponse.


        :param topics_info: The topics_info of this DescribeTopicsResponse.  # noqa: E501
        :type: list[TopicsInfoForDescribeTopicsOutput]
        """

        self._topics_info = topics_info

    @property
    def total(self):
        """Gets the total of this DescribeTopicsResponse.  # noqa: E501


        :return: The total of this DescribeTopicsResponse.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this DescribeTopicsResponse.


        :param total: The total of this DescribeTopicsResponse.  # noqa: E501
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
        if issubclass(DescribeTopicsResponse, dict):
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
        if not isinstance(other, DescribeTopicsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeTopicsResponse):
            return True

        return self.to_dict() != other.to_dict()
