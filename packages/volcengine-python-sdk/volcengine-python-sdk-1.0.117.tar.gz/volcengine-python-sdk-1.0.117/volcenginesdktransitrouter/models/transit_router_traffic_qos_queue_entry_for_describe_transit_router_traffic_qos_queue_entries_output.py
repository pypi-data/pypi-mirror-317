# coding: utf-8

"""
    transitrouter

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput(object):
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
        'bandwidth_percent': 'int',
        'creation_time': 'str',
        'description': 'str',
        'dscps': 'list[int]',
        'is_default': 'bool',
        'status': 'str',
        'transit_router_traffic_qos_queue_entry_id': 'str',
        'transit_router_traffic_qos_queue_entry_name': 'str',
        'transit_router_traffic_qos_queue_policy_id': 'str',
        'update_time': 'str'
    }

    attribute_map = {
        'bandwidth_percent': 'BandwidthPercent',
        'creation_time': 'CreationTime',
        'description': 'Description',
        'dscps': 'Dscps',
        'is_default': 'IsDefault',
        'status': 'Status',
        'transit_router_traffic_qos_queue_entry_id': 'TransitRouterTrafficQosQueueEntryId',
        'transit_router_traffic_qos_queue_entry_name': 'TransitRouterTrafficQosQueueEntryName',
        'transit_router_traffic_qos_queue_policy_id': 'TransitRouterTrafficQosQueuePolicyId',
        'update_time': 'UpdateTime'
    }

    def __init__(self, bandwidth_percent=None, creation_time=None, description=None, dscps=None, is_default=None, status=None, transit_router_traffic_qos_queue_entry_id=None, transit_router_traffic_qos_queue_entry_name=None, transit_router_traffic_qos_queue_policy_id=None, update_time=None, _configuration=None):  # noqa: E501
        """TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._bandwidth_percent = None
        self._creation_time = None
        self._description = None
        self._dscps = None
        self._is_default = None
        self._status = None
        self._transit_router_traffic_qos_queue_entry_id = None
        self._transit_router_traffic_qos_queue_entry_name = None
        self._transit_router_traffic_qos_queue_policy_id = None
        self._update_time = None
        self.discriminator = None

        if bandwidth_percent is not None:
            self.bandwidth_percent = bandwidth_percent
        if creation_time is not None:
            self.creation_time = creation_time
        if description is not None:
            self.description = description
        if dscps is not None:
            self.dscps = dscps
        if is_default is not None:
            self.is_default = is_default
        if status is not None:
            self.status = status
        if transit_router_traffic_qos_queue_entry_id is not None:
            self.transit_router_traffic_qos_queue_entry_id = transit_router_traffic_qos_queue_entry_id
        if transit_router_traffic_qos_queue_entry_name is not None:
            self.transit_router_traffic_qos_queue_entry_name = transit_router_traffic_qos_queue_entry_name
        if transit_router_traffic_qos_queue_policy_id is not None:
            self.transit_router_traffic_qos_queue_policy_id = transit_router_traffic_qos_queue_policy_id
        if update_time is not None:
            self.update_time = update_time

    @property
    def bandwidth_percent(self):
        """Gets the bandwidth_percent of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The bandwidth_percent of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: int
        """
        return self._bandwidth_percent

    @bandwidth_percent.setter
    def bandwidth_percent(self, bandwidth_percent):
        """Sets the bandwidth_percent of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param bandwidth_percent: The bandwidth_percent of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: int
        """

        self._bandwidth_percent = bandwidth_percent

    @property
    def creation_time(self):
        """Gets the creation_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The creation_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: str
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """Sets the creation_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param creation_time: The creation_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: str
        """

        self._creation_time = creation_time

    @property
    def description(self):
        """Gets the description of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The description of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param description: The description of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def dscps(self):
        """Gets the dscps of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The dscps of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: list[int]
        """
        return self._dscps

    @dscps.setter
    def dscps(self, dscps):
        """Sets the dscps of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param dscps: The dscps of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: list[int]
        """

        self._dscps = dscps

    @property
    def is_default(self):
        """Gets the is_default of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The is_default of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """Sets the is_default of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param is_default: The is_default of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: bool
        """

        self._is_default = is_default

    @property
    def status(self):
        """Gets the status of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The status of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param status: The status of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def transit_router_traffic_qos_queue_entry_id(self):
        """Gets the transit_router_traffic_qos_queue_entry_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The transit_router_traffic_qos_queue_entry_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_traffic_qos_queue_entry_id

    @transit_router_traffic_qos_queue_entry_id.setter
    def transit_router_traffic_qos_queue_entry_id(self, transit_router_traffic_qos_queue_entry_id):
        """Sets the transit_router_traffic_qos_queue_entry_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param transit_router_traffic_qos_queue_entry_id: The transit_router_traffic_qos_queue_entry_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_traffic_qos_queue_entry_id = transit_router_traffic_qos_queue_entry_id

    @property
    def transit_router_traffic_qos_queue_entry_name(self):
        """Gets the transit_router_traffic_qos_queue_entry_name of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The transit_router_traffic_qos_queue_entry_name of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_traffic_qos_queue_entry_name

    @transit_router_traffic_qos_queue_entry_name.setter
    def transit_router_traffic_qos_queue_entry_name(self, transit_router_traffic_qos_queue_entry_name):
        """Sets the transit_router_traffic_qos_queue_entry_name of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param transit_router_traffic_qos_queue_entry_name: The transit_router_traffic_qos_queue_entry_name of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_traffic_qos_queue_entry_name = transit_router_traffic_qos_queue_entry_name

    @property
    def transit_router_traffic_qos_queue_policy_id(self):
        """Gets the transit_router_traffic_qos_queue_policy_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The transit_router_traffic_qos_queue_policy_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_traffic_qos_queue_policy_id

    @transit_router_traffic_qos_queue_policy_id.setter
    def transit_router_traffic_qos_queue_policy_id(self, transit_router_traffic_qos_queue_policy_id):
        """Sets the transit_router_traffic_qos_queue_policy_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param transit_router_traffic_qos_queue_policy_id: The transit_router_traffic_qos_queue_policy_id of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: str
        """

        self._transit_router_traffic_qos_queue_policy_id = transit_router_traffic_qos_queue_policy_id

    @property
    def update_time(self):
        """Gets the update_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501


        :return: The update_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :rtype: str
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.


        :param update_time: The update_time of this TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput.  # noqa: E501
        :type: str
        """

        self._update_time = update_time

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
        if issubclass(TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput, dict):
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
        if not isinstance(other, TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TransitRouterTrafficQosQueueEntryForDescribeTransitRouterTrafficQosQueueEntriesOutput):
            return True

        return self.to_dict() != other.to_dict()
