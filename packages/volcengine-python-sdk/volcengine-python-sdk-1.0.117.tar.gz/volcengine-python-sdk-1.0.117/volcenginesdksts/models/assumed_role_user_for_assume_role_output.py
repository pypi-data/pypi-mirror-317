# coding: utf-8

"""
    sts

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class AssumedRoleUserForAssumeRoleOutput(object):
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
        'assumed_role_id': 'str',
        'trn': 'str'
    }

    attribute_map = {
        'assumed_role_id': 'AssumedRoleId',
        'trn': 'Trn'
    }

    def __init__(self, assumed_role_id=None, trn=None, _configuration=None):  # noqa: E501
        """AssumedRoleUserForAssumeRoleOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._assumed_role_id = None
        self._trn = None
        self.discriminator = None

        if assumed_role_id is not None:
            self.assumed_role_id = assumed_role_id
        if trn is not None:
            self.trn = trn

    @property
    def assumed_role_id(self):
        """Gets the assumed_role_id of this AssumedRoleUserForAssumeRoleOutput.  # noqa: E501


        :return: The assumed_role_id of this AssumedRoleUserForAssumeRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._assumed_role_id

    @assumed_role_id.setter
    def assumed_role_id(self, assumed_role_id):
        """Sets the assumed_role_id of this AssumedRoleUserForAssumeRoleOutput.


        :param assumed_role_id: The assumed_role_id of this AssumedRoleUserForAssumeRoleOutput.  # noqa: E501
        :type: str
        """

        self._assumed_role_id = assumed_role_id

    @property
    def trn(self):
        """Gets the trn of this AssumedRoleUserForAssumeRoleOutput.  # noqa: E501


        :return: The trn of this AssumedRoleUserForAssumeRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._trn

    @trn.setter
    def trn(self, trn):
        """Sets the trn of this AssumedRoleUserForAssumeRoleOutput.


        :param trn: The trn of this AssumedRoleUserForAssumeRoleOutput.  # noqa: E501
        :type: str
        """

        self._trn = trn

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
        if issubclass(AssumedRoleUserForAssumeRoleOutput, dict):
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
        if not isinstance(other, AssumedRoleUserForAssumeRoleOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AssumedRoleUserForAssumeRoleOutput):
            return True

        return self.to_dict() != other.to_dict()
