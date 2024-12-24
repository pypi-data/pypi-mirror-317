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


class CommonTypeForUpdateCdnConfigInput(object):
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
        'ignore_case': 'bool',
        'ignore_scheme': 'bool',
        'referers': 'list[str]'
    }

    attribute_map = {
        'ignore_case': 'IgnoreCase',
        'ignore_scheme': 'IgnoreScheme',
        'referers': 'Referers'
    }

    def __init__(self, ignore_case=None, ignore_scheme=None, referers=None, _configuration=None):  # noqa: E501
        """CommonTypeForUpdateCdnConfigInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._ignore_case = None
        self._ignore_scheme = None
        self._referers = None
        self.discriminator = None

        if ignore_case is not None:
            self.ignore_case = ignore_case
        if ignore_scheme is not None:
            self.ignore_scheme = ignore_scheme
        if referers is not None:
            self.referers = referers

    @property
    def ignore_case(self):
        """Gets the ignore_case of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501


        :return: The ignore_case of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_case

    @ignore_case.setter
    def ignore_case(self, ignore_case):
        """Sets the ignore_case of this CommonTypeForUpdateCdnConfigInput.


        :param ignore_case: The ignore_case of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501
        :type: bool
        """

        self._ignore_case = ignore_case

    @property
    def ignore_scheme(self):
        """Gets the ignore_scheme of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501


        :return: The ignore_scheme of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_scheme

    @ignore_scheme.setter
    def ignore_scheme(self, ignore_scheme):
        """Sets the ignore_scheme of this CommonTypeForUpdateCdnConfigInput.


        :param ignore_scheme: The ignore_scheme of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501
        :type: bool
        """

        self._ignore_scheme = ignore_scheme

    @property
    def referers(self):
        """Gets the referers of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501


        :return: The referers of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._referers

    @referers.setter
    def referers(self, referers):
        """Sets the referers of this CommonTypeForUpdateCdnConfigInput.


        :param referers: The referers of this CommonTypeForUpdateCdnConfigInput.  # noqa: E501
        :type: list[str]
        """

        self._referers = referers

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
        if issubclass(CommonTypeForUpdateCdnConfigInput, dict):
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
        if not isinstance(other, CommonTypeForUpdateCdnConfigInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CommonTypeForUpdateCdnConfigInput):
            return True

        return self.to_dict() != other.to_dict()
