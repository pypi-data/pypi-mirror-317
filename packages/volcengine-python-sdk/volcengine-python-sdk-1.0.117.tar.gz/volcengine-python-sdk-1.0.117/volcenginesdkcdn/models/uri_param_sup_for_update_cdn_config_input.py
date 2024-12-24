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


class UriParamSupForUpdateCdnConfigInput(object):
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
        'join_symbol': 'str',
        'split_symbol': 'str',
        'start_level': 'int',
        'term_level': 'int'
    }

    attribute_map = {
        'join_symbol': 'JoinSymbol',
        'split_symbol': 'SplitSymbol',
        'start_level': 'StartLevel',
        'term_level': 'TermLevel'
    }

    def __init__(self, join_symbol=None, split_symbol=None, start_level=None, term_level=None, _configuration=None):  # noqa: E501
        """UriParamSupForUpdateCdnConfigInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._join_symbol = None
        self._split_symbol = None
        self._start_level = None
        self._term_level = None
        self.discriminator = None

        if join_symbol is not None:
            self.join_symbol = join_symbol
        if split_symbol is not None:
            self.split_symbol = split_symbol
        if start_level is not None:
            self.start_level = start_level
        if term_level is not None:
            self.term_level = term_level

    @property
    def join_symbol(self):
        """Gets the join_symbol of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501


        :return: The join_symbol of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :rtype: str
        """
        return self._join_symbol

    @join_symbol.setter
    def join_symbol(self, join_symbol):
        """Sets the join_symbol of this UriParamSupForUpdateCdnConfigInput.


        :param join_symbol: The join_symbol of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :type: str
        """

        self._join_symbol = join_symbol

    @property
    def split_symbol(self):
        """Gets the split_symbol of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501


        :return: The split_symbol of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :rtype: str
        """
        return self._split_symbol

    @split_symbol.setter
    def split_symbol(self, split_symbol):
        """Sets the split_symbol of this UriParamSupForUpdateCdnConfigInput.


        :param split_symbol: The split_symbol of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :type: str
        """

        self._split_symbol = split_symbol

    @property
    def start_level(self):
        """Gets the start_level of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501


        :return: The start_level of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :rtype: int
        """
        return self._start_level

    @start_level.setter
    def start_level(self, start_level):
        """Sets the start_level of this UriParamSupForUpdateCdnConfigInput.


        :param start_level: The start_level of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :type: int
        """

        self._start_level = start_level

    @property
    def term_level(self):
        """Gets the term_level of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501


        :return: The term_level of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :rtype: int
        """
        return self._term_level

    @term_level.setter
    def term_level(self, term_level):
        """Sets the term_level of this UriParamSupForUpdateCdnConfigInput.


        :param term_level: The term_level of this UriParamSupForUpdateCdnConfigInput.  # noqa: E501
        :type: int
        """

        self._term_level = term_level

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
        if issubclass(UriParamSupForUpdateCdnConfigInput, dict):
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
        if not isinstance(other, UriParamSupForUpdateCdnConfigInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UriParamSupForUpdateCdnConfigInput):
            return True

        return self.to_dict() != other.to_dict()
