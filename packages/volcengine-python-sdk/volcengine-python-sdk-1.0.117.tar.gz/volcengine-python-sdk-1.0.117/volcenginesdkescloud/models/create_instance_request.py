# coding: utf-8

"""
    escloud

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateInstanceRequest(object):
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
        'client_token': 'str',
        'instance_configuration': 'InstanceConfigurationForCreateInstanceInput',
        'tags': 'list[TagForCreateInstanceInput]'
    }

    attribute_map = {
        'client_token': 'ClientToken',
        'instance_configuration': 'InstanceConfiguration',
        'tags': 'Tags'
    }

    def __init__(self, client_token=None, instance_configuration=None, tags=None, _configuration=None):  # noqa: E501
        """CreateInstanceRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._client_token = None
        self._instance_configuration = None
        self._tags = None
        self.discriminator = None

        if client_token is not None:
            self.client_token = client_token
        if instance_configuration is not None:
            self.instance_configuration = instance_configuration
        if tags is not None:
            self.tags = tags

    @property
    def client_token(self):
        """Gets the client_token of this CreateInstanceRequest.  # noqa: E501


        :return: The client_token of this CreateInstanceRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this CreateInstanceRequest.


        :param client_token: The client_token of this CreateInstanceRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def instance_configuration(self):
        """Gets the instance_configuration of this CreateInstanceRequest.  # noqa: E501


        :return: The instance_configuration of this CreateInstanceRequest.  # noqa: E501
        :rtype: InstanceConfigurationForCreateInstanceInput
        """
        return self._instance_configuration

    @instance_configuration.setter
    def instance_configuration(self, instance_configuration):
        """Sets the instance_configuration of this CreateInstanceRequest.


        :param instance_configuration: The instance_configuration of this CreateInstanceRequest.  # noqa: E501
        :type: InstanceConfigurationForCreateInstanceInput
        """

        self._instance_configuration = instance_configuration

    @property
    def tags(self):
        """Gets the tags of this CreateInstanceRequest.  # noqa: E501


        :return: The tags of this CreateInstanceRequest.  # noqa: E501
        :rtype: list[TagForCreateInstanceInput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateInstanceRequest.


        :param tags: The tags of this CreateInstanceRequest.  # noqa: E501
        :type: list[TagForCreateInstanceInput]
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
        if issubclass(CreateInstanceRequest, dict):
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
        if not isinstance(other, CreateInstanceRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateInstanceRequest):
            return True

        return self.to_dict() != other.to_dict()
