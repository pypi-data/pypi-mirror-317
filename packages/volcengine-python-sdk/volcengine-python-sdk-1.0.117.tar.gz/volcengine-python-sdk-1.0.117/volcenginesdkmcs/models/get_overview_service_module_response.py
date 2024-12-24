# coding: utf-8

"""
    mcs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class GetOverviewServiceModuleResponse(object):
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
        'not_ready_srv_modules': 'list[NotReadySrvModuleForGetOverviewServiceModuleOutput]'
    }

    attribute_map = {
        'not_ready_srv_modules': 'NotReadySrvModules'
    }

    def __init__(self, not_ready_srv_modules=None, _configuration=None):  # noqa: E501
        """GetOverviewServiceModuleResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._not_ready_srv_modules = None
        self.discriminator = None

        if not_ready_srv_modules is not None:
            self.not_ready_srv_modules = not_ready_srv_modules

    @property
    def not_ready_srv_modules(self):
        """Gets the not_ready_srv_modules of this GetOverviewServiceModuleResponse.  # noqa: E501


        :return: The not_ready_srv_modules of this GetOverviewServiceModuleResponse.  # noqa: E501
        :rtype: list[NotReadySrvModuleForGetOverviewServiceModuleOutput]
        """
        return self._not_ready_srv_modules

    @not_ready_srv_modules.setter
    def not_ready_srv_modules(self, not_ready_srv_modules):
        """Sets the not_ready_srv_modules of this GetOverviewServiceModuleResponse.


        :param not_ready_srv_modules: The not_ready_srv_modules of this GetOverviewServiceModuleResponse.  # noqa: E501
        :type: list[NotReadySrvModuleForGetOverviewServiceModuleOutput]
        """

        self._not_ready_srv_modules = not_ready_srv_modules

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
        if issubclass(GetOverviewServiceModuleResponse, dict):
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
        if not isinstance(other, GetOverviewServiceModuleResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetOverviewServiceModuleResponse):
            return True

        return self.to_dict() != other.to_dict()
