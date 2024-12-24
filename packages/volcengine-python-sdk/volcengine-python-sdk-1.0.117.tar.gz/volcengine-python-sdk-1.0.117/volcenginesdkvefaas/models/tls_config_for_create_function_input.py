# coding: utf-8

"""
    vefaas

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class TlsConfigForCreateFunctionInput(object):
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
        'enable_log': 'bool',
        'tls_project_id': 'str',
        'tls_topic_id': 'str'
    }

    attribute_map = {
        'enable_log': 'EnableLog',
        'tls_project_id': 'TlsProjectId',
        'tls_topic_id': 'TlsTopicId'
    }

    def __init__(self, enable_log=None, tls_project_id=None, tls_topic_id=None, _configuration=None):  # noqa: E501
        """TlsConfigForCreateFunctionInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._enable_log = None
        self._tls_project_id = None
        self._tls_topic_id = None
        self.discriminator = None

        if enable_log is not None:
            self.enable_log = enable_log
        if tls_project_id is not None:
            self.tls_project_id = tls_project_id
        if tls_topic_id is not None:
            self.tls_topic_id = tls_topic_id

    @property
    def enable_log(self):
        """Gets the enable_log of this TlsConfigForCreateFunctionInput.  # noqa: E501


        :return: The enable_log of this TlsConfigForCreateFunctionInput.  # noqa: E501
        :rtype: bool
        """
        return self._enable_log

    @enable_log.setter
    def enable_log(self, enable_log):
        """Sets the enable_log of this TlsConfigForCreateFunctionInput.


        :param enable_log: The enable_log of this TlsConfigForCreateFunctionInput.  # noqa: E501
        :type: bool
        """

        self._enable_log = enable_log

    @property
    def tls_project_id(self):
        """Gets the tls_project_id of this TlsConfigForCreateFunctionInput.  # noqa: E501


        :return: The tls_project_id of this TlsConfigForCreateFunctionInput.  # noqa: E501
        :rtype: str
        """
        return self._tls_project_id

    @tls_project_id.setter
    def tls_project_id(self, tls_project_id):
        """Sets the tls_project_id of this TlsConfigForCreateFunctionInput.


        :param tls_project_id: The tls_project_id of this TlsConfigForCreateFunctionInput.  # noqa: E501
        :type: str
        """

        self._tls_project_id = tls_project_id

    @property
    def tls_topic_id(self):
        """Gets the tls_topic_id of this TlsConfigForCreateFunctionInput.  # noqa: E501


        :return: The tls_topic_id of this TlsConfigForCreateFunctionInput.  # noqa: E501
        :rtype: str
        """
        return self._tls_topic_id

    @tls_topic_id.setter
    def tls_topic_id(self, tls_topic_id):
        """Sets the tls_topic_id of this TlsConfigForCreateFunctionInput.


        :param tls_topic_id: The tls_topic_id of this TlsConfigForCreateFunctionInput.  # noqa: E501
        :type: str
        """

        self._tls_topic_id = tls_topic_id

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
        if issubclass(TlsConfigForCreateFunctionInput, dict):
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
        if not isinstance(other, TlsConfigForCreateFunctionInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TlsConfigForCreateFunctionInput):
            return True

        return self.to_dict() != other.to_dict()
