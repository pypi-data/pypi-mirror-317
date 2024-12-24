# coding: utf-8

"""
    mongodb

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class InstanceParameterForDescribeDBInstanceParametersOutput(object):
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
        'checking_code': 'str',
        'force_modify': 'bool',
        'force_restart': 'bool',
        'parameter_default_value': 'str',
        'parameter_description': 'str',
        'parameter_names': 'str',
        'parameter_role': 'str',
        'parameter_type': 'str',
        'parameter_value': 'str'
    }

    attribute_map = {
        'checking_code': 'CheckingCode',
        'force_modify': 'ForceModify',
        'force_restart': 'ForceRestart',
        'parameter_default_value': 'ParameterDefaultValue',
        'parameter_description': 'ParameterDescription',
        'parameter_names': 'ParameterNames',
        'parameter_role': 'ParameterRole',
        'parameter_type': 'ParameterType',
        'parameter_value': 'ParameterValue'
    }

    def __init__(self, checking_code=None, force_modify=None, force_restart=None, parameter_default_value=None, parameter_description=None, parameter_names=None, parameter_role=None, parameter_type=None, parameter_value=None, _configuration=None):  # noqa: E501
        """InstanceParameterForDescribeDBInstanceParametersOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._checking_code = None
        self._force_modify = None
        self._force_restart = None
        self._parameter_default_value = None
        self._parameter_description = None
        self._parameter_names = None
        self._parameter_role = None
        self._parameter_type = None
        self._parameter_value = None
        self.discriminator = None

        if checking_code is not None:
            self.checking_code = checking_code
        if force_modify is not None:
            self.force_modify = force_modify
        if force_restart is not None:
            self.force_restart = force_restart
        if parameter_default_value is not None:
            self.parameter_default_value = parameter_default_value
        if parameter_description is not None:
            self.parameter_description = parameter_description
        if parameter_names is not None:
            self.parameter_names = parameter_names
        if parameter_role is not None:
            self.parameter_role = parameter_role
        if parameter_type is not None:
            self.parameter_type = parameter_type
        if parameter_value is not None:
            self.parameter_value = parameter_value

    @property
    def checking_code(self):
        """Gets the checking_code of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The checking_code of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: str
        """
        return self._checking_code

    @checking_code.setter
    def checking_code(self, checking_code):
        """Sets the checking_code of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param checking_code: The checking_code of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: str
        """

        self._checking_code = checking_code

    @property
    def force_modify(self):
        """Gets the force_modify of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The force_modify of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: bool
        """
        return self._force_modify

    @force_modify.setter
    def force_modify(self, force_modify):
        """Sets the force_modify of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param force_modify: The force_modify of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: bool
        """

        self._force_modify = force_modify

    @property
    def force_restart(self):
        """Gets the force_restart of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The force_restart of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: bool
        """
        return self._force_restart

    @force_restart.setter
    def force_restart(self, force_restart):
        """Sets the force_restart of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param force_restart: The force_restart of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: bool
        """

        self._force_restart = force_restart

    @property
    def parameter_default_value(self):
        """Gets the parameter_default_value of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The parameter_default_value of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: str
        """
        return self._parameter_default_value

    @parameter_default_value.setter
    def parameter_default_value(self, parameter_default_value):
        """Sets the parameter_default_value of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param parameter_default_value: The parameter_default_value of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: str
        """

        self._parameter_default_value = parameter_default_value

    @property
    def parameter_description(self):
        """Gets the parameter_description of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The parameter_description of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: str
        """
        return self._parameter_description

    @parameter_description.setter
    def parameter_description(self, parameter_description):
        """Sets the parameter_description of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param parameter_description: The parameter_description of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: str
        """

        self._parameter_description = parameter_description

    @property
    def parameter_names(self):
        """Gets the parameter_names of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The parameter_names of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: str
        """
        return self._parameter_names

    @parameter_names.setter
    def parameter_names(self, parameter_names):
        """Sets the parameter_names of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param parameter_names: The parameter_names of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: str
        """

        self._parameter_names = parameter_names

    @property
    def parameter_role(self):
        """Gets the parameter_role of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The parameter_role of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: str
        """
        return self._parameter_role

    @parameter_role.setter
    def parameter_role(self, parameter_role):
        """Sets the parameter_role of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param parameter_role: The parameter_role of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: str
        """

        self._parameter_role = parameter_role

    @property
    def parameter_type(self):
        """Gets the parameter_type of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The parameter_type of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: str
        """
        return self._parameter_type

    @parameter_type.setter
    def parameter_type(self, parameter_type):
        """Sets the parameter_type of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param parameter_type: The parameter_type of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: str
        """

        self._parameter_type = parameter_type

    @property
    def parameter_value(self):
        """Gets the parameter_value of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501


        :return: The parameter_value of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :rtype: str
        """
        return self._parameter_value

    @parameter_value.setter
    def parameter_value(self, parameter_value):
        """Sets the parameter_value of this InstanceParameterForDescribeDBInstanceParametersOutput.


        :param parameter_value: The parameter_value of this InstanceParameterForDescribeDBInstanceParametersOutput.  # noqa: E501
        :type: str
        """

        self._parameter_value = parameter_value

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
        if issubclass(InstanceParameterForDescribeDBInstanceParametersOutput, dict):
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
        if not isinstance(other, InstanceParameterForDescribeDBInstanceParametersOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InstanceParameterForDescribeDBInstanceParametersOutput):
            return True

        return self.to_dict() != other.to_dict()
