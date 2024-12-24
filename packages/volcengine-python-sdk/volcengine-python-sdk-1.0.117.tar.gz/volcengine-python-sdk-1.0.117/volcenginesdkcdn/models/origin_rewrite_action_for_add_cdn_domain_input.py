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


class OriginRewriteActionForAddCdnDomainInput(object):
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
        'rewrite_type': 'str',
        'source_path': 'str',
        'target_path': 'str'
    }

    attribute_map = {
        'rewrite_type': 'RewriteType',
        'source_path': 'SourcePath',
        'target_path': 'TargetPath'
    }

    def __init__(self, rewrite_type=None, source_path=None, target_path=None, _configuration=None):  # noqa: E501
        """OriginRewriteActionForAddCdnDomainInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._rewrite_type = None
        self._source_path = None
        self._target_path = None
        self.discriminator = None

        if rewrite_type is not None:
            self.rewrite_type = rewrite_type
        if source_path is not None:
            self.source_path = source_path
        if target_path is not None:
            self.target_path = target_path

    @property
    def rewrite_type(self):
        """Gets the rewrite_type of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501


        :return: The rewrite_type of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501
        :rtype: str
        """
        return self._rewrite_type

    @rewrite_type.setter
    def rewrite_type(self, rewrite_type):
        """Sets the rewrite_type of this OriginRewriteActionForAddCdnDomainInput.


        :param rewrite_type: The rewrite_type of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501
        :type: str
        """

        self._rewrite_type = rewrite_type

    @property
    def source_path(self):
        """Gets the source_path of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501


        :return: The source_path of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501
        :rtype: str
        """
        return self._source_path

    @source_path.setter
    def source_path(self, source_path):
        """Sets the source_path of this OriginRewriteActionForAddCdnDomainInput.


        :param source_path: The source_path of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501
        :type: str
        """

        self._source_path = source_path

    @property
    def target_path(self):
        """Gets the target_path of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501


        :return: The target_path of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501
        :rtype: str
        """
        return self._target_path

    @target_path.setter
    def target_path(self, target_path):
        """Sets the target_path of this OriginRewriteActionForAddCdnDomainInput.


        :param target_path: The target_path of this OriginRewriteActionForAddCdnDomainInput.  # noqa: E501
        :type: str
        """

        self._target_path = target_path

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
        if issubclass(OriginRewriteActionForAddCdnDomainInput, dict):
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
        if not isinstance(other, OriginRewriteActionForAddCdnDomainInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OriginRewriteActionForAddCdnDomainInput):
            return True

        return self.to_dict() != other.to_dict()
