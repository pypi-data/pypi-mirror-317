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


class MasterNodeResourceSpecForDescribeInstanceOutput(object):
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
        'cpu': 'int',
        'description': 'str',
        'display_name': 'str',
        'memory': 'int',
        'name': 'str'
    }

    attribute_map = {
        'cpu': 'CPU',
        'description': 'Description',
        'display_name': 'DisplayName',
        'memory': 'Memory',
        'name': 'Name'
    }

    def __init__(self, cpu=None, description=None, display_name=None, memory=None, name=None, _configuration=None):  # noqa: E501
        """MasterNodeResourceSpecForDescribeInstanceOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cpu = None
        self._description = None
        self._display_name = None
        self._memory = None
        self._name = None
        self.discriminator = None

        if cpu is not None:
            self.cpu = cpu
        if description is not None:
            self.description = description
        if display_name is not None:
            self.display_name = display_name
        if memory is not None:
            self.memory = memory
        if name is not None:
            self.name = name

    @property
    def cpu(self):
        """Gets the cpu of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501


        :return: The cpu of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :rtype: int
        """
        return self._cpu

    @cpu.setter
    def cpu(self, cpu):
        """Sets the cpu of this MasterNodeResourceSpecForDescribeInstanceOutput.


        :param cpu: The cpu of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :type: int
        """

        self._cpu = cpu

    @property
    def description(self):
        """Gets the description of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501


        :return: The description of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this MasterNodeResourceSpecForDescribeInstanceOutput.


        :param description: The description of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501


        :return: The display_name of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this MasterNodeResourceSpecForDescribeInstanceOutput.


        :param display_name: The display_name of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def memory(self):
        """Gets the memory of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501


        :return: The memory of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :rtype: int
        """
        return self._memory

    @memory.setter
    def memory(self, memory):
        """Sets the memory of this MasterNodeResourceSpecForDescribeInstanceOutput.


        :param memory: The memory of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :type: int
        """

        self._memory = memory

    @property
    def name(self):
        """Gets the name of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501


        :return: The name of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MasterNodeResourceSpecForDescribeInstanceOutput.


        :param name: The name of this MasterNodeResourceSpecForDescribeInstanceOutput.  # noqa: E501
        :type: str
        """

        self._name = name

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
        if issubclass(MasterNodeResourceSpecForDescribeInstanceOutput, dict):
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
        if not isinstance(other, MasterNodeResourceSpecForDescribeInstanceOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MasterNodeResourceSpecForDescribeInstanceOutput):
            return True

        return self.to_dict() != other.to_dict()
