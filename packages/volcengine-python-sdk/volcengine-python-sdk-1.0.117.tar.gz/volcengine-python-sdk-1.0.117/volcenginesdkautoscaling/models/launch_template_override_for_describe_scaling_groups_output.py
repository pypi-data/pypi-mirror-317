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


class LaunchTemplateOverrideForDescribeScalingGroupsOutput(object):
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
        'instance_type': 'str',
        'price_limit': 'float',
        'weighted_capacity': 'int'
    }

    attribute_map = {
        'instance_type': 'InstanceType',
        'price_limit': 'PriceLimit',
        'weighted_capacity': 'WeightedCapacity'
    }

    def __init__(self, instance_type=None, price_limit=None, weighted_capacity=None, _configuration=None):  # noqa: E501
        """LaunchTemplateOverrideForDescribeScalingGroupsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._instance_type = None
        self._price_limit = None
        self._weighted_capacity = None
        self.discriminator = None

        if instance_type is not None:
            self.instance_type = instance_type
        if price_limit is not None:
            self.price_limit = price_limit
        if weighted_capacity is not None:
            self.weighted_capacity = weighted_capacity

    @property
    def instance_type(self):
        """Gets the instance_type of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501


        :return: The instance_type of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """Sets the instance_type of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.


        :param instance_type: The instance_type of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501
        :type: str
        """

        self._instance_type = instance_type

    @property
    def price_limit(self):
        """Gets the price_limit of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501


        :return: The price_limit of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501
        :rtype: float
        """
        return self._price_limit

    @price_limit.setter
    def price_limit(self, price_limit):
        """Sets the price_limit of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.


        :param price_limit: The price_limit of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501
        :type: float
        """

        self._price_limit = price_limit

    @property
    def weighted_capacity(self):
        """Gets the weighted_capacity of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501


        :return: The weighted_capacity of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501
        :rtype: int
        """
        return self._weighted_capacity

    @weighted_capacity.setter
    def weighted_capacity(self, weighted_capacity):
        """Sets the weighted_capacity of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.


        :param weighted_capacity: The weighted_capacity of this LaunchTemplateOverrideForDescribeScalingGroupsOutput.  # noqa: E501
        :type: int
        """

        self._weighted_capacity = weighted_capacity

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
        if issubclass(LaunchTemplateOverrideForDescribeScalingGroupsOutput, dict):
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
        if not isinstance(other, LaunchTemplateOverrideForDescribeScalingGroupsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LaunchTemplateOverrideForDescribeScalingGroupsOutput):
            return True

        return self.to_dict() != other.to_dict()
