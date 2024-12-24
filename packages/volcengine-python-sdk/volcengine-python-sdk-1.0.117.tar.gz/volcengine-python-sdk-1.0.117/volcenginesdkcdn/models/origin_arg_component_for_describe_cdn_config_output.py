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


class OriginArgComponentForDescribeCdnConfigOutput(object):
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
        'action': 'str',
        'object': 'str',
        'subobject': 'str'
    }

    attribute_map = {
        'action': 'Action',
        'object': 'Object',
        'subobject': 'Subobject'
    }

    def __init__(self, action=None, object=None, subobject=None, _configuration=None):  # noqa: E501
        """OriginArgComponentForDescribeCdnConfigOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._action = None
        self._object = None
        self._subobject = None
        self.discriminator = None

        if action is not None:
            self.action = action
        if object is not None:
            self.object = object
        if subobject is not None:
            self.subobject = subobject

    @property
    def action(self):
        """Gets the action of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501


        :return: The action of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this OriginArgComponentForDescribeCdnConfigOutput.


        :param action: The action of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501
        :type: str
        """

        self._action = action

    @property
    def object(self):
        """Gets the object of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501


        :return: The object of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this OriginArgComponentForDescribeCdnConfigOutput.


        :param object: The object of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501
        :type: str
        """

        self._object = object

    @property
    def subobject(self):
        """Gets the subobject of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501


        :return: The subobject of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._subobject

    @subobject.setter
    def subobject(self, subobject):
        """Sets the subobject of this OriginArgComponentForDescribeCdnConfigOutput.


        :param subobject: The subobject of this OriginArgComponentForDescribeCdnConfigOutput.  # noqa: E501
        :type: str
        """

        self._subobject = subobject

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
        if issubclass(OriginArgComponentForDescribeCdnConfigOutput, dict):
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
        if not isinstance(other, OriginArgComponentForDescribeCdnConfigOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OriginArgComponentForDescribeCdnConfigOutput):
            return True

        return self.to_dict() != other.to_dict()
