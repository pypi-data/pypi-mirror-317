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


class ListIpGroupRequest(object):
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
        'ip': 'str',
        'ip_group_id': 'int',
        'list_all': 'str',
        'page': 'int',
        'page_size': 'int',
        'project_name': 'str'
    }

    attribute_map = {
        'ip': 'Ip',
        'ip_group_id': 'IpGroupId',
        'list_all': 'ListAll',
        'page': 'Page',
        'page_size': 'PageSize',
        'project_name': 'ProjectName'
    }

    def __init__(self, ip=None, ip_group_id=None, list_all=None, page=None, page_size=None, project_name=None, _configuration=None):  # noqa: E501
        """ListIpGroupRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._ip = None
        self._ip_group_id = None
        self._list_all = None
        self._page = None
        self._page_size = None
        self._project_name = None
        self.discriminator = None

        if ip is not None:
            self.ip = ip
        self.ip_group_id = ip_group_id
        if list_all is not None:
            self.list_all = list_all
        self.page = page
        self.page_size = page_size
        if project_name is not None:
            self.project_name = project_name

    @property
    def ip(self):
        """Gets the ip of this ListIpGroupRequest.  # noqa: E501


        :return: The ip of this ListIpGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this ListIpGroupRequest.


        :param ip: The ip of this ListIpGroupRequest.  # noqa: E501
        :type: str
        """

        self._ip = ip

    @property
    def ip_group_id(self):
        """Gets the ip_group_id of this ListIpGroupRequest.  # noqa: E501


        :return: The ip_group_id of this ListIpGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._ip_group_id

    @ip_group_id.setter
    def ip_group_id(self, ip_group_id):
        """Sets the ip_group_id of this ListIpGroupRequest.


        :param ip_group_id: The ip_group_id of this ListIpGroupRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and ip_group_id is None:
            raise ValueError("Invalid value for `ip_group_id`, must not be `None`")  # noqa: E501

        self._ip_group_id = ip_group_id

    @property
    def list_all(self):
        """Gets the list_all of this ListIpGroupRequest.  # noqa: E501


        :return: The list_all of this ListIpGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._list_all

    @list_all.setter
    def list_all(self, list_all):
        """Sets the list_all of this ListIpGroupRequest.


        :param list_all: The list_all of this ListIpGroupRequest.  # noqa: E501
        :type: str
        """

        self._list_all = list_all

    @property
    def page(self):
        """Gets the page of this ListIpGroupRequest.  # noqa: E501


        :return: The page of this ListIpGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this ListIpGroupRequest.


        :param page: The page of this ListIpGroupRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and page is None:
            raise ValueError("Invalid value for `page`, must not be `None`")  # noqa: E501

        self._page = page

    @property
    def page_size(self):
        """Gets the page_size of this ListIpGroupRequest.  # noqa: E501


        :return: The page_size of this ListIpGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this ListIpGroupRequest.


        :param page_size: The page_size of this ListIpGroupRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and page_size is None:
            raise ValueError("Invalid value for `page_size`, must not be `None`")  # noqa: E501

        self._page_size = page_size

    @property
    def project_name(self):
        """Gets the project_name of this ListIpGroupRequest.  # noqa: E501


        :return: The project_name of this ListIpGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this ListIpGroupRequest.


        :param project_name: The project_name of this ListIpGroupRequest.  # noqa: E501
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
        if issubclass(ListIpGroupRequest, dict):
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
        if not isinstance(other, ListIpGroupRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ListIpGroupRequest):
            return True

        return self.to_dict() != other.to_dict()
