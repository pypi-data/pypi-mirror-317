# coding: utf-8

"""
    vpc

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateIpAddressPoolRequest(object):
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
        'cidr_block': 'str',
        'cidr_mask': 'int',
        'client_token': 'str',
        'description': 'str',
        'isp': 'str',
        'name': 'str',
        'project_name': 'str',
        'tags': 'list[TagForCreateIpAddressPoolInput]'
    }

    attribute_map = {
        'cidr_block': 'CidrBlock',
        'cidr_mask': 'CidrMask',
        'client_token': 'ClientToken',
        'description': 'Description',
        'isp': 'ISP',
        'name': 'Name',
        'project_name': 'ProjectName',
        'tags': 'Tags'
    }

    def __init__(self, cidr_block=None, cidr_mask=None, client_token=None, description=None, isp=None, name=None, project_name=None, tags=None, _configuration=None):  # noqa: E501
        """CreateIpAddressPoolRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cidr_block = None
        self._cidr_mask = None
        self._client_token = None
        self._description = None
        self._isp = None
        self._name = None
        self._project_name = None
        self._tags = None
        self.discriminator = None

        if cidr_block is not None:
            self.cidr_block = cidr_block
        if cidr_mask is not None:
            self.cidr_mask = cidr_mask
        if client_token is not None:
            self.client_token = client_token
        if description is not None:
            self.description = description
        self.isp = isp
        if name is not None:
            self.name = name
        if project_name is not None:
            self.project_name = project_name
        if tags is not None:
            self.tags = tags

    @property
    def cidr_block(self):
        """Gets the cidr_block of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The cidr_block of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: str
        """
        return self._cidr_block

    @cidr_block.setter
    def cidr_block(self, cidr_block):
        """Sets the cidr_block of this CreateIpAddressPoolRequest.


        :param cidr_block: The cidr_block of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: str
        """

        self._cidr_block = cidr_block

    @property
    def cidr_mask(self):
        """Gets the cidr_mask of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The cidr_mask of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: int
        """
        return self._cidr_mask

    @cidr_mask.setter
    def cidr_mask(self, cidr_mask):
        """Sets the cidr_mask of this CreateIpAddressPoolRequest.


        :param cidr_mask: The cidr_mask of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: int
        """

        self._cidr_mask = cidr_mask

    @property
    def client_token(self):
        """Gets the client_token of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The client_token of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this CreateIpAddressPoolRequest.


        :param client_token: The client_token of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def description(self):
        """Gets the description of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The description of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateIpAddressPoolRequest.


        :param description: The description of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def isp(self):
        """Gets the isp of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The isp of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: str
        """
        return self._isp

    @isp.setter
    def isp(self, isp):
        """Sets the isp of this CreateIpAddressPoolRequest.


        :param isp: The isp of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and isp is None:
            raise ValueError("Invalid value for `isp`, must not be `None`")  # noqa: E501

        self._isp = isp

    @property
    def name(self):
        """Gets the name of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The name of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateIpAddressPoolRequest.


        :param name: The name of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def project_name(self):
        """Gets the project_name of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The project_name of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this CreateIpAddressPoolRequest.


        :param project_name: The project_name of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def tags(self):
        """Gets the tags of this CreateIpAddressPoolRequest.  # noqa: E501


        :return: The tags of this CreateIpAddressPoolRequest.  # noqa: E501
        :rtype: list[TagForCreateIpAddressPoolInput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateIpAddressPoolRequest.


        :param tags: The tags of this CreateIpAddressPoolRequest.  # noqa: E501
        :type: list[TagForCreateIpAddressPoolInput]
        """

        self._tags = tags

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
        if issubclass(CreateIpAddressPoolRequest, dict):
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
        if not isinstance(other, CreateIpAddressPoolRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateIpAddressPoolRequest):
            return True

        return self.to_dict() != other.to_dict()
