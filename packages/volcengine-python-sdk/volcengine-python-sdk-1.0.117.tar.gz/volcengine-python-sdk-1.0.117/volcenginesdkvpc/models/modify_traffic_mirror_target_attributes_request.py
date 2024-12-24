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


class ModifyTrafficMirrorTargetAttributesRequest(object):
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
        'traffic_mirror_target_id': 'str',
        'traffic_mirror_target_name': 'str'
    }

    attribute_map = {
        'description': 'Description',
        'traffic_mirror_target_id': 'TrafficMirrorTargetId',
        'traffic_mirror_target_name': 'TrafficMirrorTargetName'
    }

    def __init__(self, description=None, traffic_mirror_target_id=None, traffic_mirror_target_name=None, _configuration=None):  # noqa: E501
        """ModifyTrafficMirrorTargetAttributesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._description = None
        self._traffic_mirror_target_id = None
        self._traffic_mirror_target_name = None
        self.discriminator = None

        if description is not None:
            self.description = description
        self.traffic_mirror_target_id = traffic_mirror_target_id
        if traffic_mirror_target_name is not None:
            self.traffic_mirror_target_name = traffic_mirror_target_name

    @property
    def description(self):
        """Gets the description of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501


        :return: The description of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ModifyTrafficMirrorTargetAttributesRequest.


        :param description: The description of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def traffic_mirror_target_id(self):
        """Gets the traffic_mirror_target_id of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501


        :return: The traffic_mirror_target_id of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._traffic_mirror_target_id

    @traffic_mirror_target_id.setter
    def traffic_mirror_target_id(self, traffic_mirror_target_id):
        """Sets the traffic_mirror_target_id of this ModifyTrafficMirrorTargetAttributesRequest.


        :param traffic_mirror_target_id: The traffic_mirror_target_id of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and traffic_mirror_target_id is None:
            raise ValueError("Invalid value for `traffic_mirror_target_id`, must not be `None`")  # noqa: E501

        self._traffic_mirror_target_id = traffic_mirror_target_id

    @property
    def traffic_mirror_target_name(self):
        """Gets the traffic_mirror_target_name of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501


        :return: The traffic_mirror_target_name of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._traffic_mirror_target_name

    @traffic_mirror_target_name.setter
    def traffic_mirror_target_name(self, traffic_mirror_target_name):
        """Sets the traffic_mirror_target_name of this ModifyTrafficMirrorTargetAttributesRequest.


        :param traffic_mirror_target_name: The traffic_mirror_target_name of this ModifyTrafficMirrorTargetAttributesRequest.  # noqa: E501
        :type: str
        """

        self._traffic_mirror_target_name = traffic_mirror_target_name

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
        if issubclass(ModifyTrafficMirrorTargetAttributesRequest, dict):
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
        if not isinstance(other, ModifyTrafficMirrorTargetAttributesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyTrafficMirrorTargetAttributesRequest):
            return True

        return self.to_dict() != other.to_dict()
