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


class CustomizeRuleForDescribeCdnConfigOutput(object):
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
        'access_action': 'AccessActionForDescribeCdnConfigOutput',
        'condition': 'ConditionForDescribeCdnConfigOutput'
    }

    attribute_map = {
        'access_action': 'AccessAction',
        'condition': 'Condition'
    }

    def __init__(self, access_action=None, condition=None, _configuration=None):  # noqa: E501
        """CustomizeRuleForDescribeCdnConfigOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._access_action = None
        self._condition = None
        self.discriminator = None

        if access_action is not None:
            self.access_action = access_action
        if condition is not None:
            self.condition = condition

    @property
    def access_action(self):
        """Gets the access_action of this CustomizeRuleForDescribeCdnConfigOutput.  # noqa: E501


        :return: The access_action of this CustomizeRuleForDescribeCdnConfigOutput.  # noqa: E501
        :rtype: AccessActionForDescribeCdnConfigOutput
        """
        return self._access_action

    @access_action.setter
    def access_action(self, access_action):
        """Sets the access_action of this CustomizeRuleForDescribeCdnConfigOutput.


        :param access_action: The access_action of this CustomizeRuleForDescribeCdnConfigOutput.  # noqa: E501
        :type: AccessActionForDescribeCdnConfigOutput
        """

        self._access_action = access_action

    @property
    def condition(self):
        """Gets the condition of this CustomizeRuleForDescribeCdnConfigOutput.  # noqa: E501


        :return: The condition of this CustomizeRuleForDescribeCdnConfigOutput.  # noqa: E501
        :rtype: ConditionForDescribeCdnConfigOutput
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this CustomizeRuleForDescribeCdnConfigOutput.


        :param condition: The condition of this CustomizeRuleForDescribeCdnConfigOutput.  # noqa: E501
        :type: ConditionForDescribeCdnConfigOutput
        """

        self._condition = condition

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
        if issubclass(CustomizeRuleForDescribeCdnConfigOutput, dict):
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
        if not isinstance(other, CustomizeRuleForDescribeCdnConfigOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustomizeRuleForDescribeCdnConfigOutput):
            return True

        return self.to_dict() != other.to_dict()
