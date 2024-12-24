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


class AuthorizeSecurityGroupIngressRequest(object):
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
        'cidr_ip': 'str',
        'client_token': 'str',
        'description': 'str',
        'policy': 'str',
        'port_end': 'int',
        'port_start': 'int',
        'prefix_list_id': 'str',
        'priority': 'int',
        'protocol': 'str',
        'security_group_id': 'str',
        'source_group_id': 'str'
    }

    attribute_map = {
        'cidr_ip': 'CidrIp',
        'client_token': 'ClientToken',
        'description': 'Description',
        'policy': 'Policy',
        'port_end': 'PortEnd',
        'port_start': 'PortStart',
        'prefix_list_id': 'PrefixListId',
        'priority': 'Priority',
        'protocol': 'Protocol',
        'security_group_id': 'SecurityGroupId',
        'source_group_id': 'SourceGroupId'
    }

    def __init__(self, cidr_ip=None, client_token=None, description=None, policy=None, port_end=None, port_start=None, prefix_list_id=None, priority=None, protocol=None, security_group_id=None, source_group_id=None, _configuration=None):  # noqa: E501
        """AuthorizeSecurityGroupIngressRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cidr_ip = None
        self._client_token = None
        self._description = None
        self._policy = None
        self._port_end = None
        self._port_start = None
        self._prefix_list_id = None
        self._priority = None
        self._protocol = None
        self._security_group_id = None
        self._source_group_id = None
        self.discriminator = None

        if cidr_ip is not None:
            self.cidr_ip = cidr_ip
        if client_token is not None:
            self.client_token = client_token
        if description is not None:
            self.description = description
        if policy is not None:
            self.policy = policy
        self.port_end = port_end
        self.port_start = port_start
        if prefix_list_id is not None:
            self.prefix_list_id = prefix_list_id
        if priority is not None:
            self.priority = priority
        self.protocol = protocol
        self.security_group_id = security_group_id
        if source_group_id is not None:
            self.source_group_id = source_group_id

    @property
    def cidr_ip(self):
        """Gets the cidr_ip of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The cidr_ip of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._cidr_ip

    @cidr_ip.setter
    def cidr_ip(self, cidr_ip):
        """Sets the cidr_ip of this AuthorizeSecurityGroupIngressRequest.


        :param cidr_ip: The cidr_ip of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """

        self._cidr_ip = cidr_ip

    @property
    def client_token(self):
        """Gets the client_token of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The client_token of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this AuthorizeSecurityGroupIngressRequest.


        :param client_token: The client_token of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def description(self):
        """Gets the description of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The description of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AuthorizeSecurityGroupIngressRequest.


        :param description: The description of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def policy(self):
        """Gets the policy of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The policy of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """Sets the policy of this AuthorizeSecurityGroupIngressRequest.


        :param policy: The policy of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """

        self._policy = policy

    @property
    def port_end(self):
        """Gets the port_end of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The port_end of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: int
        """
        return self._port_end

    @port_end.setter
    def port_end(self, port_end):
        """Sets the port_end of this AuthorizeSecurityGroupIngressRequest.


        :param port_end: The port_end of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and port_end is None:
            raise ValueError("Invalid value for `port_end`, must not be `None`")  # noqa: E501

        self._port_end = port_end

    @property
    def port_start(self):
        """Gets the port_start of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The port_start of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: int
        """
        return self._port_start

    @port_start.setter
    def port_start(self, port_start):
        """Sets the port_start of this AuthorizeSecurityGroupIngressRequest.


        :param port_start: The port_start of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and port_start is None:
            raise ValueError("Invalid value for `port_start`, must not be `None`")  # noqa: E501

        self._port_start = port_start

    @property
    def prefix_list_id(self):
        """Gets the prefix_list_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The prefix_list_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._prefix_list_id

    @prefix_list_id.setter
    def prefix_list_id(self, prefix_list_id):
        """Sets the prefix_list_id of this AuthorizeSecurityGroupIngressRequest.


        :param prefix_list_id: The prefix_list_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """

        self._prefix_list_id = prefix_list_id

    @property
    def priority(self):
        """Gets the priority of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The priority of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this AuthorizeSecurityGroupIngressRequest.


        :param priority: The priority of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def protocol(self):
        """Gets the protocol of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The protocol of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """Sets the protocol of this AuthorizeSecurityGroupIngressRequest.


        :param protocol: The protocol of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and protocol is None:
            raise ValueError("Invalid value for `protocol`, must not be `None`")  # noqa: E501

        self._protocol = protocol

    @property
    def security_group_id(self):
        """Gets the security_group_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The security_group_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._security_group_id

    @security_group_id.setter
    def security_group_id(self, security_group_id):
        """Sets the security_group_id of this AuthorizeSecurityGroupIngressRequest.


        :param security_group_id: The security_group_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and security_group_id is None:
            raise ValueError("Invalid value for `security_group_id`, must not be `None`")  # noqa: E501

        self._security_group_id = security_group_id

    @property
    def source_group_id(self):
        """Gets the source_group_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501


        :return: The source_group_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :rtype: str
        """
        return self._source_group_id

    @source_group_id.setter
    def source_group_id(self, source_group_id):
        """Sets the source_group_id of this AuthorizeSecurityGroupIngressRequest.


        :param source_group_id: The source_group_id of this AuthorizeSecurityGroupIngressRequest.  # noqa: E501
        :type: str
        """

        self._source_group_id = source_group_id

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
        if issubclass(AuthorizeSecurityGroupIngressRequest, dict):
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
        if not isinstance(other, AuthorizeSecurityGroupIngressRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AuthorizeSecurityGroupIngressRequest):
            return True

        return self.to_dict() != other.to_dict()
