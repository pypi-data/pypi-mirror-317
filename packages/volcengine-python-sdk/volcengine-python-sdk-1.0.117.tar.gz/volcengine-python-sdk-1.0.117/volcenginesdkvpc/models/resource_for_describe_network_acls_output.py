# coding: utf-8

"""
    vpc

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ResourceForDescribeNetworkAclsOutput(object):
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
        'resource_id': 'str',
        'status': 'str'
    }

    attribute_map = {
        'resource_id': 'ResourceId',
        'status': 'Status'
    }

    def __init__(self, resource_id=None, status=None, _configuration=None):  # noqa: E501
        """ResourceForDescribeNetworkAclsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._resource_id = None
        self._status = None
        self.discriminator = None

        if resource_id is not None:
            self.resource_id = resource_id
        if status is not None:
            self.status = status

    @property
    def resource_id(self):
        """Gets the resource_id of this ResourceForDescribeNetworkAclsOutput.  # noqa: E501


        :return: The resource_id of this ResourceForDescribeNetworkAclsOutput.  # noqa: E501
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """Sets the resource_id of this ResourceForDescribeNetworkAclsOutput.


        :param resource_id: The resource_id of this ResourceForDescribeNetworkAclsOutput.  # noqa: E501
        :type: str
        """

        self._resource_id = resource_id

    @property
    def status(self):
        """Gets the status of this ResourceForDescribeNetworkAclsOutput.  # noqa: E501


        :return: The status of this ResourceForDescribeNetworkAclsOutput.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ResourceForDescribeNetworkAclsOutput.


        :param status: The status of this ResourceForDescribeNetworkAclsOutput.  # noqa: E501
        :type: str
        """

        self._status = status

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
        if issubclass(ResourceForDescribeNetworkAclsOutput, dict):
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
        if not isinstance(other, ResourceForDescribeNetworkAclsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResourceForDescribeNetworkAclsOutput):
            return True

        return self.to_dict() != other.to_dict()
