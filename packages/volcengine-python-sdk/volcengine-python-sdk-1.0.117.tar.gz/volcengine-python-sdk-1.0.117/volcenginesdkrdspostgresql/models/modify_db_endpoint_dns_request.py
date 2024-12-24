# coding: utf-8

"""
    rds_postgresql

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ModifyDBEndpointDNSRequest(object):
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
        'dns_visibility': 'bool',
        'endpoint_id': 'str',
        'instance_id': 'str',
        'network_type': 'str'
    }

    attribute_map = {
        'dns_visibility': 'DNSVisibility',
        'endpoint_id': 'EndpointId',
        'instance_id': 'InstanceId',
        'network_type': 'NetworkType'
    }

    def __init__(self, dns_visibility=None, endpoint_id=None, instance_id=None, network_type=None, _configuration=None):  # noqa: E501
        """ModifyDBEndpointDNSRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._dns_visibility = None
        self._endpoint_id = None
        self._instance_id = None
        self._network_type = None
        self.discriminator = None

        self.dns_visibility = dns_visibility
        if endpoint_id is not None:
            self.endpoint_id = endpoint_id
        self.instance_id = instance_id
        self.network_type = network_type

    @property
    def dns_visibility(self):
        """Gets the dns_visibility of this ModifyDBEndpointDNSRequest.  # noqa: E501


        :return: The dns_visibility of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :rtype: bool
        """
        return self._dns_visibility

    @dns_visibility.setter
    def dns_visibility(self, dns_visibility):
        """Sets the dns_visibility of this ModifyDBEndpointDNSRequest.


        :param dns_visibility: The dns_visibility of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :type: bool
        """
        if self._configuration.client_side_validation and dns_visibility is None:
            raise ValueError("Invalid value for `dns_visibility`, must not be `None`")  # noqa: E501

        self._dns_visibility = dns_visibility

    @property
    def endpoint_id(self):
        """Gets the endpoint_id of this ModifyDBEndpointDNSRequest.  # noqa: E501


        :return: The endpoint_id of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, endpoint_id):
        """Sets the endpoint_id of this ModifyDBEndpointDNSRequest.


        :param endpoint_id: The endpoint_id of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :type: str
        """

        self._endpoint_id = endpoint_id

    @property
    def instance_id(self):
        """Gets the instance_id of this ModifyDBEndpointDNSRequest.  # noqa: E501


        :return: The instance_id of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ModifyDBEndpointDNSRequest.


        :param instance_id: The instance_id of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def network_type(self):
        """Gets the network_type of this ModifyDBEndpointDNSRequest.  # noqa: E501


        :return: The network_type of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :rtype: str
        """
        return self._network_type

    @network_type.setter
    def network_type(self, network_type):
        """Sets the network_type of this ModifyDBEndpointDNSRequest.


        :param network_type: The network_type of this ModifyDBEndpointDNSRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and network_type is None:
            raise ValueError("Invalid value for `network_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Private"]  # noqa: E501
        if (self._configuration.client_side_validation and
                network_type not in allowed_values):
            raise ValueError(
                "Invalid value for `network_type` ({0}), must be one of {1}"  # noqa: E501
                .format(network_type, allowed_values)
            )

        self._network_type = network_type

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
        if issubclass(ModifyDBEndpointDNSRequest, dict):
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
        if not isinstance(other, ModifyDBEndpointDNSRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyDBEndpointDNSRequest):
            return True

        return self.to_dict() != other.to_dict()
