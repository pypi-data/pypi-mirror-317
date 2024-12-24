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


class RouteEntryForDescribeRouteEntryListOutput(object):
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
        'description': 'str',
        'destination_cidr_block': 'str',
        'next_hop_id': 'str',
        'next_hop_name': 'str',
        'next_hop_type': 'str',
        'prefix_list_cidr_blocks': 'list[str]',
        'route_entry_id': 'str',
        'route_entry_name': 'str',
        'route_table_id': 'str',
        'status': 'str',
        'type': 'str',
        'vpc_id': 'str'
    }

    attribute_map = {
        'description': 'Description',
        'destination_cidr_block': 'DestinationCidrBlock',
        'next_hop_id': 'NextHopId',
        'next_hop_name': 'NextHopName',
        'next_hop_type': 'NextHopType',
        'prefix_list_cidr_blocks': 'PrefixListCidrBlocks',
        'route_entry_id': 'RouteEntryId',
        'route_entry_name': 'RouteEntryName',
        'route_table_id': 'RouteTableId',
        'status': 'Status',
        'type': 'Type',
        'vpc_id': 'VpcId'
    }

    def __init__(self, description=None, destination_cidr_block=None, next_hop_id=None, next_hop_name=None, next_hop_type=None, prefix_list_cidr_blocks=None, route_entry_id=None, route_entry_name=None, route_table_id=None, status=None, type=None, vpc_id=None, _configuration=None):  # noqa: E501
        """RouteEntryForDescribeRouteEntryListOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._description = None
        self._destination_cidr_block = None
        self._next_hop_id = None
        self._next_hop_name = None
        self._next_hop_type = None
        self._prefix_list_cidr_blocks = None
        self._route_entry_id = None
        self._route_entry_name = None
        self._route_table_id = None
        self._status = None
        self._type = None
        self._vpc_id = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if destination_cidr_block is not None:
            self.destination_cidr_block = destination_cidr_block
        if next_hop_id is not None:
            self.next_hop_id = next_hop_id
        if next_hop_name is not None:
            self.next_hop_name = next_hop_name
        if next_hop_type is not None:
            self.next_hop_type = next_hop_type
        if prefix_list_cidr_blocks is not None:
            self.prefix_list_cidr_blocks = prefix_list_cidr_blocks
        if route_entry_id is not None:
            self.route_entry_id = route_entry_id
        if route_entry_name is not None:
            self.route_entry_name = route_entry_name
        if route_table_id is not None:
            self.route_table_id = route_table_id
        if status is not None:
            self.status = status
        if type is not None:
            self.type = type
        if vpc_id is not None:
            self.vpc_id = vpc_id

    @property
    def description(self):
        """Gets the description of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The description of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RouteEntryForDescribeRouteEntryListOutput.


        :param description: The description of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def destination_cidr_block(self):
        """Gets the destination_cidr_block of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The destination_cidr_block of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._destination_cidr_block

    @destination_cidr_block.setter
    def destination_cidr_block(self, destination_cidr_block):
        """Sets the destination_cidr_block of this RouteEntryForDescribeRouteEntryListOutput.


        :param destination_cidr_block: The destination_cidr_block of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._destination_cidr_block = destination_cidr_block

    @property
    def next_hop_id(self):
        """Gets the next_hop_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The next_hop_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._next_hop_id

    @next_hop_id.setter
    def next_hop_id(self, next_hop_id):
        """Sets the next_hop_id of this RouteEntryForDescribeRouteEntryListOutput.


        :param next_hop_id: The next_hop_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._next_hop_id = next_hop_id

    @property
    def next_hop_name(self):
        """Gets the next_hop_name of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The next_hop_name of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._next_hop_name

    @next_hop_name.setter
    def next_hop_name(self, next_hop_name):
        """Sets the next_hop_name of this RouteEntryForDescribeRouteEntryListOutput.


        :param next_hop_name: The next_hop_name of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._next_hop_name = next_hop_name

    @property
    def next_hop_type(self):
        """Gets the next_hop_type of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The next_hop_type of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._next_hop_type

    @next_hop_type.setter
    def next_hop_type(self, next_hop_type):
        """Sets the next_hop_type of this RouteEntryForDescribeRouteEntryListOutput.


        :param next_hop_type: The next_hop_type of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._next_hop_type = next_hop_type

    @property
    def prefix_list_cidr_blocks(self):
        """Gets the prefix_list_cidr_blocks of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The prefix_list_cidr_blocks of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._prefix_list_cidr_blocks

    @prefix_list_cidr_blocks.setter
    def prefix_list_cidr_blocks(self, prefix_list_cidr_blocks):
        """Sets the prefix_list_cidr_blocks of this RouteEntryForDescribeRouteEntryListOutput.


        :param prefix_list_cidr_blocks: The prefix_list_cidr_blocks of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: list[str]
        """

        self._prefix_list_cidr_blocks = prefix_list_cidr_blocks

    @property
    def route_entry_id(self):
        """Gets the route_entry_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The route_entry_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._route_entry_id

    @route_entry_id.setter
    def route_entry_id(self, route_entry_id):
        """Sets the route_entry_id of this RouteEntryForDescribeRouteEntryListOutput.


        :param route_entry_id: The route_entry_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._route_entry_id = route_entry_id

    @property
    def route_entry_name(self):
        """Gets the route_entry_name of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The route_entry_name of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._route_entry_name

    @route_entry_name.setter
    def route_entry_name(self, route_entry_name):
        """Sets the route_entry_name of this RouteEntryForDescribeRouteEntryListOutput.


        :param route_entry_name: The route_entry_name of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._route_entry_name = route_entry_name

    @property
    def route_table_id(self):
        """Gets the route_table_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The route_table_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._route_table_id

    @route_table_id.setter
    def route_table_id(self, route_table_id):
        """Sets the route_table_id of this RouteEntryForDescribeRouteEntryListOutput.


        :param route_table_id: The route_table_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._route_table_id = route_table_id

    @property
    def status(self):
        """Gets the status of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The status of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this RouteEntryForDescribeRouteEntryListOutput.


        :param status: The status of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def type(self):
        """Gets the type of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The type of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this RouteEntryForDescribeRouteEntryListOutput.


        :param type: The type of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def vpc_id(self):
        """Gets the vpc_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501


        :return: The vpc_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this RouteEntryForDescribeRouteEntryListOutput.


        :param vpc_id: The vpc_id of this RouteEntryForDescribeRouteEntryListOutput.  # noqa: E501
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
        if issubclass(RouteEntryForDescribeRouteEntryListOutput, dict):
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
        if not isinstance(other, RouteEntryForDescribeRouteEntryListOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RouteEntryForDescribeRouteEntryListOutput):
            return True

        return self.to_dict() != other.to_dict()
