# coding: utf-8

"""
    rocketmq

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class AccessPolicyForDescribeTopicAccessPoliciesOutput(object):
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
        'access_key': 'str',
        'authority': 'str'
    }

    attribute_map = {
        'access_key': 'AccessKey',
        'authority': 'Authority'
    }

    def __init__(self, access_key=None, authority=None, _configuration=None):  # noqa: E501
        """AccessPolicyForDescribeTopicAccessPoliciesOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._access_key = None
        self._authority = None
        self.discriminator = None

        if access_key is not None:
            self.access_key = access_key
        if authority is not None:
            self.authority = authority

    @property
    def access_key(self):
        """Gets the access_key of this AccessPolicyForDescribeTopicAccessPoliciesOutput.  # noqa: E501


        :return: The access_key of this AccessPolicyForDescribeTopicAccessPoliciesOutput.  # noqa: E501
        :rtype: str
        """
        return self._access_key

    @access_key.setter
    def access_key(self, access_key):
        """Sets the access_key of this AccessPolicyForDescribeTopicAccessPoliciesOutput.


        :param access_key: The access_key of this AccessPolicyForDescribeTopicAccessPoliciesOutput.  # noqa: E501
        :type: str
        """

        self._access_key = access_key

    @property
    def authority(self):
        """Gets the authority of this AccessPolicyForDescribeTopicAccessPoliciesOutput.  # noqa: E501


        :return: The authority of this AccessPolicyForDescribeTopicAccessPoliciesOutput.  # noqa: E501
        :rtype: str
        """
        return self._authority

    @authority.setter
    def authority(self, authority):
        """Sets the authority of this AccessPolicyForDescribeTopicAccessPoliciesOutput.


        :param authority: The authority of this AccessPolicyForDescribeTopicAccessPoliciesOutput.  # noqa: E501
        :type: str
        """

        self._authority = authority

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
        if issubclass(AccessPolicyForDescribeTopicAccessPoliciesOutput, dict):
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
        if not isinstance(other, AccessPolicyForDescribeTopicAccessPoliciesOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccessPolicyForDescribeTopicAccessPoliciesOutput):
            return True

        return self.to_dict() != other.to_dict()
