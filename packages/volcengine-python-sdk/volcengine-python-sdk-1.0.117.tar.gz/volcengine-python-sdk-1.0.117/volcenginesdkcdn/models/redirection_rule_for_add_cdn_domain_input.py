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


class RedirectionRuleForAddCdnDomainInput(object):
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
        'redirection_action': 'RedirectionActionForAddCdnDomainInput'
    }

    attribute_map = {
        'redirection_action': 'RedirectionAction'
    }

    def __init__(self, redirection_action=None, _configuration=None):  # noqa: E501
        """RedirectionRuleForAddCdnDomainInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._redirection_action = None
        self.discriminator = None

        if redirection_action is not None:
            self.redirection_action = redirection_action

    @property
    def redirection_action(self):
        """Gets the redirection_action of this RedirectionRuleForAddCdnDomainInput.  # noqa: E501


        :return: The redirection_action of this RedirectionRuleForAddCdnDomainInput.  # noqa: E501
        :rtype: RedirectionActionForAddCdnDomainInput
        """
        return self._redirection_action

    @redirection_action.setter
    def redirection_action(self, redirection_action):
        """Sets the redirection_action of this RedirectionRuleForAddCdnDomainInput.


        :param redirection_action: The redirection_action of this RedirectionRuleForAddCdnDomainInput.  # noqa: E501
        :type: RedirectionActionForAddCdnDomainInput
        """

        self._redirection_action = redirection_action

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
        if issubclass(RedirectionRuleForAddCdnDomainInput, dict):
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
        if not isinstance(other, RedirectionRuleForAddCdnDomainInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RedirectionRuleForAddCdnDomainInput):
            return True

        return self.to_dict() != other.to_dict()
