# coding: utf-8

"""
    escloud

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ColdNodeStorageSpecForDescribeInstancesOutput(object):
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
        'description': 'str',
        'display_name': 'str',
        'max_size': 'int',
        'min_size': 'int',
        'name': 'str',
        'size': 'int'
    }

    attribute_map = {
        'description': 'Description',
        'display_name': 'DisplayName',
        'max_size': 'MaxSize',
        'min_size': 'MinSize',
        'name': 'Name',
        'size': 'Size'
    }

    def __init__(self, description=None, display_name=None, max_size=None, min_size=None, name=None, size=None, _configuration=None):  # noqa: E501
        """ColdNodeStorageSpecForDescribeInstancesOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._description = None
        self._display_name = None
        self._max_size = None
        self._min_size = None
        self._name = None
        self._size = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if display_name is not None:
            self.display_name = display_name
        if max_size is not None:
            self.max_size = max_size
        if min_size is not None:
            self.min_size = min_size
        if name is not None:
            self.name = name
        if size is not None:
            self.size = size

    @property
    def description(self):
        """Gets the description of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501


        :return: The description of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ColdNodeStorageSpecForDescribeInstancesOutput.


        :param description: The description of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501


        :return: The display_name of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ColdNodeStorageSpecForDescribeInstancesOutput.


        :param display_name: The display_name of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def max_size(self):
        """Gets the max_size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501


        :return: The max_size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :rtype: int
        """
        return self._max_size

    @max_size.setter
    def max_size(self, max_size):
        """Sets the max_size of this ColdNodeStorageSpecForDescribeInstancesOutput.


        :param max_size: The max_size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :type: int
        """

        self._max_size = max_size

    @property
    def min_size(self):
        """Gets the min_size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501


        :return: The min_size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :rtype: int
        """
        return self._min_size

    @min_size.setter
    def min_size(self, min_size):
        """Sets the min_size of this ColdNodeStorageSpecForDescribeInstancesOutput.


        :param min_size: The min_size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :type: int
        """

        self._min_size = min_size

    @property
    def name(self):
        """Gets the name of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501


        :return: The name of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ColdNodeStorageSpecForDescribeInstancesOutput.


        :param name: The name of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def size(self):
        """Gets the size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501


        :return: The size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this ColdNodeStorageSpecForDescribeInstancesOutput.


        :param size: The size of this ColdNodeStorageSpecForDescribeInstancesOutput.  # noqa: E501
        :type: int
        """

        self._size = size

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
        if issubclass(ColdNodeStorageSpecForDescribeInstancesOutput, dict):
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
        if not isinstance(other, ColdNodeStorageSpecForDescribeInstancesOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ColdNodeStorageSpecForDescribeInstancesOutput):
            return True

        return self.to_dict() != other.to_dict()
