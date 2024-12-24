# coding: utf-8

"""
    iam

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateServiceLinkedRoleRequest(object):
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
        'service_name': 'str',
        'tags': 'list[TagForCreateServiceLinkedRoleInput]'
    }

    attribute_map = {
        'service_name': 'ServiceName',
        'tags': 'Tags'
    }

    def __init__(self, service_name=None, tags=None, _configuration=None):  # noqa: E501
        """CreateServiceLinkedRoleRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._service_name = None
        self._tags = None
        self.discriminator = None

        self.service_name = service_name
        if tags is not None:
            self.tags = tags

    @property
    def service_name(self):
        """Gets the service_name of this CreateServiceLinkedRoleRequest.  # noqa: E501


        :return: The service_name of this CreateServiceLinkedRoleRequest.  # noqa: E501
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """Sets the service_name of this CreateServiceLinkedRoleRequest.


        :param service_name: The service_name of this CreateServiceLinkedRoleRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and service_name is None:
            raise ValueError("Invalid value for `service_name`, must not be `None`")  # noqa: E501

        self._service_name = service_name

    @property
    def tags(self):
        """Gets the tags of this CreateServiceLinkedRoleRequest.  # noqa: E501


        :return: The tags of this CreateServiceLinkedRoleRequest.  # noqa: E501
        :rtype: list[TagForCreateServiceLinkedRoleInput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateServiceLinkedRoleRequest.


        :param tags: The tags of this CreateServiceLinkedRoleRequest.  # noqa: E501
        :type: list[TagForCreateServiceLinkedRoleInput]
        """

        self._tags = tags

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
        if issubclass(CreateServiceLinkedRoleRequest, dict):
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
        if not isinstance(other, CreateServiceLinkedRoleRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateServiceLinkedRoleRequest):
            return True

        return self.to_dict() != other.to_dict()
