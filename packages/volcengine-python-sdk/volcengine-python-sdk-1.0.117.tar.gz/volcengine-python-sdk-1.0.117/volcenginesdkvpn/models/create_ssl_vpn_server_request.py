# coding: utf-8

"""
    vpn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateSslVpnServerRequest(object):
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
        'auth': 'str',
        'cipher': 'str',
        'client_ip_pool': 'str',
        'client_token': 'str',
        'compress': 'bool',
        'description': 'str',
        'local_subnets': 'list[str]',
        'port': 'int',
        'project_name': 'str',
        'protocol': 'str',
        'ssl_vpn_server_name': 'str',
        'vpn_gateway_id': 'str'
    }

    attribute_map = {
        'auth': 'Auth',
        'cipher': 'Cipher',
        'client_ip_pool': 'ClientIpPool',
        'client_token': 'ClientToken',
        'compress': 'Compress',
        'description': 'Description',
        'local_subnets': 'LocalSubnets',
        'port': 'Port',
        'project_name': 'ProjectName',
        'protocol': 'Protocol',
        'ssl_vpn_server_name': 'SslVpnServerName',
        'vpn_gateway_id': 'VpnGatewayId'
    }

    def __init__(self, auth=None, cipher=None, client_ip_pool=None, client_token=None, compress=None, description=None, local_subnets=None, port=None, project_name=None, protocol=None, ssl_vpn_server_name=None, vpn_gateway_id=None, _configuration=None):  # noqa: E501
        """CreateSslVpnServerRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._auth = None
        self._cipher = None
        self._client_ip_pool = None
        self._client_token = None
        self._compress = None
        self._description = None
        self._local_subnets = None
        self._port = None
        self._project_name = None
        self._protocol = None
        self._ssl_vpn_server_name = None
        self._vpn_gateway_id = None
        self.discriminator = None

        if auth is not None:
            self.auth = auth
        if cipher is not None:
            self.cipher = cipher
        self.client_ip_pool = client_ip_pool
        if client_token is not None:
            self.client_token = client_token
        if compress is not None:
            self.compress = compress
        if description is not None:
            self.description = description
        if local_subnets is not None:
            self.local_subnets = local_subnets
        if port is not None:
            self.port = port
        if project_name is not None:
            self.project_name = project_name
        if protocol is not None:
            self.protocol = protocol
        if ssl_vpn_server_name is not None:
            self.ssl_vpn_server_name = ssl_vpn_server_name
        self.vpn_gateway_id = vpn_gateway_id

    @property
    def auth(self):
        """Gets the auth of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The auth of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._auth

    @auth.setter
    def auth(self, auth):
        """Sets the auth of this CreateSslVpnServerRequest.


        :param auth: The auth of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """

        self._auth = auth

    @property
    def cipher(self):
        """Gets the cipher of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The cipher of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._cipher

    @cipher.setter
    def cipher(self, cipher):
        """Sets the cipher of this CreateSslVpnServerRequest.


        :param cipher: The cipher of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """

        self._cipher = cipher

    @property
    def client_ip_pool(self):
        """Gets the client_ip_pool of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The client_ip_pool of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_ip_pool

    @client_ip_pool.setter
    def client_ip_pool(self, client_ip_pool):
        """Sets the client_ip_pool of this CreateSslVpnServerRequest.


        :param client_ip_pool: The client_ip_pool of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and client_ip_pool is None:
            raise ValueError("Invalid value for `client_ip_pool`, must not be `None`")  # noqa: E501

        self._client_ip_pool = client_ip_pool

    @property
    def client_token(self):
        """Gets the client_token of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The client_token of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this CreateSslVpnServerRequest.


        :param client_token: The client_token of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def compress(self):
        """Gets the compress of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The compress of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: bool
        """
        return self._compress

    @compress.setter
    def compress(self, compress):
        """Sets the compress of this CreateSslVpnServerRequest.


        :param compress: The compress of this CreateSslVpnServerRequest.  # noqa: E501
        :type: bool
        """

        self._compress = compress

    @property
    def description(self):
        """Gets the description of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The description of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateSslVpnServerRequest.


        :param description: The description of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def local_subnets(self):
        """Gets the local_subnets of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The local_subnets of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._local_subnets

    @local_subnets.setter
    def local_subnets(self, local_subnets):
        """Sets the local_subnets of this CreateSslVpnServerRequest.


        :param local_subnets: The local_subnets of this CreateSslVpnServerRequest.  # noqa: E501
        :type: list[str]
        """

        self._local_subnets = local_subnets

    @property
    def port(self):
        """Gets the port of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The port of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this CreateSslVpnServerRequest.


        :param port: The port of this CreateSslVpnServerRequest.  # noqa: E501
        :type: int
        """

        self._port = port

    @property
    def project_name(self):
        """Gets the project_name of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The project_name of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this CreateSslVpnServerRequest.


        :param project_name: The project_name of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def protocol(self):
        """Gets the protocol of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The protocol of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """Sets the protocol of this CreateSslVpnServerRequest.


        :param protocol: The protocol of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """

        self._protocol = protocol

    @property
    def ssl_vpn_server_name(self):
        """Gets the ssl_vpn_server_name of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The ssl_vpn_server_name of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._ssl_vpn_server_name

    @ssl_vpn_server_name.setter
    def ssl_vpn_server_name(self, ssl_vpn_server_name):
        """Sets the ssl_vpn_server_name of this CreateSslVpnServerRequest.


        :param ssl_vpn_server_name: The ssl_vpn_server_name of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """

        self._ssl_vpn_server_name = ssl_vpn_server_name

    @property
    def vpn_gateway_id(self):
        """Gets the vpn_gateway_id of this CreateSslVpnServerRequest.  # noqa: E501


        :return: The vpn_gateway_id of this CreateSslVpnServerRequest.  # noqa: E501
        :rtype: str
        """
        return self._vpn_gateway_id

    @vpn_gateway_id.setter
    def vpn_gateway_id(self, vpn_gateway_id):
        """Sets the vpn_gateway_id of this CreateSslVpnServerRequest.


        :param vpn_gateway_id: The vpn_gateway_id of this CreateSslVpnServerRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and vpn_gateway_id is None:
            raise ValueError("Invalid value for `vpn_gateway_id`, must not be `None`")  # noqa: E501

        self._vpn_gateway_id = vpn_gateway_id

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
        if issubclass(CreateSslVpnServerRequest, dict):
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
        if not isinstance(other, CreateSslVpnServerRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateSslVpnServerRequest):
            return True

        return self.to_dict() != other.to_dict()
