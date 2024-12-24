# coding: utf-8

"""
    cr

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DeleteRepositoryRequest(object):
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
        'name': 'str',
        'namespace': 'str',
        'registry': 'str'
    }

    attribute_map = {
        'name': 'Name',
        'namespace': 'Namespace',
        'registry': 'Registry'
    }

    def __init__(self, name=None, namespace=None, registry=None, _configuration=None):  # noqa: E501
        """DeleteRepositoryRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._namespace = None
        self._registry = None
        self.discriminator = None

        self.name = name
        self.namespace = namespace
        self.registry = registry

    @property
    def name(self):
        """Gets the name of this DeleteRepositoryRequest.  # noqa: E501


        :return: The name of this DeleteRepositoryRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DeleteRepositoryRequest.


        :param name: The name of this DeleteRepositoryRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def namespace(self):
        """Gets the namespace of this DeleteRepositoryRequest.  # noqa: E501


        :return: The namespace of this DeleteRepositoryRequest.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this DeleteRepositoryRequest.


        :param namespace: The namespace of this DeleteRepositoryRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and namespace is None:
            raise ValueError("Invalid value for `namespace`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                namespace is not None and len(namespace) > 90):
            raise ValueError("Invalid value for `namespace`, length must be less than or equal to `90`")  # noqa: E501
        if (self._configuration.client_side_validation and
                namespace is not None and len(namespace) < 2):
            raise ValueError("Invalid value for `namespace`, length must be greater than or equal to `2`")  # noqa: E501

        self._namespace = namespace

    @property
    def registry(self):
        """Gets the registry of this DeleteRepositoryRequest.  # noqa: E501


        :return: The registry of this DeleteRepositoryRequest.  # noqa: E501
        :rtype: str
        """
        return self._registry

    @registry.setter
    def registry(self, registry):
        """Sets the registry of this DeleteRepositoryRequest.


        :param registry: The registry of this DeleteRepositoryRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and registry is None:
            raise ValueError("Invalid value for `registry`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                registry is not None and len(registry) > 30):
            raise ValueError("Invalid value for `registry`, length must be less than or equal to `30`")  # noqa: E501
        if (self._configuration.client_side_validation and
                registry is not None and len(registry) < 3):
            raise ValueError("Invalid value for `registry`, length must be greater than or equal to `3`")  # noqa: E501

        self._registry = registry

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
        if issubclass(DeleteRepositoryRequest, dict):
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
        if not isinstance(other, DeleteRepositoryRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeleteRepositoryRequest):
            return True

        return self.to_dict() != other.to_dict()
