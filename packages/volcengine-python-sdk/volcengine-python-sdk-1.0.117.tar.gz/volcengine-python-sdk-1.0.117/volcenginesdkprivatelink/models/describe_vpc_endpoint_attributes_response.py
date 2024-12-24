# coding: utf-8

"""
    privatelink

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeVpcEndpointAttributesResponse(object):
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
        'business_status': 'str',
        'connection_status': 'str',
        'creation_time': 'str',
        'deleted_time': 'str',
        'description': 'str',
        'endpoint': 'EndpointForDescribeVpcEndpointAttributesOutput',
        'endpoint_domain': 'str',
        'endpoint_id': 'str',
        'endpoint_index': 'int',
        'endpoint_name': 'str',
        'endpoint_type': 'str',
        'ip_address_versions': 'list[str]',
        'ip_address_versions_n': 'list[str]',
        'payer': 'str',
        'private_dns_enabled': 'bool',
        'private_dns_name': 'str',
        'project_name': 'str',
        'request_id': 'str',
        'service_id': 'str',
        'service_managed': 'bool',
        'service_name': 'str',
        'status': 'str',
        'tags': 'list[TagForDescribeVpcEndpointAttributesOutput]',
        'update_time': 'str',
        'vpc_id': 'str'
    }

    attribute_map = {
        'business_status': 'BusinessStatus',
        'connection_status': 'ConnectionStatus',
        'creation_time': 'CreationTime',
        'deleted_time': 'DeletedTime',
        'description': 'Description',
        'endpoint': 'Endpoint',
        'endpoint_domain': 'EndpointDomain',
        'endpoint_id': 'EndpointId',
        'endpoint_index': 'EndpointIndex',
        'endpoint_name': 'EndpointName',
        'endpoint_type': 'EndpointType',
        'ip_address_versions': 'IpAddressVersions',
        'ip_address_versions_n': 'IpAddressVersions.N',
        'payer': 'Payer',
        'private_dns_enabled': 'PrivateDNSEnabled',
        'private_dns_name': 'PrivateDNSName',
        'project_name': 'ProjectName',
        'request_id': 'RequestId',
        'service_id': 'ServiceId',
        'service_managed': 'ServiceManaged',
        'service_name': 'ServiceName',
        'status': 'Status',
        'tags': 'Tags',
        'update_time': 'UpdateTime',
        'vpc_id': 'VpcId'
    }

    def __init__(self, business_status=None, connection_status=None, creation_time=None, deleted_time=None, description=None, endpoint=None, endpoint_domain=None, endpoint_id=None, endpoint_index=None, endpoint_name=None, endpoint_type=None, ip_address_versions=None, ip_address_versions_n=None, payer=None, private_dns_enabled=None, private_dns_name=None, project_name=None, request_id=None, service_id=None, service_managed=None, service_name=None, status=None, tags=None, update_time=None, vpc_id=None, _configuration=None):  # noqa: E501
        """DescribeVpcEndpointAttributesResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._business_status = None
        self._connection_status = None
        self._creation_time = None
        self._deleted_time = None
        self._description = None
        self._endpoint = None
        self._endpoint_domain = None
        self._endpoint_id = None
        self._endpoint_index = None
        self._endpoint_name = None
        self._endpoint_type = None
        self._ip_address_versions = None
        self._ip_address_versions_n = None
        self._payer = None
        self._private_dns_enabled = None
        self._private_dns_name = None
        self._project_name = None
        self._request_id = None
        self._service_id = None
        self._service_managed = None
        self._service_name = None
        self._status = None
        self._tags = None
        self._update_time = None
        self._vpc_id = None
        self.discriminator = None

        if business_status is not None:
            self.business_status = business_status
        if connection_status is not None:
            self.connection_status = connection_status
        if creation_time is not None:
            self.creation_time = creation_time
        if deleted_time is not None:
            self.deleted_time = deleted_time
        if description is not None:
            self.description = description
        if endpoint is not None:
            self.endpoint = endpoint
        if endpoint_domain is not None:
            self.endpoint_domain = endpoint_domain
        if endpoint_id is not None:
            self.endpoint_id = endpoint_id
        if endpoint_index is not None:
            self.endpoint_index = endpoint_index
        if endpoint_name is not None:
            self.endpoint_name = endpoint_name
        if endpoint_type is not None:
            self.endpoint_type = endpoint_type
        if ip_address_versions is not None:
            self.ip_address_versions = ip_address_versions
        if ip_address_versions_n is not None:
            self.ip_address_versions_n = ip_address_versions_n
        if payer is not None:
            self.payer = payer
        if private_dns_enabled is not None:
            self.private_dns_enabled = private_dns_enabled
        if private_dns_name is not None:
            self.private_dns_name = private_dns_name
        if project_name is not None:
            self.project_name = project_name
        if request_id is not None:
            self.request_id = request_id
        if service_id is not None:
            self.service_id = service_id
        if service_managed is not None:
            self.service_managed = service_managed
        if service_name is not None:
            self.service_name = service_name
        if status is not None:
            self.status = status
        if tags is not None:
            self.tags = tags
        if update_time is not None:
            self.update_time = update_time
        if vpc_id is not None:
            self.vpc_id = vpc_id

    @property
    def business_status(self):
        """Gets the business_status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The business_status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_status

    @business_status.setter
    def business_status(self, business_status):
        """Sets the business_status of this DescribeVpcEndpointAttributesResponse.


        :param business_status: The business_status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._business_status = business_status

    @property
    def connection_status(self):
        """Gets the connection_status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The connection_status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._connection_status

    @connection_status.setter
    def connection_status(self, connection_status):
        """Sets the connection_status of this DescribeVpcEndpointAttributesResponse.


        :param connection_status: The connection_status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._connection_status = connection_status

    @property
    def creation_time(self):
        """Gets the creation_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The creation_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """Sets the creation_time of this DescribeVpcEndpointAttributesResponse.


        :param creation_time: The creation_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._creation_time = creation_time

    @property
    def deleted_time(self):
        """Gets the deleted_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The deleted_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._deleted_time

    @deleted_time.setter
    def deleted_time(self, deleted_time):
        """Sets the deleted_time of this DescribeVpcEndpointAttributesResponse.


        :param deleted_time: The deleted_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._deleted_time = deleted_time

    @property
    def description(self):
        """Gets the description of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The description of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this DescribeVpcEndpointAttributesResponse.


        :param description: The description of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def endpoint(self):
        """Gets the endpoint of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The endpoint of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: EndpointForDescribeVpcEndpointAttributesOutput
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """Sets the endpoint of this DescribeVpcEndpointAttributesResponse.


        :param endpoint: The endpoint of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: EndpointForDescribeVpcEndpointAttributesOutput
        """

        self._endpoint = endpoint

    @property
    def endpoint_domain(self):
        """Gets the endpoint_domain of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The endpoint_domain of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_domain

    @endpoint_domain.setter
    def endpoint_domain(self, endpoint_domain):
        """Sets the endpoint_domain of this DescribeVpcEndpointAttributesResponse.


        :param endpoint_domain: The endpoint_domain of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._endpoint_domain = endpoint_domain

    @property
    def endpoint_id(self):
        """Gets the endpoint_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The endpoint_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, endpoint_id):
        """Sets the endpoint_id of this DescribeVpcEndpointAttributesResponse.


        :param endpoint_id: The endpoint_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._endpoint_id = endpoint_id

    @property
    def endpoint_index(self):
        """Gets the endpoint_index of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The endpoint_index of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: int
        """
        return self._endpoint_index

    @endpoint_index.setter
    def endpoint_index(self, endpoint_index):
        """Sets the endpoint_index of this DescribeVpcEndpointAttributesResponse.


        :param endpoint_index: The endpoint_index of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: int
        """

        self._endpoint_index = endpoint_index

    @property
    def endpoint_name(self):
        """Gets the endpoint_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The endpoint_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_name

    @endpoint_name.setter
    def endpoint_name(self, endpoint_name):
        """Sets the endpoint_name of this DescribeVpcEndpointAttributesResponse.


        :param endpoint_name: The endpoint_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._endpoint_name = endpoint_name

    @property
    def endpoint_type(self):
        """Gets the endpoint_type of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The endpoint_type of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_type

    @endpoint_type.setter
    def endpoint_type(self, endpoint_type):
        """Sets the endpoint_type of this DescribeVpcEndpointAttributesResponse.


        :param endpoint_type: The endpoint_type of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._endpoint_type = endpoint_type

    @property
    def ip_address_versions(self):
        """Gets the ip_address_versions of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The ip_address_versions of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._ip_address_versions

    @ip_address_versions.setter
    def ip_address_versions(self, ip_address_versions):
        """Sets the ip_address_versions of this DescribeVpcEndpointAttributesResponse.


        :param ip_address_versions: The ip_address_versions of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: list[str]
        """

        self._ip_address_versions = ip_address_versions

    @property
    def ip_address_versions_n(self):
        """Gets the ip_address_versions_n of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The ip_address_versions_n of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._ip_address_versions_n

    @ip_address_versions_n.setter
    def ip_address_versions_n(self, ip_address_versions_n):
        """Sets the ip_address_versions_n of this DescribeVpcEndpointAttributesResponse.


        :param ip_address_versions_n: The ip_address_versions_n of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: list[str]
        """

        self._ip_address_versions_n = ip_address_versions_n

    @property
    def payer(self):
        """Gets the payer of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The payer of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._payer

    @payer.setter
    def payer(self, payer):
        """Sets the payer of this DescribeVpcEndpointAttributesResponse.


        :param payer: The payer of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._payer = payer

    @property
    def private_dns_enabled(self):
        """Gets the private_dns_enabled of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The private_dns_enabled of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: bool
        """
        return self._private_dns_enabled

    @private_dns_enabled.setter
    def private_dns_enabled(self, private_dns_enabled):
        """Sets the private_dns_enabled of this DescribeVpcEndpointAttributesResponse.


        :param private_dns_enabled: The private_dns_enabled of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: bool
        """

        self._private_dns_enabled = private_dns_enabled

    @property
    def private_dns_name(self):
        """Gets the private_dns_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The private_dns_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._private_dns_name

    @private_dns_name.setter
    def private_dns_name(self, private_dns_name):
        """Sets the private_dns_name of this DescribeVpcEndpointAttributesResponse.


        :param private_dns_name: The private_dns_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._private_dns_name = private_dns_name

    @property
    def project_name(self):
        """Gets the project_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The project_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this DescribeVpcEndpointAttributesResponse.


        :param project_name: The project_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def request_id(self):
        """Gets the request_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The request_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this DescribeVpcEndpointAttributesResponse.


        :param request_id: The request_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def service_id(self):
        """Gets the service_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The service_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id):
        """Sets the service_id of this DescribeVpcEndpointAttributesResponse.


        :param service_id: The service_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._service_id = service_id

    @property
    def service_managed(self):
        """Gets the service_managed of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The service_managed of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: bool
        """
        return self._service_managed

    @service_managed.setter
    def service_managed(self, service_managed):
        """Sets the service_managed of this DescribeVpcEndpointAttributesResponse.


        :param service_managed: The service_managed of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: bool
        """

        self._service_managed = service_managed

    @property
    def service_name(self):
        """Gets the service_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The service_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """Sets the service_name of this DescribeVpcEndpointAttributesResponse.


        :param service_name: The service_name of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._service_name = service_name

    @property
    def status(self):
        """Gets the status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DescribeVpcEndpointAttributesResponse.


        :param status: The status of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def tags(self):
        """Gets the tags of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The tags of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: list[TagForDescribeVpcEndpointAttributesOutput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this DescribeVpcEndpointAttributesResponse.


        :param tags: The tags of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: list[TagForDescribeVpcEndpointAttributesOutput]
        """

        self._tags = tags

    @property
    def update_time(self):
        """Gets the update_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The update_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this DescribeVpcEndpointAttributesResponse.


        :param update_time: The update_time of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._update_time = update_time

    @property
    def vpc_id(self):
        """Gets the vpc_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501


        :return: The vpc_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this DescribeVpcEndpointAttributesResponse.


        :param vpc_id: The vpc_id of this DescribeVpcEndpointAttributesResponse.  # noqa: E501
        :type: str
        """

        self._vpc_id = vpc_id

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
        if issubclass(DescribeVpcEndpointAttributesResponse, dict):
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
        if not isinstance(other, DescribeVpcEndpointAttributesResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeVpcEndpointAttributesResponse):
            return True

        return self.to_dict() != other.to_dict()
