# coding: utf-8

"""
    waf

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class UpdateHostGroupRequest(object):
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
        'description': 'str',
        'host_group_id': 'int',
        'host_list': 'list[str]',
        'name': 'str',
        'project_name': 'str'
    }

    attribute_map = {
        'action': 'Action',
        'description': 'Description',
        'host_group_id': 'HostGroupID',
        'host_list': 'HostList',
        'name': 'Name',
        'project_name': 'ProjectName'
    }

    def __init__(self, action=None, description=None, host_group_id=None, host_list=None, name=None, project_name=None, _configuration=None):  # noqa: E501
        """UpdateHostGroupRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._action = None
        self._description = None
        self._host_group_id = None
        self._host_list = None
        self._name = None
        self._project_name = None
        self.discriminator = None

        if action is not None:
            self.action = action
        if description is not None:
            self.description = description
        self.host_group_id = host_group_id
        if host_list is not None:
            self.host_list = host_list
        if name is not None:
            self.name = name
        if project_name is not None:
            self.project_name = project_name

    @property
    def action(self):
        """Gets the action of this UpdateHostGroupRequest.  # noqa: E501


        :return: The action of this UpdateHostGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this UpdateHostGroupRequest.


        :param action: The action of this UpdateHostGroupRequest.  # noqa: E501
        :type: str
        """

        self._action = action

    @property
    def description(self):
        """Gets the description of this UpdateHostGroupRequest.  # noqa: E501


        :return: The description of this UpdateHostGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateHostGroupRequest.


        :param description: The description of this UpdateHostGroupRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def host_group_id(self):
        """Gets the host_group_id of this UpdateHostGroupRequest.  # noqa: E501


        :return: The host_group_id of this UpdateHostGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._host_group_id

    @host_group_id.setter
    def host_group_id(self, host_group_id):
        """Sets the host_group_id of this UpdateHostGroupRequest.


        :param host_group_id: The host_group_id of this UpdateHostGroupRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and host_group_id is None:
            raise ValueError("Invalid value for `host_group_id`, must not be `None`")  # noqa: E501

        self._host_group_id = host_group_id

    @property
    def host_list(self):
        """Gets the host_list of this UpdateHostGroupRequest.  # noqa: E501


        :return: The host_list of this UpdateHostGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._host_list

    @host_list.setter
    def host_list(self, host_list):
        """Sets the host_list of this UpdateHostGroupRequest.


        :param host_list: The host_list of this UpdateHostGroupRequest.  # noqa: E501
        :type: list[str]
        """

        self._host_list = host_list

    @property
    def name(self):
        """Gets the name of this UpdateHostGroupRequest.  # noqa: E501


        :return: The name of this UpdateHostGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateHostGroupRequest.


        :param name: The name of this UpdateHostGroupRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def project_name(self):
        """Gets the project_name of this UpdateHostGroupRequest.  # noqa: E501


        :return: The project_name of this UpdateHostGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this UpdateHostGroupRequest.


        :param project_name: The project_name of this UpdateHostGroupRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

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
        if issubclass(UpdateHostGroupRequest, dict):
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
        if not isinstance(other, UpdateHostGroupRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateHostGroupRequest):
            return True

        return self.to_dict() != other.to_dict()
