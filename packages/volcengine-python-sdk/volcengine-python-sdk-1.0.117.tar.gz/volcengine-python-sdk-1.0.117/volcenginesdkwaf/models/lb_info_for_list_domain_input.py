# coding: utf-8

"""
    waf

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class LBInfoForListDomainInput(object):
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
        'access_mode': 'int',
        'lb_instance_id': 'str'
    }

    attribute_map = {
        'access_mode': 'AccessMode',
        'lb_instance_id': 'LBInstanceID'
    }

    def __init__(self, access_mode=None, lb_instance_id=None, _configuration=None):  # noqa: E501
        """LBInfoForListDomainInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._access_mode = None
        self._lb_instance_id = None
        self.discriminator = None

        if access_mode is not None:
            self.access_mode = access_mode
        if lb_instance_id is not None:
            self.lb_instance_id = lb_instance_id

    @property
    def access_mode(self):
        """Gets the access_mode of this LBInfoForListDomainInput.  # noqa: E501


        :return: The access_mode of this LBInfoForListDomainInput.  # noqa: E501
        :rtype: int
        """
        return self._access_mode

    @access_mode.setter
    def access_mode(self, access_mode):
        """Sets the access_mode of this LBInfoForListDomainInput.


        :param access_mode: The access_mode of this LBInfoForListDomainInput.  # noqa: E501
        :type: int
        """

        self._access_mode = access_mode

    @property
    def lb_instance_id(self):
        """Gets the lb_instance_id of this LBInfoForListDomainInput.  # noqa: E501


        :return: The lb_instance_id of this LBInfoForListDomainInput.  # noqa: E501
        :rtype: str
        """
        return self._lb_instance_id

    @lb_instance_id.setter
    def lb_instance_id(self, lb_instance_id):
        """Sets the lb_instance_id of this LBInfoForListDomainInput.


        :param lb_instance_id: The lb_instance_id of this LBInfoForListDomainInput.  # noqa: E501
        :type: str
        """

        self._lb_instance_id = lb_instance_id

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
        if issubclass(LBInfoForListDomainInput, dict):
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
        if not isinstance(other, LBInfoForListDomainInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LBInfoForListDomainInput):
            return True

        return self.to_dict() != other.to_dict()
