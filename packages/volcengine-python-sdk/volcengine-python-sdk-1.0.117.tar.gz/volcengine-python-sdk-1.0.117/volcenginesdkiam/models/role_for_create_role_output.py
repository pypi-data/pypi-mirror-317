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


class RoleForCreateRoleOutput(object):
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
        'create_date': 'str',
        'description': 'str',
        'display_name': 'str',
        'is_service_linked_role': 'int',
        'max_session_duration': 'int',
        'role_id': 'int',
        'role_name': 'str',
        'trn': 'str',
        'trust_policy_document': 'str',
        'update_date': 'str'
    }

    attribute_map = {
        'create_date': 'CreateDate',
        'description': 'Description',
        'display_name': 'DisplayName',
        'is_service_linked_role': 'IsServiceLinkedRole',
        'max_session_duration': 'MaxSessionDuration',
        'role_id': 'RoleId',
        'role_name': 'RoleName',
        'trn': 'Trn',
        'trust_policy_document': 'TrustPolicyDocument',
        'update_date': 'UpdateDate'
    }

    def __init__(self, create_date=None, description=None, display_name=None, is_service_linked_role=None, max_session_duration=None, role_id=None, role_name=None, trn=None, trust_policy_document=None, update_date=None, _configuration=None):  # noqa: E501
        """RoleForCreateRoleOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._create_date = None
        self._description = None
        self._display_name = None
        self._is_service_linked_role = None
        self._max_session_duration = None
        self._role_id = None
        self._role_name = None
        self._trn = None
        self._trust_policy_document = None
        self._update_date = None
        self.discriminator = None

        if create_date is not None:
            self.create_date = create_date
        if description is not None:
            self.description = description
        if display_name is not None:
            self.display_name = display_name
        if is_service_linked_role is not None:
            self.is_service_linked_role = is_service_linked_role
        if max_session_duration is not None:
            self.max_session_duration = max_session_duration
        if role_id is not None:
            self.role_id = role_id
        if role_name is not None:
            self.role_name = role_name
        if trn is not None:
            self.trn = trn
        if trust_policy_document is not None:
            self.trust_policy_document = trust_policy_document
        if update_date is not None:
            self.update_date = update_date

    @property
    def create_date(self):
        """Gets the create_date of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The create_date of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        """Sets the create_date of this RoleForCreateRoleOutput.


        :param create_date: The create_date of this RoleForCreateRoleOutput.  # noqa: E501
        :type: str
        """

        self._create_date = create_date

    @property
    def description(self):
        """Gets the description of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The description of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RoleForCreateRoleOutput.


        :param description: The description of this RoleForCreateRoleOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The display_name of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this RoleForCreateRoleOutput.


        :param display_name: The display_name of this RoleForCreateRoleOutput.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def is_service_linked_role(self):
        """Gets the is_service_linked_role of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The is_service_linked_role of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: int
        """
        return self._is_service_linked_role

    @is_service_linked_role.setter
    def is_service_linked_role(self, is_service_linked_role):
        """Sets the is_service_linked_role of this RoleForCreateRoleOutput.


        :param is_service_linked_role: The is_service_linked_role of this RoleForCreateRoleOutput.  # noqa: E501
        :type: int
        """

        self._is_service_linked_role = is_service_linked_role

    @property
    def max_session_duration(self):
        """Gets the max_session_duration of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The max_session_duration of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: int
        """
        return self._max_session_duration

    @max_session_duration.setter
    def max_session_duration(self, max_session_duration):
        """Sets the max_session_duration of this RoleForCreateRoleOutput.


        :param max_session_duration: The max_session_duration of this RoleForCreateRoleOutput.  # noqa: E501
        :type: int
        """

        self._max_session_duration = max_session_duration

    @property
    def role_id(self):
        """Gets the role_id of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The role_id of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: int
        """
        return self._role_id

    @role_id.setter
    def role_id(self, role_id):
        """Sets the role_id of this RoleForCreateRoleOutput.


        :param role_id: The role_id of this RoleForCreateRoleOutput.  # noqa: E501
        :type: int
        """

        self._role_id = role_id

    @property
    def role_name(self):
        """Gets the role_name of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The role_name of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._role_name

    @role_name.setter
    def role_name(self, role_name):
        """Sets the role_name of this RoleForCreateRoleOutput.


        :param role_name: The role_name of this RoleForCreateRoleOutput.  # noqa: E501
        :type: str
        """

        self._role_name = role_name

    @property
    def trn(self):
        """Gets the trn of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The trn of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._trn

    @trn.setter
    def trn(self, trn):
        """Sets the trn of this RoleForCreateRoleOutput.


        :param trn: The trn of this RoleForCreateRoleOutput.  # noqa: E501
        :type: str
        """

        self._trn = trn

    @property
    def trust_policy_document(self):
        """Gets the trust_policy_document of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The trust_policy_document of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._trust_policy_document

    @trust_policy_document.setter
    def trust_policy_document(self, trust_policy_document):
        """Sets the trust_policy_document of this RoleForCreateRoleOutput.


        :param trust_policy_document: The trust_policy_document of this RoleForCreateRoleOutput.  # noqa: E501
        :type: str
        """

        self._trust_policy_document = trust_policy_document

    @property
    def update_date(self):
        """Gets the update_date of this RoleForCreateRoleOutput.  # noqa: E501


        :return: The update_date of this RoleForCreateRoleOutput.  # noqa: E501
        :rtype: str
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this RoleForCreateRoleOutput.


        :param update_date: The update_date of this RoleForCreateRoleOutput.  # noqa: E501
        :type: str
        """

        self._update_date = update_date

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
        if issubclass(RoleForCreateRoleOutput, dict):
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
        if not isinstance(other, RoleForCreateRoleOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RoleForCreateRoleOutput):
            return True

        return self.to_dict() != other.to_dict()
