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


class NotifyConfigForDescribeAlertStrategyOutput(object):
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
        'ignore_disabled_domains': 'bool',
        'level': 'str',
        'send_type': 'list[str]'
    }

    attribute_map = {
        'ignore_disabled_domains': 'IgnoreDisabledDomains',
        'level': 'Level',
        'send_type': 'SendType'
    }

    def __init__(self, ignore_disabled_domains=None, level=None, send_type=None, _configuration=None):  # noqa: E501
        """NotifyConfigForDescribeAlertStrategyOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._ignore_disabled_domains = None
        self._level = None
        self._send_type = None
        self.discriminator = None

        if ignore_disabled_domains is not None:
            self.ignore_disabled_domains = ignore_disabled_domains
        if level is not None:
            self.level = level
        if send_type is not None:
            self.send_type = send_type

    @property
    def ignore_disabled_domains(self):
        """Gets the ignore_disabled_domains of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501


        :return: The ignore_disabled_domains of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_disabled_domains

    @ignore_disabled_domains.setter
    def ignore_disabled_domains(self, ignore_disabled_domains):
        """Sets the ignore_disabled_domains of this NotifyConfigForDescribeAlertStrategyOutput.


        :param ignore_disabled_domains: The ignore_disabled_domains of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501
        :type: bool
        """

        self._ignore_disabled_domains = ignore_disabled_domains

    @property
    def level(self):
        """Gets the level of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501


        :return: The level of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501
        :rtype: str
        """
        return self._level

    @level.setter
    def level(self, level):
        """Sets the level of this NotifyConfigForDescribeAlertStrategyOutput.


        :param level: The level of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501
        :type: str
        """

        self._level = level

    @property
    def send_type(self):
        """Gets the send_type of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501


        :return: The send_type of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._send_type

    @send_type.setter
    def send_type(self, send_type):
        """Sets the send_type of this NotifyConfigForDescribeAlertStrategyOutput.


        :param send_type: The send_type of this NotifyConfigForDescribeAlertStrategyOutput.  # noqa: E501
        :type: list[str]
        """

        self._send_type = send_type

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
        if issubclass(NotifyConfigForDescribeAlertStrategyOutput, dict):
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
        if not isinstance(other, NotifyConfigForDescribeAlertStrategyOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NotifyConfigForDescribeAlertStrategyOutput):
            return True

        return self.to_dict() != other.to_dict()
