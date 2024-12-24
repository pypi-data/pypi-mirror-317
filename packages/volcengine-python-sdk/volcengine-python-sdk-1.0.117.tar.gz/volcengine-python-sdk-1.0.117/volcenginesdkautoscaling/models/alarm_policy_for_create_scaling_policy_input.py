# coding: utf-8

"""
    auto_scaling

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class AlarmPolicyForCreateScalingPolicyInput(object):
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
        'condition': 'AlarmPolicyConditionForCreateScalingPolicyInput',
        'evaluation_count': 'int',
        'rule_type': 'str'
    }

    attribute_map = {
        'condition': 'Condition',
        'evaluation_count': 'EvaluationCount',
        'rule_type': 'RuleType'
    }

    def __init__(self, condition=None, evaluation_count=None, rule_type=None, _configuration=None):  # noqa: E501
        """AlarmPolicyForCreateScalingPolicyInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._condition = None
        self._evaluation_count = None
        self._rule_type = None
        self.discriminator = None

        if condition is not None:
            self.condition = condition
        if evaluation_count is not None:
            self.evaluation_count = evaluation_count
        if rule_type is not None:
            self.rule_type = rule_type

    @property
    def condition(self):
        """Gets the condition of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501


        :return: The condition of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501
        :rtype: AlarmPolicyConditionForCreateScalingPolicyInput
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this AlarmPolicyForCreateScalingPolicyInput.


        :param condition: The condition of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501
        :type: AlarmPolicyConditionForCreateScalingPolicyInput
        """

        self._condition = condition

    @property
    def evaluation_count(self):
        """Gets the evaluation_count of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501


        :return: The evaluation_count of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501
        :rtype: int
        """
        return self._evaluation_count

    @evaluation_count.setter
    def evaluation_count(self, evaluation_count):
        """Sets the evaluation_count of this AlarmPolicyForCreateScalingPolicyInput.


        :param evaluation_count: The evaluation_count of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501
        :type: int
        """
        if (self._configuration.client_side_validation and
                evaluation_count is not None and evaluation_count > 180):  # noqa: E501
            raise ValueError("Invalid value for `evaluation_count`, must be a value less than or equal to `180`")  # noqa: E501
        if (self._configuration.client_side_validation and
                evaluation_count is not None and evaluation_count < 1):  # noqa: E501
            raise ValueError("Invalid value for `evaluation_count`, must be a value greater than or equal to `1`")  # noqa: E501

        self._evaluation_count = evaluation_count

    @property
    def rule_type(self):
        """Gets the rule_type of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501


        :return: The rule_type of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501
        :rtype: str
        """
        return self._rule_type

    @rule_type.setter
    def rule_type(self, rule_type):
        """Sets the rule_type of this AlarmPolicyForCreateScalingPolicyInput.


        :param rule_type: The rule_type of this AlarmPolicyForCreateScalingPolicyInput.  # noqa: E501
        :type: str
        """

        self._rule_type = rule_type

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
        if issubclass(AlarmPolicyForCreateScalingPolicyInput, dict):
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
        if not isinstance(other, AlarmPolicyForCreateScalingPolicyInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AlarmPolicyForCreateScalingPolicyInput):
            return True

        return self.to_dict() != other.to_dict()
