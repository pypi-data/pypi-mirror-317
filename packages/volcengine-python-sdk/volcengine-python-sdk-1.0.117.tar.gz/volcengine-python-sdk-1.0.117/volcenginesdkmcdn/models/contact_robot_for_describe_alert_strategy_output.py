# coding: utf-8

"""
    mcdn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ContactRobotForDescribeAlertStrategyOutput(object):
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
        'id': 'str',
        'name': 'str',
        'robot_type': 'str'
    }

    attribute_map = {
        'id': 'Id',
        'name': 'Name',
        'robot_type': 'RobotType'
    }

    def __init__(self, id=None, name=None, robot_type=None, _configuration=None):  # noqa: E501
        """ContactRobotForDescribeAlertStrategyOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._name = None
        self._robot_type = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if robot_type is not None:
            self.robot_type = robot_type

    @property
    def id(self):
        """Gets the id of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501


        :return: The id of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ContactRobotForDescribeAlertStrategyOutput.


        :param id: The id of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501


        :return: The name of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ContactRobotForDescribeAlertStrategyOutput.


        :param name: The name of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def robot_type(self):
        """Gets the robot_type of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501


        :return: The robot_type of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501
        :rtype: str
        """
        return self._robot_type

    @robot_type.setter
    def robot_type(self, robot_type):
        """Sets the robot_type of this ContactRobotForDescribeAlertStrategyOutput.


        :param robot_type: The robot_type of this ContactRobotForDescribeAlertStrategyOutput.  # noqa: E501
        :type: str
        """

        self._robot_type = robot_type

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
        if issubclass(ContactRobotForDescribeAlertStrategyOutput, dict):
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
        if not isinstance(other, ContactRobotForDescribeAlertStrategyOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ContactRobotForDescribeAlertStrategyOutput):
            return True

        return self.to_dict() != other.to_dict()
