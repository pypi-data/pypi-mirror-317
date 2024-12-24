# coding: utf-8

"""
    advdefence

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ConfListForBatchUpdHostRuleInput(object):
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
        'all_ssl_cipher': 'int',
        'back_up_status': 'int',
        'chunk_mode': 'int',
        'client_max_body_size': 'int',
        'def_ip': 'list[str]',
        'gzip_mode': 'int',
        'host': 'str',
        'http2': 'int',
        'keep_alive_requests': 'int',
        'keep_alive_time_out': 'int',
        'lb_algorithm': 'str',
        'labels': 'list[str]',
        'proto_follow': 'int',
        'protocols': 'list[str]',
        'proxy_connect_time_out': 'int',
        'proxy_keep_alive_requests': 'int',
        'proxy_keep_alive_time_out': 'int',
        'proxy_read_time_out': 'int',
        'proxy_retry': 'int',
        'proxy_send_time_out': 'int',
        'proxy_set_header': 'list[ProxySetHeaderForBatchUpdHostRuleInput]',
        'ssl_ciphers': 'list[str]',
        'ssl_protocols': 'list[str]',
        'servers': 'list[ServerForBatchUpdHostRuleInput]',
        'tls_enable': 'int',
        'user_cert_id': 'str'
    }

    attribute_map = {
        'all_ssl_cipher': 'AllSSLCipher',
        'back_up_status': 'BackUpStatus',
        'chunk_mode': 'ChunkMode',
        'client_max_body_size': 'ClientMaxBodySize',
        'def_ip': 'DefIp',
        'gzip_mode': 'GzipMode',
        'host': 'Host',
        'http2': 'Http2',
        'keep_alive_requests': 'KeepAliveRequests',
        'keep_alive_time_out': 'KeepAliveTimeOut',
        'lb_algorithm': 'LBAlgorithm',
        'labels': 'Labels',
        'proto_follow': 'ProtoFollow',
        'protocols': 'Protocols',
        'proxy_connect_time_out': 'ProxyConnectTimeOut',
        'proxy_keep_alive_requests': 'ProxyKeepAliveRequests',
        'proxy_keep_alive_time_out': 'ProxyKeepAliveTimeOut',
        'proxy_read_time_out': 'ProxyReadTimeOut',
        'proxy_retry': 'ProxyRetry',
        'proxy_send_time_out': 'ProxySendTimeOut',
        'proxy_set_header': 'ProxySetHeader',
        'ssl_ciphers': 'SSLCiphers',
        'ssl_protocols': 'SSLProtocols',
        'servers': 'Servers',
        'tls_enable': 'TLSEnable',
        'user_cert_id': 'UserCertId'
    }

    def __init__(self, all_ssl_cipher=None, back_up_status=None, chunk_mode=None, client_max_body_size=None, def_ip=None, gzip_mode=None, host=None, http2=None, keep_alive_requests=None, keep_alive_time_out=None, lb_algorithm=None, labels=None, proto_follow=None, protocols=None, proxy_connect_time_out=None, proxy_keep_alive_requests=None, proxy_keep_alive_time_out=None, proxy_read_time_out=None, proxy_retry=None, proxy_send_time_out=None, proxy_set_header=None, ssl_ciphers=None, ssl_protocols=None, servers=None, tls_enable=None, user_cert_id=None, _configuration=None):  # noqa: E501
        """ConfListForBatchUpdHostRuleInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._all_ssl_cipher = None
        self._back_up_status = None
        self._chunk_mode = None
        self._client_max_body_size = None
        self._def_ip = None
        self._gzip_mode = None
        self._host = None
        self._http2 = None
        self._keep_alive_requests = None
        self._keep_alive_time_out = None
        self._lb_algorithm = None
        self._labels = None
        self._proto_follow = None
        self._protocols = None
        self._proxy_connect_time_out = None
        self._proxy_keep_alive_requests = None
        self._proxy_keep_alive_time_out = None
        self._proxy_read_time_out = None
        self._proxy_retry = None
        self._proxy_send_time_out = None
        self._proxy_set_header = None
        self._ssl_ciphers = None
        self._ssl_protocols = None
        self._servers = None
        self._tls_enable = None
        self._user_cert_id = None
        self.discriminator = None

        if all_ssl_cipher is not None:
            self.all_ssl_cipher = all_ssl_cipher
        if back_up_status is not None:
            self.back_up_status = back_up_status
        if chunk_mode is not None:
            self.chunk_mode = chunk_mode
        if client_max_body_size is not None:
            self.client_max_body_size = client_max_body_size
        if def_ip is not None:
            self.def_ip = def_ip
        if gzip_mode is not None:
            self.gzip_mode = gzip_mode
        if host is not None:
            self.host = host
        if http2 is not None:
            self.http2 = http2
        if keep_alive_requests is not None:
            self.keep_alive_requests = keep_alive_requests
        if keep_alive_time_out is not None:
            self.keep_alive_time_out = keep_alive_time_out
        if lb_algorithm is not None:
            self.lb_algorithm = lb_algorithm
        if labels is not None:
            self.labels = labels
        if proto_follow is not None:
            self.proto_follow = proto_follow
        if protocols is not None:
            self.protocols = protocols
        if proxy_connect_time_out is not None:
            self.proxy_connect_time_out = proxy_connect_time_out
        if proxy_keep_alive_requests is not None:
            self.proxy_keep_alive_requests = proxy_keep_alive_requests
        if proxy_keep_alive_time_out is not None:
            self.proxy_keep_alive_time_out = proxy_keep_alive_time_out
        if proxy_read_time_out is not None:
            self.proxy_read_time_out = proxy_read_time_out
        if proxy_retry is not None:
            self.proxy_retry = proxy_retry
        if proxy_send_time_out is not None:
            self.proxy_send_time_out = proxy_send_time_out
        if proxy_set_header is not None:
            self.proxy_set_header = proxy_set_header
        if ssl_ciphers is not None:
            self.ssl_ciphers = ssl_ciphers
        if ssl_protocols is not None:
            self.ssl_protocols = ssl_protocols
        if servers is not None:
            self.servers = servers
        if tls_enable is not None:
            self.tls_enable = tls_enable
        if user_cert_id is not None:
            self.user_cert_id = user_cert_id

    @property
    def all_ssl_cipher(self):
        """Gets the all_ssl_cipher of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The all_ssl_cipher of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._all_ssl_cipher

    @all_ssl_cipher.setter
    def all_ssl_cipher(self, all_ssl_cipher):
        """Sets the all_ssl_cipher of this ConfListForBatchUpdHostRuleInput.


        :param all_ssl_cipher: The all_ssl_cipher of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._all_ssl_cipher = all_ssl_cipher

    @property
    def back_up_status(self):
        """Gets the back_up_status of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The back_up_status of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._back_up_status

    @back_up_status.setter
    def back_up_status(self, back_up_status):
        """Sets the back_up_status of this ConfListForBatchUpdHostRuleInput.


        :param back_up_status: The back_up_status of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._back_up_status = back_up_status

    @property
    def chunk_mode(self):
        """Gets the chunk_mode of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The chunk_mode of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._chunk_mode

    @chunk_mode.setter
    def chunk_mode(self, chunk_mode):
        """Sets the chunk_mode of this ConfListForBatchUpdHostRuleInput.


        :param chunk_mode: The chunk_mode of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._chunk_mode = chunk_mode

    @property
    def client_max_body_size(self):
        """Gets the client_max_body_size of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The client_max_body_size of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._client_max_body_size

    @client_max_body_size.setter
    def client_max_body_size(self, client_max_body_size):
        """Sets the client_max_body_size of this ConfListForBatchUpdHostRuleInput.


        :param client_max_body_size: The client_max_body_size of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._client_max_body_size = client_max_body_size

    @property
    def def_ip(self):
        """Gets the def_ip of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The def_ip of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._def_ip

    @def_ip.setter
    def def_ip(self, def_ip):
        """Sets the def_ip of this ConfListForBatchUpdHostRuleInput.


        :param def_ip: The def_ip of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: list[str]
        """

        self._def_ip = def_ip

    @property
    def gzip_mode(self):
        """Gets the gzip_mode of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The gzip_mode of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._gzip_mode

    @gzip_mode.setter
    def gzip_mode(self, gzip_mode):
        """Sets the gzip_mode of this ConfListForBatchUpdHostRuleInput.


        :param gzip_mode: The gzip_mode of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._gzip_mode = gzip_mode

    @property
    def host(self):
        """Gets the host of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The host of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this ConfListForBatchUpdHostRuleInput.


        :param host: The host of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: str
        """

        self._host = host

    @property
    def http2(self):
        """Gets the http2 of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The http2 of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._http2

    @http2.setter
    def http2(self, http2):
        """Sets the http2 of this ConfListForBatchUpdHostRuleInput.


        :param http2: The http2 of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._http2 = http2

    @property
    def keep_alive_requests(self):
        """Gets the keep_alive_requests of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The keep_alive_requests of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._keep_alive_requests

    @keep_alive_requests.setter
    def keep_alive_requests(self, keep_alive_requests):
        """Sets the keep_alive_requests of this ConfListForBatchUpdHostRuleInput.


        :param keep_alive_requests: The keep_alive_requests of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._keep_alive_requests = keep_alive_requests

    @property
    def keep_alive_time_out(self):
        """Gets the keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._keep_alive_time_out

    @keep_alive_time_out.setter
    def keep_alive_time_out(self, keep_alive_time_out):
        """Sets the keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.


        :param keep_alive_time_out: The keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._keep_alive_time_out = keep_alive_time_out

    @property
    def lb_algorithm(self):
        """Gets the lb_algorithm of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The lb_algorithm of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: str
        """
        return self._lb_algorithm

    @lb_algorithm.setter
    def lb_algorithm(self, lb_algorithm):
        """Sets the lb_algorithm of this ConfListForBatchUpdHostRuleInput.


        :param lb_algorithm: The lb_algorithm of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: str
        """

        self._lb_algorithm = lb_algorithm

    @property
    def labels(self):
        """Gets the labels of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The labels of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this ConfListForBatchUpdHostRuleInput.


        :param labels: The labels of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def proto_follow(self):
        """Gets the proto_follow of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proto_follow of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._proto_follow

    @proto_follow.setter
    def proto_follow(self, proto_follow):
        """Sets the proto_follow of this ConfListForBatchUpdHostRuleInput.


        :param proto_follow: The proto_follow of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._proto_follow = proto_follow

    @property
    def protocols(self):
        """Gets the protocols of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The protocols of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._protocols

    @protocols.setter
    def protocols(self, protocols):
        """Sets the protocols of this ConfListForBatchUpdHostRuleInput.


        :param protocols: The protocols of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: list[str]
        """

        self._protocols = protocols

    @property
    def proxy_connect_time_out(self):
        """Gets the proxy_connect_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proxy_connect_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._proxy_connect_time_out

    @proxy_connect_time_out.setter
    def proxy_connect_time_out(self, proxy_connect_time_out):
        """Sets the proxy_connect_time_out of this ConfListForBatchUpdHostRuleInput.


        :param proxy_connect_time_out: The proxy_connect_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._proxy_connect_time_out = proxy_connect_time_out

    @property
    def proxy_keep_alive_requests(self):
        """Gets the proxy_keep_alive_requests of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proxy_keep_alive_requests of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._proxy_keep_alive_requests

    @proxy_keep_alive_requests.setter
    def proxy_keep_alive_requests(self, proxy_keep_alive_requests):
        """Sets the proxy_keep_alive_requests of this ConfListForBatchUpdHostRuleInput.


        :param proxy_keep_alive_requests: The proxy_keep_alive_requests of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._proxy_keep_alive_requests = proxy_keep_alive_requests

    @property
    def proxy_keep_alive_time_out(self):
        """Gets the proxy_keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proxy_keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._proxy_keep_alive_time_out

    @proxy_keep_alive_time_out.setter
    def proxy_keep_alive_time_out(self, proxy_keep_alive_time_out):
        """Sets the proxy_keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.


        :param proxy_keep_alive_time_out: The proxy_keep_alive_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._proxy_keep_alive_time_out = proxy_keep_alive_time_out

    @property
    def proxy_read_time_out(self):
        """Gets the proxy_read_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proxy_read_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._proxy_read_time_out

    @proxy_read_time_out.setter
    def proxy_read_time_out(self, proxy_read_time_out):
        """Sets the proxy_read_time_out of this ConfListForBatchUpdHostRuleInput.


        :param proxy_read_time_out: The proxy_read_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._proxy_read_time_out = proxy_read_time_out

    @property
    def proxy_retry(self):
        """Gets the proxy_retry of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proxy_retry of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._proxy_retry

    @proxy_retry.setter
    def proxy_retry(self, proxy_retry):
        """Sets the proxy_retry of this ConfListForBatchUpdHostRuleInput.


        :param proxy_retry: The proxy_retry of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._proxy_retry = proxy_retry

    @property
    def proxy_send_time_out(self):
        """Gets the proxy_send_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proxy_send_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._proxy_send_time_out

    @proxy_send_time_out.setter
    def proxy_send_time_out(self, proxy_send_time_out):
        """Sets the proxy_send_time_out of this ConfListForBatchUpdHostRuleInput.


        :param proxy_send_time_out: The proxy_send_time_out of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._proxy_send_time_out = proxy_send_time_out

    @property
    def proxy_set_header(self):
        """Gets the proxy_set_header of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The proxy_set_header of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: list[ProxySetHeaderForBatchUpdHostRuleInput]
        """
        return self._proxy_set_header

    @proxy_set_header.setter
    def proxy_set_header(self, proxy_set_header):
        """Sets the proxy_set_header of this ConfListForBatchUpdHostRuleInput.


        :param proxy_set_header: The proxy_set_header of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: list[ProxySetHeaderForBatchUpdHostRuleInput]
        """

        self._proxy_set_header = proxy_set_header

    @property
    def ssl_ciphers(self):
        """Gets the ssl_ciphers of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The ssl_ciphers of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._ssl_ciphers

    @ssl_ciphers.setter
    def ssl_ciphers(self, ssl_ciphers):
        """Sets the ssl_ciphers of this ConfListForBatchUpdHostRuleInput.


        :param ssl_ciphers: The ssl_ciphers of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: list[str]
        """

        self._ssl_ciphers = ssl_ciphers

    @property
    def ssl_protocols(self):
        """Gets the ssl_protocols of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The ssl_protocols of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._ssl_protocols

    @ssl_protocols.setter
    def ssl_protocols(self, ssl_protocols):
        """Sets the ssl_protocols of this ConfListForBatchUpdHostRuleInput.


        :param ssl_protocols: The ssl_protocols of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: list[str]
        """

        self._ssl_protocols = ssl_protocols

    @property
    def servers(self):
        """Gets the servers of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The servers of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: list[ServerForBatchUpdHostRuleInput]
        """
        return self._servers

    @servers.setter
    def servers(self, servers):
        """Sets the servers of this ConfListForBatchUpdHostRuleInput.


        :param servers: The servers of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: list[ServerForBatchUpdHostRuleInput]
        """

        self._servers = servers

    @property
    def tls_enable(self):
        """Gets the tls_enable of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The tls_enable of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: int
        """
        return self._tls_enable

    @tls_enable.setter
    def tls_enable(self, tls_enable):
        """Sets the tls_enable of this ConfListForBatchUpdHostRuleInput.


        :param tls_enable: The tls_enable of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: int
        """

        self._tls_enable = tls_enable

    @property
    def user_cert_id(self):
        """Gets the user_cert_id of this ConfListForBatchUpdHostRuleInput.  # noqa: E501


        :return: The user_cert_id of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :rtype: str
        """
        return self._user_cert_id

    @user_cert_id.setter
    def user_cert_id(self, user_cert_id):
        """Sets the user_cert_id of this ConfListForBatchUpdHostRuleInput.


        :param user_cert_id: The user_cert_id of this ConfListForBatchUpdHostRuleInput.  # noqa: E501
        :type: str
        """

        self._user_cert_id = user_cert_id

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
        if issubclass(ConfListForBatchUpdHostRuleInput, dict):
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
        if not isinstance(other, ConfListForBatchUpdHostRuleInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConfListForBatchUpdHostRuleInput):
            return True

        return self.to_dict() != other.to_dict()
