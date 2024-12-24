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


class NasStorageForListFunctionsOutput(object):
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
        'enable_nas': 'bool',
        'nas_configs': 'list[NasConfigForListFunctionsOutput]'
    }

    attribute_map = {
        'enable_nas': 'EnableNas',
        'nas_configs': 'NasConfigs'
    }

    def __init__(self, enable_nas=None, nas_configs=None, _configuration=None):  # noqa: E501
        """NasStorageForListFunctionsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._enable_nas = None
        self._nas_configs = None
        self.discriminator = None

        if enable_nas is not None:
            self.enable_nas = enable_nas
        if nas_configs is not None:
            self.nas_configs = nas_configs

    @property
    def enable_nas(self):
        """Gets the enable_nas of this NasStorageForListFunctionsOutput.  # noqa: E501


        :return: The enable_nas of this NasStorageForListFunctionsOutput.  # noqa: E501
        :rtype: bool
        """
        return self._enable_nas

    @enable_nas.setter
    def enable_nas(self, enable_nas):
        """Sets the enable_nas of this NasStorageForListFunctionsOutput.


        :param enable_nas: The enable_nas of this NasStorageForListFunctionsOutput.  # noqa: E501
        :type: bool
        """

        self._enable_nas = enable_nas

    @property
    def nas_configs(self):
        """Gets the nas_configs of this NasStorageForListFunctionsOutput.  # noqa: E501


        :return: The nas_configs of this NasStorageForListFunctionsOutput.  # noqa: E501
        :rtype: list[NasConfigForListFunctionsOutput]
        """
        return self._nas_configs

    @nas_configs.setter
    def nas_configs(self, nas_configs):
        """Sets the nas_configs of this NasStorageForListFunctionsOutput.


        :param nas_configs: The nas_configs of this NasStorageForListFunctionsOutput.  # noqa: E501
        :type: list[NasConfigForListFunctionsOutput]
        """

        self._nas_configs = nas_configs

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
        if issubclass(NasStorageForListFunctionsOutput, dict):
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
        if not isinstance(other, NasStorageForListFunctionsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NasStorageForListFunctionsOutput):
            return True

        return self.to_dict() != other.to_dict()
