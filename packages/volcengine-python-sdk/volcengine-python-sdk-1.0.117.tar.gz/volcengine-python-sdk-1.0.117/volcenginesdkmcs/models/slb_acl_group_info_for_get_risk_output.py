# coding: utf-8

"""
    mcs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class SLBAclGroupInfoForGetRiskOutput(object):
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
        'ip_count': 'int',
        'name': 'str',
        'policy': 'str',
        'uid': 'str'
    }

    attribute_map = {
        'ip_count': 'IPCount',
        'name': 'Name',
        'policy': 'Policy',
        'uid': 'UID'
    }

    def __init__(self, ip_count=None, name=None, policy=None, uid=None, _configuration=None):  # noqa: E501
        """SLBAclGroupInfoForGetRiskOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._ip_count = None
        self._name = None
        self._policy = None
        self._uid = None
        self.discriminator = None

        if ip_count is not None:
            self.ip_count = ip_count
        if name is not None:
            self.name = name
        if policy is not None:
            self.policy = policy
        if uid is not None:
            self.uid = uid

    @property
    def ip_count(self):
        """Gets the ip_count of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501


        :return: The ip_count of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :rtype: int
        """
        return self._ip_count

    @ip_count.setter
    def ip_count(self, ip_count):
        """Sets the ip_count of this SLBAclGroupInfoForGetRiskOutput.


        :param ip_count: The ip_count of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :type: int
        """

        self._ip_count = ip_count

    @property
    def name(self):
        """Gets the name of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501


        :return: The name of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SLBAclGroupInfoForGetRiskOutput.


        :param name: The name of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def policy(self):
        """Gets the policy of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501


        :return: The policy of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """Sets the policy of this SLBAclGroupInfoForGetRiskOutput.


        :param policy: The policy of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._policy = policy

    @property
    def uid(self):
        """Gets the uid of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501


        :return: The uid of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this SLBAclGroupInfoForGetRiskOutput.


        :param uid: The uid of this SLBAclGroupInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._uid = uid

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
        if issubclass(SLBAclGroupInfoForGetRiskOutput, dict):
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
        if not isinstance(other, SLBAclGroupInfoForGetRiskOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SLBAclGroupInfoForGetRiskOutput):
            return True

        return self.to_dict() != other.to_dict()
