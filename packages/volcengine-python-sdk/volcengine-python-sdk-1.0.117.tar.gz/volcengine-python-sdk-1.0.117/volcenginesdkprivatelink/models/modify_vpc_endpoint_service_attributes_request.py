# coding: utf-8

"""
    privatelink

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ModifyVpcEndpointServiceAttributesRequest(object):
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
        'auto_accept_enabled': 'bool',
        'description': 'str',
        'ip_address_versions': 'list[str]',
        'private_dns_enabled': 'str',
        'private_dns_name': 'str',
        'private_dns_type': 'str',
        'service_id': 'str'
    }

    attribute_map = {
        'auto_accept_enabled': 'AutoAcceptEnabled',
        'description': 'Description',
        'ip_address_versions': 'IpAddressVersions',
        'private_dns_enabled': 'PrivateDNSEnabled',
        'private_dns_name': 'PrivateDNSName',
        'private_dns_type': 'PrivateDNSType',
        'service_id': 'ServiceId'
    }

    def __init__(self, auto_accept_enabled=None, description=None, ip_address_versions=None, private_dns_enabled=None, private_dns_name=None, private_dns_type=None, service_id=None, _configuration=None):  # noqa: E501
        """ModifyVpcEndpointServiceAttributesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._auto_accept_enabled = None
        self._description = None
        self._ip_address_versions = None
        self._private_dns_enabled = None
        self._private_dns_name = None
        self._private_dns_type = None
        self._service_id = None
        self.discriminator = None

        if auto_accept_enabled is not None:
            self.auto_accept_enabled = auto_accept_enabled
        if description is not None:
            self.description = description
        if ip_address_versions is not None:
            self.ip_address_versions = ip_address_versions
        if private_dns_enabled is not None:
            self.private_dns_enabled = private_dns_enabled
        if private_dns_name is not None:
            self.private_dns_name = private_dns_name
        if private_dns_type is not None:
            self.private_dns_type = private_dns_type
        self.service_id = service_id

    @property
    def auto_accept_enabled(self):
        """Gets the auto_accept_enabled of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501


        :return: The auto_accept_enabled of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :rtype: bool
        """
        return self._auto_accept_enabled

    @auto_accept_enabled.setter
    def auto_accept_enabled(self, auto_accept_enabled):
        """Sets the auto_accept_enabled of this ModifyVpcEndpointServiceAttributesRequest.


        :param auto_accept_enabled: The auto_accept_enabled of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :type: bool
        """

        self._auto_accept_enabled = auto_accept_enabled

    @property
    def description(self):
        """Gets the description of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501


        :return: The description of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ModifyVpcEndpointServiceAttributesRequest.


        :param description: The description of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def ip_address_versions(self):
        """Gets the ip_address_versions of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501


        :return: The ip_address_versions of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._ip_address_versions

    @ip_address_versions.setter
    def ip_address_versions(self, ip_address_versions):
        """Sets the ip_address_versions of this ModifyVpcEndpointServiceAttributesRequest.


        :param ip_address_versions: The ip_address_versions of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :type: list[str]
        """

        self._ip_address_versions = ip_address_versions

    @property
    def private_dns_enabled(self):
        """Gets the private_dns_enabled of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501


        :return: The private_dns_enabled of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._private_dns_enabled

    @private_dns_enabled.setter
    def private_dns_enabled(self, private_dns_enabled):
        """Sets the private_dns_enabled of this ModifyVpcEndpointServiceAttributesRequest.


        :param private_dns_enabled: The private_dns_enabled of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :type: str
        """

        self._private_dns_enabled = private_dns_enabled

    @property
    def private_dns_name(self):
        """Gets the private_dns_name of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501


        :return: The private_dns_name of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._private_dns_name

    @private_dns_name.setter
    def private_dns_name(self, private_dns_name):
        """Sets the private_dns_name of this ModifyVpcEndpointServiceAttributesRequest.


        :param private_dns_name: The private_dns_name of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :type: str
        """

        self._private_dns_name = private_dns_name

    @property
    def private_dns_type(self):
        """Gets the private_dns_type of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501


        :return: The private_dns_type of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._private_dns_type

    @private_dns_type.setter
    def private_dns_type(self, private_dns_type):
        """Sets the private_dns_type of this ModifyVpcEndpointServiceAttributesRequest.


        :param private_dns_type: The private_dns_type of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :type: str
        """

        self._private_dns_type = private_dns_type

    @property
    def service_id(self):
        """Gets the service_id of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501


        :return: The service_id of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id):
        """Sets the service_id of this ModifyVpcEndpointServiceAttributesRequest.


        :param service_id: The service_id of this ModifyVpcEndpointServiceAttributesRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and service_id is None:
            raise ValueError("Invalid value for `service_id`, must not be `None`")  # noqa: E501

        self._service_id = service_id

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
        if issubclass(ModifyVpcEndpointServiceAttributesRequest, dict):
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
        if not isinstance(other, ModifyVpcEndpointServiceAttributesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyVpcEndpointServiceAttributesRequest):
            return True

        return self.to_dict() != other.to_dict()
