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


class DescribeConsumedClientsResponse(object):
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
        'connection_count': 'int',
        'consumed_clients_info': 'list[ConsumedClientsInfoForDescribeConsumedClientsOutput]'
    }

    attribute_map = {
        'connection_count': 'ConnectionCount',
        'consumed_clients_info': 'ConsumedClientsInfo'
    }

    def __init__(self, connection_count=None, consumed_clients_info=None, _configuration=None):  # noqa: E501
        """DescribeConsumedClientsResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._connection_count = None
        self._consumed_clients_info = None
        self.discriminator = None

        if connection_count is not None:
            self.connection_count = connection_count
        if consumed_clients_info is not None:
            self.consumed_clients_info = consumed_clients_info

    @property
    def connection_count(self):
        """Gets the connection_count of this DescribeConsumedClientsResponse.  # noqa: E501


        :return: The connection_count of this DescribeConsumedClientsResponse.  # noqa: E501
        :rtype: int
        """
        return self._connection_count

    @connection_count.setter
    def connection_count(self, connection_count):
        """Sets the connection_count of this DescribeConsumedClientsResponse.


        :param connection_count: The connection_count of this DescribeConsumedClientsResponse.  # noqa: E501
        :type: int
        """

        self._connection_count = connection_count

    @property
    def consumed_clients_info(self):
        """Gets the consumed_clients_info of this DescribeConsumedClientsResponse.  # noqa: E501


        :return: The consumed_clients_info of this DescribeConsumedClientsResponse.  # noqa: E501
        :rtype: list[ConsumedClientsInfoForDescribeConsumedClientsOutput]
        """
        return self._consumed_clients_info

    @consumed_clients_info.setter
    def consumed_clients_info(self, consumed_clients_info):
        """Sets the consumed_clients_info of this DescribeConsumedClientsResponse.


        :param consumed_clients_info: The consumed_clients_info of this DescribeConsumedClientsResponse.  # noqa: E501
        :type: list[ConsumedClientsInfoForDescribeConsumedClientsOutput]
        """

        self._consumed_clients_info = consumed_clients_info

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
        if issubclass(DescribeConsumedClientsResponse, dict):
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
        if not isinstance(other, DescribeConsumedClientsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeConsumedClientsResponse):
            return True

        return self.to_dict() != other.to_dict()
