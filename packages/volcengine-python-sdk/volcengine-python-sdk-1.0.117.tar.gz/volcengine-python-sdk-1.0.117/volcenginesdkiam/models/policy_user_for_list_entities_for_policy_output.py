# coding: utf-8

"""
    iam

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class PolicyUserForListEntitiesForPolicyOutput(object):
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
        'attach_date': 'str',
        'description': 'str',
        'display_name': 'str',
        'id': 'int',
        'policy_scope': 'list[PolicyScopeForListEntitiesForPolicyOutput]',
        'user_name': 'str'
    }

    attribute_map = {
        'attach_date': 'AttachDate',
        'description': 'Description',
        'display_name': 'DisplayName',
        'id': 'Id',
        'policy_scope': 'PolicyScope',
        'user_name': 'UserName'
    }

    def __init__(self, attach_date=None, description=None, display_name=None, id=None, policy_scope=None, user_name=None, _configuration=None):  # noqa: E501
        """PolicyUserForListEntitiesForPolicyOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._attach_date = None
        self._description = None
        self._display_name = None
        self._id = None
        self._policy_scope = None
        self._user_name = None
        self.discriminator = None

        if attach_date is not None:
            self.attach_date = attach_date
        if description is not None:
            self.description = description
        if display_name is not None:
            self.display_name = display_name
        if id is not None:
            self.id = id
        if policy_scope is not None:
            self.policy_scope = policy_scope
        if user_name is not None:
            self.user_name = user_name

    @property
    def attach_date(self):
        """Gets the attach_date of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501


        :return: The attach_date of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :rtype: str
        """
        return self._attach_date

    @attach_date.setter
    def attach_date(self, attach_date):
        """Sets the attach_date of this PolicyUserForListEntitiesForPolicyOutput.


        :param attach_date: The attach_date of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :type: str
        """

        self._attach_date = attach_date

    @property
    def description(self):
        """Gets the description of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501


        :return: The description of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PolicyUserForListEntitiesForPolicyOutput.


        :param description: The description of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501


        :return: The display_name of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this PolicyUserForListEntitiesForPolicyOutput.


        :param display_name: The display_name of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def id(self):
        """Gets the id of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501


        :return: The id of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PolicyUserForListEntitiesForPolicyOutput.


        :param id: The id of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def policy_scope(self):
        """Gets the policy_scope of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501


        :return: The policy_scope of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :rtype: list[PolicyScopeForListEntitiesForPolicyOutput]
        """
        return self._policy_scope

    @policy_scope.setter
    def policy_scope(self, policy_scope):
        """Sets the policy_scope of this PolicyUserForListEntitiesForPolicyOutput.


        :param policy_scope: The policy_scope of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :type: list[PolicyScopeForListEntitiesForPolicyOutput]
        """

        self._policy_scope = policy_scope

    @property
    def user_name(self):
        """Gets the user_name of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501


        :return: The user_name of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """Sets the user_name of this PolicyUserForListEntitiesForPolicyOutput.


        :param user_name: The user_name of this PolicyUserForListEntitiesForPolicyOutput.  # noqa: E501
        :type: str
        """

        self._user_name = user_name

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
        if issubclass(PolicyUserForListEntitiesForPolicyOutput, dict):
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
        if not isinstance(other, PolicyUserForListEntitiesForPolicyOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PolicyUserForListEntitiesForPolicyOutput):
            return True

        return self.to_dict() != other.to_dict()
