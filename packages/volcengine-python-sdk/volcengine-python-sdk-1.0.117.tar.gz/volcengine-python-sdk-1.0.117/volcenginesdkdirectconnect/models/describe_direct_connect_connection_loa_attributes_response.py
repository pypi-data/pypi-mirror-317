# coding: utf-8

"""
    directconnect

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeDirectConnectConnectionLoaAttributesResponse(object):
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
        'bandwidth': 'int',
        'company_name': 'str',
        'construction_time': 'str',
        'direct_connect_connection_id': 'str',
        'engineers': 'list[EngineerForDescribeDirectConnectConnectionLoaAttributesOutput]',
        'line_type': 'str',
        'loa_content': 'str',
        'loa_content_type': 'str',
        'peer_location': 'str',
        'request_id': 'str',
        'system_integrator': 'str'
    }

    attribute_map = {
        'bandwidth': 'Bandwidth',
        'company_name': 'CompanyName',
        'construction_time': 'ConstructionTime',
        'direct_connect_connection_id': 'DirectConnectConnectionId',
        'engineers': 'Engineers',
        'line_type': 'LineType',
        'loa_content': 'LoaContent',
        'loa_content_type': 'LoaContentType',
        'peer_location': 'PeerLocation',
        'request_id': 'RequestId',
        'system_integrator': 'SystemIntegrator'
    }

    def __init__(self, bandwidth=None, company_name=None, construction_time=None, direct_connect_connection_id=None, engineers=None, line_type=None, loa_content=None, loa_content_type=None, peer_location=None, request_id=None, system_integrator=None, _configuration=None):  # noqa: E501
        """DescribeDirectConnectConnectionLoaAttributesResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._bandwidth = None
        self._company_name = None
        self._construction_time = None
        self._direct_connect_connection_id = None
        self._engineers = None
        self._line_type = None
        self._loa_content = None
        self._loa_content_type = None
        self._peer_location = None
        self._request_id = None
        self._system_integrator = None
        self.discriminator = None

        if bandwidth is not None:
            self.bandwidth = bandwidth
        if company_name is not None:
            self.company_name = company_name
        if construction_time is not None:
            self.construction_time = construction_time
        if direct_connect_connection_id is not None:
            self.direct_connect_connection_id = direct_connect_connection_id
        if engineers is not None:
            self.engineers = engineers
        if line_type is not None:
            self.line_type = line_type
        if loa_content is not None:
            self.loa_content = loa_content
        if loa_content_type is not None:
            self.loa_content_type = loa_content_type
        if peer_location is not None:
            self.peer_location = peer_location
        if request_id is not None:
            self.request_id = request_id
        if system_integrator is not None:
            self.system_integrator = system_integrator

    @property
    def bandwidth(self):
        """Gets the bandwidth of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The bandwidth of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: int
        """
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        """Sets the bandwidth of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param bandwidth: The bandwidth of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: int
        """

        self._bandwidth = bandwidth

    @property
    def company_name(self):
        """Gets the company_name of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The company_name of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        """Sets the company_name of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param company_name: The company_name of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._company_name = company_name

    @property
    def construction_time(self):
        """Gets the construction_time of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The construction_time of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._construction_time

    @construction_time.setter
    def construction_time(self, construction_time):
        """Sets the construction_time of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param construction_time: The construction_time of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._construction_time = construction_time

    @property
    def direct_connect_connection_id(self):
        """Gets the direct_connect_connection_id of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The direct_connect_connection_id of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._direct_connect_connection_id

    @direct_connect_connection_id.setter
    def direct_connect_connection_id(self, direct_connect_connection_id):
        """Sets the direct_connect_connection_id of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param direct_connect_connection_id: The direct_connect_connection_id of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._direct_connect_connection_id = direct_connect_connection_id

    @property
    def engineers(self):
        """Gets the engineers of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The engineers of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: list[EngineerForDescribeDirectConnectConnectionLoaAttributesOutput]
        """
        return self._engineers

    @engineers.setter
    def engineers(self, engineers):
        """Sets the engineers of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param engineers: The engineers of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: list[EngineerForDescribeDirectConnectConnectionLoaAttributesOutput]
        """

        self._engineers = engineers

    @property
    def line_type(self):
        """Gets the line_type of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The line_type of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._line_type

    @line_type.setter
    def line_type(self, line_type):
        """Sets the line_type of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param line_type: The line_type of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._line_type = line_type

    @property
    def loa_content(self):
        """Gets the loa_content of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The loa_content of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._loa_content

    @loa_content.setter
    def loa_content(self, loa_content):
        """Sets the loa_content of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param loa_content: The loa_content of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._loa_content = loa_content

    @property
    def loa_content_type(self):
        """Gets the loa_content_type of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The loa_content_type of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._loa_content_type

    @loa_content_type.setter
    def loa_content_type(self, loa_content_type):
        """Sets the loa_content_type of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param loa_content_type: The loa_content_type of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._loa_content_type = loa_content_type

    @property
    def peer_location(self):
        """Gets the peer_location of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The peer_location of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._peer_location

    @peer_location.setter
    def peer_location(self, peer_location):
        """Sets the peer_location of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param peer_location: The peer_location of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._peer_location = peer_location

    @property
    def request_id(self):
        """Gets the request_id of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The request_id of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param request_id: The request_id of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def system_integrator(self):
        """Gets the system_integrator of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501


        :return: The system_integrator of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._system_integrator

    @system_integrator.setter
    def system_integrator(self, system_integrator):
        """Sets the system_integrator of this DescribeDirectConnectConnectionLoaAttributesResponse.


        :param system_integrator: The system_integrator of this DescribeDirectConnectConnectionLoaAttributesResponse.  # noqa: E501
        :type: str
        """

        self._system_integrator = system_integrator

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
        if issubclass(DescribeDirectConnectConnectionLoaAttributesResponse, dict):
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
        if not isinstance(other, DescribeDirectConnectConnectionLoaAttributesResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeDirectConnectConnectionLoaAttributesResponse):
            return True

        return self.to_dict() != other.to_dict()
