# coding: utf-8

"""
    rds_mysql_v2

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class TemplateParamForCreateParameterTemplateInput(object):
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
        'default_value': 'str',
        'description': 'str',
        'expect_value': 'str',
        'expression': 'str',
        'name': 'str',
        'restart': 'bool',
        'running_value': 'str',
        'value_range': 'str'
    }

    attribute_map = {
        'default_value': 'DefaultValue',
        'description': 'Description',
        'expect_value': 'ExpectValue',
        'expression': 'Expression',
        'name': 'Name',
        'restart': 'Restart',
        'running_value': 'RunningValue',
        'value_range': 'ValueRange'
    }

    def __init__(self, default_value=None, description=None, expect_value=None, expression=None, name=None, restart=None, running_value=None, value_range=None, _configuration=None):  # noqa: E501
        """TemplateParamForCreateParameterTemplateInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._default_value = None
        self._description = None
        self._expect_value = None
        self._expression = None
        self._name = None
        self._restart = None
        self._running_value = None
        self._value_range = None
        self.discriminator = None

        if default_value is not None:
            self.default_value = default_value
        if description is not None:
            self.description = description
        if expect_value is not None:
            self.expect_value = expect_value
        if expression is not None:
            self.expression = expression
        if name is not None:
            self.name = name
        if restart is not None:
            self.restart = restart
        if running_value is not None:
            self.running_value = running_value
        if value_range is not None:
            self.value_range = value_range

    @property
    def default_value(self):
        """Gets the default_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The default_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: str
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """Sets the default_value of this TemplateParamForCreateParameterTemplateInput.


        :param default_value: The default_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: str
        """

        self._default_value = default_value

    @property
    def description(self):
        """Gets the description of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The description of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TemplateParamForCreateParameterTemplateInput.


        :param description: The description of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def expect_value(self):
        """Gets the expect_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The expect_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: str
        """
        return self._expect_value

    @expect_value.setter
    def expect_value(self, expect_value):
        """Sets the expect_value of this TemplateParamForCreateParameterTemplateInput.


        :param expect_value: The expect_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: str
        """

        self._expect_value = expect_value

    @property
    def expression(self):
        """Gets the expression of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The expression of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: str
        """
        return self._expression

    @expression.setter
    def expression(self, expression):
        """Sets the expression of this TemplateParamForCreateParameterTemplateInput.


        :param expression: The expression of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: str
        """

        self._expression = expression

    @property
    def name(self):
        """Gets the name of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The name of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TemplateParamForCreateParameterTemplateInput.


        :param name: The name of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def restart(self):
        """Gets the restart of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The restart of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: bool
        """
        return self._restart

    @restart.setter
    def restart(self, restart):
        """Sets the restart of this TemplateParamForCreateParameterTemplateInput.


        :param restart: The restart of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: bool
        """

        self._restart = restart

    @property
    def running_value(self):
        """Gets the running_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The running_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: str
        """
        return self._running_value

    @running_value.setter
    def running_value(self, running_value):
        """Sets the running_value of this TemplateParamForCreateParameterTemplateInput.


        :param running_value: The running_value of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: str
        """

        self._running_value = running_value

    @property
    def value_range(self):
        """Gets the value_range of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501


        :return: The value_range of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :rtype: str
        """
        return self._value_range

    @value_range.setter
    def value_range(self, value_range):
        """Sets the value_range of this TemplateParamForCreateParameterTemplateInput.


        :param value_range: The value_range of this TemplateParamForCreateParameterTemplateInput.  # noqa: E501
        :type: str
        """

        self._value_range = value_range

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
        if issubclass(TemplateParamForCreateParameterTemplateInput, dict):
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
        if not isinstance(other, TemplateParamForCreateParameterTemplateInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TemplateParamForCreateParameterTemplateInput):
            return True

        return self.to_dict() != other.to_dict()
