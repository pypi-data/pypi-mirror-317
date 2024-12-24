# coding: utf-8

"""
    transitrouter

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ModifyTransitRouterForwardPolicyTableAttributesRequest(object):
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
        'description': 'str',
        'transit_router_forward_policy_table_id': 'str',
        'transit_router_forward_policy_table_name': 'str'
    }

    attribute_map = {
        'description': 'Description',
        'transit_router_forward_policy_table_id': 'TransitRouterForwardPolicyTableId',
        'transit_router_forward_policy_table_name': 'TransitRouterForwardPolicyTableName'
    }

    def __init__(self, description=None, transit_router_forward_policy_table_id=None, transit_router_forward_policy_table_name=None, _configuration=None):  # noqa: E501
        """ModifyTransitRouterForwardPolicyTableAttributesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._description = None
        self._transit_router_forward_policy_table_id = None
        self._transit_router_forward_policy_table_name = None
        self.discriminator = None

        if description is not None:
            self.description = description
        self.transit_router_forward_policy_table_id = transit_router_forward_policy_table_id
        if transit_router_forward_policy_table_name is not None:
            self.transit_router_forward_policy_table_name = transit_router_forward_policy_table_name

    @property
    def description(self):
        """Gets the description of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501


        :return: The description of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ModifyTransitRouterForwardPolicyTableAttributesRequest.


        :param description: The description of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def transit_router_forward_policy_table_id(self):
        """Gets the transit_router_forward_policy_table_id of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501


        :return: The transit_router_forward_policy_table_id of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_forward_policy_table_id

    @transit_router_forward_policy_table_id.setter
    def transit_router_forward_policy_table_id(self, transit_router_forward_policy_table_id):
        """Sets the transit_router_forward_policy_table_id of this ModifyTransitRouterForwardPolicyTableAttributesRequest.


        :param transit_router_forward_policy_table_id: The transit_router_forward_policy_table_id of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and transit_router_forward_policy_table_id is None:
            raise ValueError("Invalid value for `transit_router_forward_policy_table_id`, must not be `None`")  # noqa: E501

        self._transit_router_forward_policy_table_id = transit_router_forward_policy_table_id

    @property
    def transit_router_forward_policy_table_name(self):
        """Gets the transit_router_forward_policy_table_name of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501


        :return: The transit_router_forward_policy_table_name of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_forward_policy_table_name

    @transit_router_forward_policy_table_name.setter
    def transit_router_forward_policy_table_name(self, transit_router_forward_policy_table_name):
        """Sets the transit_router_forward_policy_table_name of this ModifyTransitRouterForwardPolicyTableAttributesRequest.


        :param transit_router_forward_policy_table_name: The transit_router_forward_policy_table_name of this ModifyTransitRouterForwardPolicyTableAttributesRequest.  # noqa: E501
        :type: str
        """

        self._transit_router_forward_policy_table_name = transit_router_forward_policy_table_name

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
        if issubclass(ModifyTransitRouterForwardPolicyTableAttributesRequest, dict):
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
        if not isinstance(other, ModifyTransitRouterForwardPolicyTableAttributesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyTransitRouterForwardPolicyTableAttributesRequest):
            return True

        return self.to_dict() != other.to_dict()
