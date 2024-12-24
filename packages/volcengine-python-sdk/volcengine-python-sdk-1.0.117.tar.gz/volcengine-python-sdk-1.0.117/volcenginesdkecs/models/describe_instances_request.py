# coding: utf-8

"""
    ecs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeInstancesRequest(object):
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
        'dedicated_host_cluster_id': 'str',
        'dedicated_host_id': 'str',
        'deployment_set_group_numbers': 'list[int]',
        'deployment_set_ids': 'list[str]',
        'eip_addresses': 'list[str]',
        'hpc_cluster_id': 'str',
        'instance_charge_type': 'str',
        'instance_ids': 'list[str]',
        'instance_name': 'str',
        'instance_type_families': 'list[str]',
        'instance_type_ids': 'list[str]',
        'instance_types': 'list[str]',
        'ipv6_addresses': 'list[str]',
        'key_pair_name': 'str',
        'max_results': 'int',
        'next_token': 'str',
        'primary_ip_address': 'str',
        'project_name': 'str',
        'scheduled_instance_id': 'str',
        'status': 'str',
        'tag_filters': 'list[TagFilterForDescribeInstancesInput]',
        'vpc_id': 'str',
        'zone_id': 'str'
    }

    attribute_map = {
        'dedicated_host_cluster_id': 'DedicatedHostClusterId',
        'dedicated_host_id': 'DedicatedHostId',
        'deployment_set_group_numbers': 'DeploymentSetGroupNumbers',
        'deployment_set_ids': 'DeploymentSetIds',
        'eip_addresses': 'EipAddresses',
        'hpc_cluster_id': 'HpcClusterId',
        'instance_charge_type': 'InstanceChargeType',
        'instance_ids': 'InstanceIds',
        'instance_name': 'InstanceName',
        'instance_type_families': 'InstanceTypeFamilies',
        'instance_type_ids': 'InstanceTypeIds',
        'instance_types': 'InstanceTypes',
        'ipv6_addresses': 'Ipv6Addresses',
        'key_pair_name': 'KeyPairName',
        'max_results': 'MaxResults',
        'next_token': 'NextToken',
        'primary_ip_address': 'PrimaryIpAddress',
        'project_name': 'ProjectName',
        'scheduled_instance_id': 'ScheduledInstanceId',
        'status': 'Status',
        'tag_filters': 'TagFilters',
        'vpc_id': 'VpcId',
        'zone_id': 'ZoneId'
    }

    def __init__(self, dedicated_host_cluster_id=None, dedicated_host_id=None, deployment_set_group_numbers=None, deployment_set_ids=None, eip_addresses=None, hpc_cluster_id=None, instance_charge_type=None, instance_ids=None, instance_name=None, instance_type_families=None, instance_type_ids=None, instance_types=None, ipv6_addresses=None, key_pair_name=None, max_results=None, next_token=None, primary_ip_address=None, project_name=None, scheduled_instance_id=None, status=None, tag_filters=None, vpc_id=None, zone_id=None, _configuration=None):  # noqa: E501
        """DescribeInstancesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._dedicated_host_cluster_id = None
        self._dedicated_host_id = None
        self._deployment_set_group_numbers = None
        self._deployment_set_ids = None
        self._eip_addresses = None
        self._hpc_cluster_id = None
        self._instance_charge_type = None
        self._instance_ids = None
        self._instance_name = None
        self._instance_type_families = None
        self._instance_type_ids = None
        self._instance_types = None
        self._ipv6_addresses = None
        self._key_pair_name = None
        self._max_results = None
        self._next_token = None
        self._primary_ip_address = None
        self._project_name = None
        self._scheduled_instance_id = None
        self._status = None
        self._tag_filters = None
        self._vpc_id = None
        self._zone_id = None
        self.discriminator = None

        if dedicated_host_cluster_id is not None:
            self.dedicated_host_cluster_id = dedicated_host_cluster_id
        if dedicated_host_id is not None:
            self.dedicated_host_id = dedicated_host_id
        if deployment_set_group_numbers is not None:
            self.deployment_set_group_numbers = deployment_set_group_numbers
        if deployment_set_ids is not None:
            self.deployment_set_ids = deployment_set_ids
        if eip_addresses is not None:
            self.eip_addresses = eip_addresses
        if hpc_cluster_id is not None:
            self.hpc_cluster_id = hpc_cluster_id
        if instance_charge_type is not None:
            self.instance_charge_type = instance_charge_type
        if instance_ids is not None:
            self.instance_ids = instance_ids
        if instance_name is not None:
            self.instance_name = instance_name
        if instance_type_families is not None:
            self.instance_type_families = instance_type_families
        if instance_type_ids is not None:
            self.instance_type_ids = instance_type_ids
        if instance_types is not None:
            self.instance_types = instance_types
        if ipv6_addresses is not None:
            self.ipv6_addresses = ipv6_addresses
        if key_pair_name is not None:
            self.key_pair_name = key_pair_name
        if max_results is not None:
            self.max_results = max_results
        if next_token is not None:
            self.next_token = next_token
        if primary_ip_address is not None:
            self.primary_ip_address = primary_ip_address
        if project_name is not None:
            self.project_name = project_name
        if scheduled_instance_id is not None:
            self.scheduled_instance_id = scheduled_instance_id
        if status is not None:
            self.status = status
        if tag_filters is not None:
            self.tag_filters = tag_filters
        if vpc_id is not None:
            self.vpc_id = vpc_id
        if zone_id is not None:
            self.zone_id = zone_id

    @property
    def dedicated_host_cluster_id(self):
        """Gets the dedicated_host_cluster_id of this DescribeInstancesRequest.  # noqa: E501


        :return: The dedicated_host_cluster_id of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._dedicated_host_cluster_id

    @dedicated_host_cluster_id.setter
    def dedicated_host_cluster_id(self, dedicated_host_cluster_id):
        """Sets the dedicated_host_cluster_id of this DescribeInstancesRequest.


        :param dedicated_host_cluster_id: The dedicated_host_cluster_id of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._dedicated_host_cluster_id = dedicated_host_cluster_id

    @property
    def dedicated_host_id(self):
        """Gets the dedicated_host_id of this DescribeInstancesRequest.  # noqa: E501


        :return: The dedicated_host_id of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._dedicated_host_id

    @dedicated_host_id.setter
    def dedicated_host_id(self, dedicated_host_id):
        """Sets the dedicated_host_id of this DescribeInstancesRequest.


        :param dedicated_host_id: The dedicated_host_id of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._dedicated_host_id = dedicated_host_id

    @property
    def deployment_set_group_numbers(self):
        """Gets the deployment_set_group_numbers of this DescribeInstancesRequest.  # noqa: E501


        :return: The deployment_set_group_numbers of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[int]
        """
        return self._deployment_set_group_numbers

    @deployment_set_group_numbers.setter
    def deployment_set_group_numbers(self, deployment_set_group_numbers):
        """Sets the deployment_set_group_numbers of this DescribeInstancesRequest.


        :param deployment_set_group_numbers: The deployment_set_group_numbers of this DescribeInstancesRequest.  # noqa: E501
        :type: list[int]
        """

        self._deployment_set_group_numbers = deployment_set_group_numbers

    @property
    def deployment_set_ids(self):
        """Gets the deployment_set_ids of this DescribeInstancesRequest.  # noqa: E501


        :return: The deployment_set_ids of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._deployment_set_ids

    @deployment_set_ids.setter
    def deployment_set_ids(self, deployment_set_ids):
        """Sets the deployment_set_ids of this DescribeInstancesRequest.


        :param deployment_set_ids: The deployment_set_ids of this DescribeInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._deployment_set_ids = deployment_set_ids

    @property
    def eip_addresses(self):
        """Gets the eip_addresses of this DescribeInstancesRequest.  # noqa: E501


        :return: The eip_addresses of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._eip_addresses

    @eip_addresses.setter
    def eip_addresses(self, eip_addresses):
        """Sets the eip_addresses of this DescribeInstancesRequest.


        :param eip_addresses: The eip_addresses of this DescribeInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._eip_addresses = eip_addresses

    @property
    def hpc_cluster_id(self):
        """Gets the hpc_cluster_id of this DescribeInstancesRequest.  # noqa: E501


        :return: The hpc_cluster_id of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._hpc_cluster_id

    @hpc_cluster_id.setter
    def hpc_cluster_id(self, hpc_cluster_id):
        """Sets the hpc_cluster_id of this DescribeInstancesRequest.


        :param hpc_cluster_id: The hpc_cluster_id of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._hpc_cluster_id = hpc_cluster_id

    @property
    def instance_charge_type(self):
        """Gets the instance_charge_type of this DescribeInstancesRequest.  # noqa: E501


        :return: The instance_charge_type of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_charge_type

    @instance_charge_type.setter
    def instance_charge_type(self, instance_charge_type):
        """Sets the instance_charge_type of this DescribeInstancesRequest.


        :param instance_charge_type: The instance_charge_type of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._instance_charge_type = instance_charge_type

    @property
    def instance_ids(self):
        """Gets the instance_ids of this DescribeInstancesRequest.  # noqa: E501


        :return: The instance_ids of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_ids

    @instance_ids.setter
    def instance_ids(self, instance_ids):
        """Sets the instance_ids of this DescribeInstancesRequest.


        :param instance_ids: The instance_ids of this DescribeInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._instance_ids = instance_ids

    @property
    def instance_name(self):
        """Gets the instance_name of this DescribeInstancesRequest.  # noqa: E501


        :return: The instance_name of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """Sets the instance_name of this DescribeInstancesRequest.


        :param instance_name: The instance_name of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._instance_name = instance_name

    @property
    def instance_type_families(self):
        """Gets the instance_type_families of this DescribeInstancesRequest.  # noqa: E501


        :return: The instance_type_families of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_type_families

    @instance_type_families.setter
    def instance_type_families(self, instance_type_families):
        """Sets the instance_type_families of this DescribeInstancesRequest.


        :param instance_type_families: The instance_type_families of this DescribeInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._instance_type_families = instance_type_families

    @property
    def instance_type_ids(self):
        """Gets the instance_type_ids of this DescribeInstancesRequest.  # noqa: E501


        :return: The instance_type_ids of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_type_ids

    @instance_type_ids.setter
    def instance_type_ids(self, instance_type_ids):
        """Sets the instance_type_ids of this DescribeInstancesRequest.


        :param instance_type_ids: The instance_type_ids of this DescribeInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._instance_type_ids = instance_type_ids

    @property
    def instance_types(self):
        """Gets the instance_types of this DescribeInstancesRequest.  # noqa: E501


        :return: The instance_types of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_types

    @instance_types.setter
    def instance_types(self, instance_types):
        """Sets the instance_types of this DescribeInstancesRequest.


        :param instance_types: The instance_types of this DescribeInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._instance_types = instance_types

    @property
    def ipv6_addresses(self):
        """Gets the ipv6_addresses of this DescribeInstancesRequest.  # noqa: E501


        :return: The ipv6_addresses of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._ipv6_addresses

    @ipv6_addresses.setter
    def ipv6_addresses(self, ipv6_addresses):
        """Sets the ipv6_addresses of this DescribeInstancesRequest.


        :param ipv6_addresses: The ipv6_addresses of this DescribeInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._ipv6_addresses = ipv6_addresses

    @property
    def key_pair_name(self):
        """Gets the key_pair_name of this DescribeInstancesRequest.  # noqa: E501


        :return: The key_pair_name of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._key_pair_name

    @key_pair_name.setter
    def key_pair_name(self, key_pair_name):
        """Sets the key_pair_name of this DescribeInstancesRequest.


        :param key_pair_name: The key_pair_name of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._key_pair_name = key_pair_name

    @property
    def max_results(self):
        """Gets the max_results of this DescribeInstancesRequest.  # noqa: E501


        :return: The max_results of this DescribeInstancesRequest.  # noqa: E501
        :rtype: int
        """
        return self._max_results

    @max_results.setter
    def max_results(self, max_results):
        """Sets the max_results of this DescribeInstancesRequest.


        :param max_results: The max_results of this DescribeInstancesRequest.  # noqa: E501
        :type: int
        """

        self._max_results = max_results

    @property
    def next_token(self):
        """Gets the next_token of this DescribeInstancesRequest.  # noqa: E501


        :return: The next_token of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._next_token

    @next_token.setter
    def next_token(self, next_token):
        """Sets the next_token of this DescribeInstancesRequest.


        :param next_token: The next_token of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._next_token = next_token

    @property
    def primary_ip_address(self):
        """Gets the primary_ip_address of this DescribeInstancesRequest.  # noqa: E501


        :return: The primary_ip_address of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._primary_ip_address

    @primary_ip_address.setter
    def primary_ip_address(self, primary_ip_address):
        """Sets the primary_ip_address of this DescribeInstancesRequest.


        :param primary_ip_address: The primary_ip_address of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._primary_ip_address = primary_ip_address

    @property
    def project_name(self):
        """Gets the project_name of this DescribeInstancesRequest.  # noqa: E501


        :return: The project_name of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this DescribeInstancesRequest.


        :param project_name: The project_name of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def scheduled_instance_id(self):
        """Gets the scheduled_instance_id of this DescribeInstancesRequest.  # noqa: E501


        :return: The scheduled_instance_id of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._scheduled_instance_id

    @scheduled_instance_id.setter
    def scheduled_instance_id(self, scheduled_instance_id):
        """Sets the scheduled_instance_id of this DescribeInstancesRequest.


        :param scheduled_instance_id: The scheduled_instance_id of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._scheduled_instance_id = scheduled_instance_id

    @property
    def status(self):
        """Gets the status of this DescribeInstancesRequest.  # noqa: E501


        :return: The status of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DescribeInstancesRequest.


        :param status: The status of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def tag_filters(self):
        """Gets the tag_filters of this DescribeInstancesRequest.  # noqa: E501


        :return: The tag_filters of this DescribeInstancesRequest.  # noqa: E501
        :rtype: list[TagFilterForDescribeInstancesInput]
        """
        return self._tag_filters

    @tag_filters.setter
    def tag_filters(self, tag_filters):
        """Sets the tag_filters of this DescribeInstancesRequest.


        :param tag_filters: The tag_filters of this DescribeInstancesRequest.  # noqa: E501
        :type: list[TagFilterForDescribeInstancesInput]
        """

        self._tag_filters = tag_filters

    @property
    def vpc_id(self):
        """Gets the vpc_id of this DescribeInstancesRequest.  # noqa: E501


        :return: The vpc_id of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this DescribeInstancesRequest.


        :param vpc_id: The vpc_id of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._vpc_id = vpc_id

    @property
    def zone_id(self):
        """Gets the zone_id of this DescribeInstancesRequest.  # noqa: E501


        :return: The zone_id of this DescribeInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._zone_id

    @zone_id.setter
    def zone_id(self, zone_id):
        """Sets the zone_id of this DescribeInstancesRequest.


        :param zone_id: The zone_id of this DescribeInstancesRequest.  # noqa: E501
        :type: str
        """

        self._zone_id = zone_id

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
        if issubclass(DescribeInstancesRequest, dict):
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
        if not isinstance(other, DescribeInstancesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeInstancesRequest):
            return True

        return self.to_dict() != other.to_dict()
