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


class ModifyDBEndpointReadWeightRequest(object):
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
        'endpoint_id': 'str',
        'instance_id': 'str',
        'read_only_node_distribution_type': 'str',
        'read_only_node_weight': 'list[ReadOnlyNodeWeightForModifyDBEndpointReadWeightInput]'
    }

    attribute_map = {
        'endpoint_id': 'EndpointId',
        'instance_id': 'InstanceId',
        'read_only_node_distribution_type': 'ReadOnlyNodeDistributionType',
        'read_only_node_weight': 'ReadOnlyNodeWeight'
    }

    def __init__(self, endpoint_id=None, instance_id=None, read_only_node_distribution_type=None, read_only_node_weight=None, _configuration=None):  # noqa: E501
        """ModifyDBEndpointReadWeightRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._endpoint_id = None
        self._instance_id = None
        self._read_only_node_distribution_type = None
        self._read_only_node_weight = None
        self.discriminator = None

        self.endpoint_id = endpoint_id
        self.instance_id = instance_id
        self.read_only_node_distribution_type = read_only_node_distribution_type
        if read_only_node_weight is not None:
            self.read_only_node_weight = read_only_node_weight

    @property
    def endpoint_id(self):
        """Gets the endpoint_id of this ModifyDBEndpointReadWeightRequest.  # noqa: E501


        :return: The endpoint_id of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, endpoint_id):
        """Sets the endpoint_id of this ModifyDBEndpointReadWeightRequest.


        :param endpoint_id: The endpoint_id of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and endpoint_id is None:
            raise ValueError("Invalid value for `endpoint_id`, must not be `None`")  # noqa: E501

        self._endpoint_id = endpoint_id

    @property
    def instance_id(self):
        """Gets the instance_id of this ModifyDBEndpointReadWeightRequest.  # noqa: E501


        :return: The instance_id of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ModifyDBEndpointReadWeightRequest.


        :param instance_id: The instance_id of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def read_only_node_distribution_type(self):
        """Gets the read_only_node_distribution_type of this ModifyDBEndpointReadWeightRequest.  # noqa: E501


        :return: The read_only_node_distribution_type of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :rtype: str
        """
        return self._read_only_node_distribution_type

    @read_only_node_distribution_type.setter
    def read_only_node_distribution_type(self, read_only_node_distribution_type):
        """Sets the read_only_node_distribution_type of this ModifyDBEndpointReadWeightRequest.


        :param read_only_node_distribution_type: The read_only_node_distribution_type of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and read_only_node_distribution_type is None:
            raise ValueError("Invalid value for `read_only_node_distribution_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Default", "Custom"]  # noqa: E501
        if (self._configuration.client_side_validation and
                read_only_node_distribution_type not in allowed_values):
            raise ValueError(
                "Invalid value for `read_only_node_distribution_type` ({0}), must be one of {1}"  # noqa: E501
                .format(read_only_node_distribution_type, allowed_values)
            )

        self._read_only_node_distribution_type = read_only_node_distribution_type

    @property
    def read_only_node_weight(self):
        """Gets the read_only_node_weight of this ModifyDBEndpointReadWeightRequest.  # noqa: E501


        :return: The read_only_node_weight of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :rtype: list[ReadOnlyNodeWeightForModifyDBEndpointReadWeightInput]
        """
        return self._read_only_node_weight

    @read_only_node_weight.setter
    def read_only_node_weight(self, read_only_node_weight):
        """Sets the read_only_node_weight of this ModifyDBEndpointReadWeightRequest.


        :param read_only_node_weight: The read_only_node_weight of this ModifyDBEndpointReadWeightRequest.  # noqa: E501
        :type: list[ReadOnlyNodeWeightForModifyDBEndpointReadWeightInput]
        """

        self._read_only_node_weight = read_only_node_weight

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
        if issubclass(ModifyDBEndpointReadWeightRequest, dict):
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
        if not isinstance(other, ModifyDBEndpointReadWeightRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyDBEndpointReadWeightRequest):
            return True

        return self.to_dict() != other.to_dict()
