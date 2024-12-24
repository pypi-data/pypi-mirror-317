# coding: utf-8

"""
    cdn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class HstsForAddCdnDomainInput(object):
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
        'subdomain': 'str',
        'switch': 'bool',
        'ttl': 'int'
    }

    attribute_map = {
        'subdomain': 'Subdomain',
        'switch': 'Switch',
        'ttl': 'Ttl'
    }

    def __init__(self, subdomain=None, switch=None, ttl=None, _configuration=None):  # noqa: E501
        """HstsForAddCdnDomainInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._subdomain = None
        self._switch = None
        self._ttl = None
        self.discriminator = None

        if subdomain is not None:
            self.subdomain = subdomain
        if switch is not None:
            self.switch = switch
        if ttl is not None:
            self.ttl = ttl

    @property
    def subdomain(self):
        """Gets the subdomain of this HstsForAddCdnDomainInput.  # noqa: E501


        :return: The subdomain of this HstsForAddCdnDomainInput.  # noqa: E501
        :rtype: str
        """
        return self._subdomain

    @subdomain.setter
    def subdomain(self, subdomain):
        """Sets the subdomain of this HstsForAddCdnDomainInput.


        :param subdomain: The subdomain of this HstsForAddCdnDomainInput.  # noqa: E501
        :type: str
        """

        self._subdomain = subdomain

    @property
    def switch(self):
        """Gets the switch of this HstsForAddCdnDomainInput.  # noqa: E501


        :return: The switch of this HstsForAddCdnDomainInput.  # noqa: E501
        :rtype: bool
        """
        return self._switch

    @switch.setter
    def switch(self, switch):
        """Sets the switch of this HstsForAddCdnDomainInput.


        :param switch: The switch of this HstsForAddCdnDomainInput.  # noqa: E501
        :type: bool
        """

        self._switch = switch

    @property
    def ttl(self):
        """Gets the ttl of this HstsForAddCdnDomainInput.  # noqa: E501


        :return: The ttl of this HstsForAddCdnDomainInput.  # noqa: E501
        :rtype: int
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this HstsForAddCdnDomainInput.


        :param ttl: The ttl of this HstsForAddCdnDomainInput.  # noqa: E501
        :type: int
        """

        self._ttl = ttl

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
        if issubclass(HstsForAddCdnDomainInput, dict):
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
        if not isinstance(other, HstsForAddCdnDomainInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HstsForAddCdnDomainInput):
            return True

        return self.to_dict() != other.to_dict()
