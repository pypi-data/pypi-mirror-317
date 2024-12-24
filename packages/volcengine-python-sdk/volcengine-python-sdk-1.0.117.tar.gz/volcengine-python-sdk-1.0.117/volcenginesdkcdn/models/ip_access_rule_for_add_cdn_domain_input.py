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


class IpAccessRuleForAddCdnDomainInput(object):
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
        'ip': 'list[str]',
        'rule_type': 'str',
        'shared_config': 'SharedConfigForAddCdnDomainInput',
        'switch': 'bool'
    }

    attribute_map = {
        'ip': 'Ip',
        'rule_type': 'RuleType',
        'shared_config': 'SharedConfig',
        'switch': 'Switch'
    }

    def __init__(self, ip=None, rule_type=None, shared_config=None, switch=None, _configuration=None):  # noqa: E501
        """IpAccessRuleForAddCdnDomainInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._ip = None
        self._rule_type = None
        self._shared_config = None
        self._switch = None
        self.discriminator = None

        if ip is not None:
            self.ip = ip
        if rule_type is not None:
            self.rule_type = rule_type
        if shared_config is not None:
            self.shared_config = shared_config
        if switch is not None:
            self.switch = switch

    @property
    def ip(self):
        """Gets the ip of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501


        :return: The ip of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this IpAccessRuleForAddCdnDomainInput.


        :param ip: The ip of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :type: list[str]
        """

        self._ip = ip

    @property
    def rule_type(self):
        """Gets the rule_type of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501


        :return: The rule_type of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :rtype: str
        """
        return self._rule_type

    @rule_type.setter
    def rule_type(self, rule_type):
        """Sets the rule_type of this IpAccessRuleForAddCdnDomainInput.


        :param rule_type: The rule_type of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :type: str
        """

        self._rule_type = rule_type

    @property
    def shared_config(self):
        """Gets the shared_config of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501


        :return: The shared_config of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :rtype: SharedConfigForAddCdnDomainInput
        """
        return self._shared_config

    @shared_config.setter
    def shared_config(self, shared_config):
        """Sets the shared_config of this IpAccessRuleForAddCdnDomainInput.


        :param shared_config: The shared_config of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :type: SharedConfigForAddCdnDomainInput
        """

        self._shared_config = shared_config

    @property
    def switch(self):
        """Gets the switch of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501


        :return: The switch of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :rtype: bool
        """
        return self._switch

    @switch.setter
    def switch(self, switch):
        """Sets the switch of this IpAccessRuleForAddCdnDomainInput.


        :param switch: The switch of this IpAccessRuleForAddCdnDomainInput.  # noqa: E501
        :type: bool
        """

        self._switch = switch

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
        if issubclass(IpAccessRuleForAddCdnDomainInput, dict):
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
        if not isinstance(other, IpAccessRuleForAddCdnDomainInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IpAccessRuleForAddCdnDomainInput):
            return True

        return self.to_dict() != other.to_dict()
