# coding: utf-8

"""
    cv20240606

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class LogoInfoForFaceSwapInput(object):
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
        'add_logo': 'bool',
        'language': 'int',
        'logo_text_content': 'str',
        'position': 'int'
    }

    attribute_map = {
        'add_logo': 'add_logo',
        'language': 'language',
        'logo_text_content': 'logo_text_content',
        'position': 'position'
    }

    def __init__(self, add_logo=None, language=None, logo_text_content=None, position=None, _configuration=None):  # noqa: E501
        """LogoInfoForFaceSwapInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._add_logo = None
        self._language = None
        self._logo_text_content = None
        self._position = None
        self.discriminator = None

        if add_logo is not None:
            self.add_logo = add_logo
        if language is not None:
            self.language = language
        if logo_text_content is not None:
            self.logo_text_content = logo_text_content
        if position is not None:
            self.position = position

    @property
    def add_logo(self):
        """Gets the add_logo of this LogoInfoForFaceSwapInput.  # noqa: E501


        :return: The add_logo of this LogoInfoForFaceSwapInput.  # noqa: E501
        :rtype: bool
        """
        return self._add_logo

    @add_logo.setter
    def add_logo(self, add_logo):
        """Sets the add_logo of this LogoInfoForFaceSwapInput.


        :param add_logo: The add_logo of this LogoInfoForFaceSwapInput.  # noqa: E501
        :type: bool
        """

        self._add_logo = add_logo

    @property
    def language(self):
        """Gets the language of this LogoInfoForFaceSwapInput.  # noqa: E501


        :return: The language of this LogoInfoForFaceSwapInput.  # noqa: E501
        :rtype: int
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this LogoInfoForFaceSwapInput.


        :param language: The language of this LogoInfoForFaceSwapInput.  # noqa: E501
        :type: int
        """

        self._language = language

    @property
    def logo_text_content(self):
        """Gets the logo_text_content of this LogoInfoForFaceSwapInput.  # noqa: E501


        :return: The logo_text_content of this LogoInfoForFaceSwapInput.  # noqa: E501
        :rtype: str
        """
        return self._logo_text_content

    @logo_text_content.setter
    def logo_text_content(self, logo_text_content):
        """Sets the logo_text_content of this LogoInfoForFaceSwapInput.


        :param logo_text_content: The logo_text_content of this LogoInfoForFaceSwapInput.  # noqa: E501
        :type: str
        """

        self._logo_text_content = logo_text_content

    @property
    def position(self):
        """Gets the position of this LogoInfoForFaceSwapInput.  # noqa: E501


        :return: The position of this LogoInfoForFaceSwapInput.  # noqa: E501
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this LogoInfoForFaceSwapInput.


        :param position: The position of this LogoInfoForFaceSwapInput.  # noqa: E501
        :type: int
        """

        self._position = position

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
        if issubclass(LogoInfoForFaceSwapInput, dict):
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
        if not isinstance(other, LogoInfoForFaceSwapInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LogoInfoForFaceSwapInput):
            return True

        return self.to_dict() != other.to_dict()
