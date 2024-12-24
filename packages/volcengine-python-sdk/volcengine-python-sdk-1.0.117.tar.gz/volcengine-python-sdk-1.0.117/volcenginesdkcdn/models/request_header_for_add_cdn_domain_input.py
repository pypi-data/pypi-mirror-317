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


class RequestHeaderForAddCdnDomainInput(object):
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
        'condition': 'ConditionForAddCdnDomainInput',
        'request_header_action': 'RequestHeaderActionForAddCdnDomainInput'
    }

    attribute_map = {
        'condition': 'Condition',
        'request_header_action': 'RequestHeaderAction'
    }

    def __init__(self, condition=None, request_header_action=None, _configuration=None):  # noqa: E501
        """RequestHeaderForAddCdnDomainInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._condition = None
        self._request_header_action = None
        self.discriminator = None

        if condition is not None:
            self.condition = condition
        if request_header_action is not None:
            self.request_header_action = request_header_action

    @property
    def condition(self):
        """Gets the condition of this RequestHeaderForAddCdnDomainInput.  # noqa: E501


        :return: The condition of this RequestHeaderForAddCdnDomainInput.  # noqa: E501
        :rtype: ConditionForAddCdnDomainInput
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this RequestHeaderForAddCdnDomainInput.


        :param condition: The condition of this RequestHeaderForAddCdnDomainInput.  # noqa: E501
        :type: ConditionForAddCdnDomainInput
        """

        self._condition = condition

    @property
    def request_header_action(self):
        """Gets the request_header_action of this RequestHeaderForAddCdnDomainInput.  # noqa: E501


        :return: The request_header_action of this RequestHeaderForAddCdnDomainInput.  # noqa: E501
        :rtype: RequestHeaderActionForAddCdnDomainInput
        """
        return self._request_header_action

    @request_header_action.setter
    def request_header_action(self, request_header_action):
        """Sets the request_header_action of this RequestHeaderForAddCdnDomainInput.


        :param request_header_action: The request_header_action of this RequestHeaderForAddCdnDomainInput.  # noqa: E501
        :type: RequestHeaderActionForAddCdnDomainInput
        """

        self._request_header_action = request_header_action

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
        if issubclass(RequestHeaderForAddCdnDomainInput, dict):
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
        if not isinstance(other, RequestHeaderForAddCdnDomainInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RequestHeaderForAddCdnDomainInput):
            return True

        return self.to_dict() != other.to_dict()
