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


class DescribeTransitRouterBandwidthPackagesRequest(object):
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
        'local_geographic_region_set_id': 'str',
        'page_number': 'int',
        'page_size': 'int',
        'peer_geographic_region_set_id': 'str',
        'project_name': 'str',
        'tag_filters': 'list[TagFilterForDescribeTransitRouterBandwidthPackagesInput]',
        'transit_router_bandwidth_package_ids': 'list[str]',
        'transit_router_bandwidth_package_name': 'str',
        'transit_router_peer_attachment_id': 'str'
    }

    attribute_map = {
        'local_geographic_region_set_id': 'LocalGeographicRegionSetId',
        'page_number': 'PageNumber',
        'page_size': 'PageSize',
        'peer_geographic_region_set_id': 'PeerGeographicRegionSetId',
        'project_name': 'ProjectName',
        'tag_filters': 'TagFilters',
        'transit_router_bandwidth_package_ids': 'TransitRouterBandwidthPackageIds',
        'transit_router_bandwidth_package_name': 'TransitRouterBandwidthPackageName',
        'transit_router_peer_attachment_id': 'TransitRouterPeerAttachmentId'
    }

    def __init__(self, local_geographic_region_set_id=None, page_number=None, page_size=None, peer_geographic_region_set_id=None, project_name=None, tag_filters=None, transit_router_bandwidth_package_ids=None, transit_router_bandwidth_package_name=None, transit_router_peer_attachment_id=None, _configuration=None):  # noqa: E501
        """DescribeTransitRouterBandwidthPackagesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._local_geographic_region_set_id = None
        self._page_number = None
        self._page_size = None
        self._peer_geographic_region_set_id = None
        self._project_name = None
        self._tag_filters = None
        self._transit_router_bandwidth_package_ids = None
        self._transit_router_bandwidth_package_name = None
        self._transit_router_peer_attachment_id = None
        self.discriminator = None

        if local_geographic_region_set_id is not None:
            self.local_geographic_region_set_id = local_geographic_region_set_id
        if page_number is not None:
            self.page_number = page_number
        if page_size is not None:
            self.page_size = page_size
        if peer_geographic_region_set_id is not None:
            self.peer_geographic_region_set_id = peer_geographic_region_set_id
        if project_name is not None:
            self.project_name = project_name
        if tag_filters is not None:
            self.tag_filters = tag_filters
        if transit_router_bandwidth_package_ids is not None:
            self.transit_router_bandwidth_package_ids = transit_router_bandwidth_package_ids
        if transit_router_bandwidth_package_name is not None:
            self.transit_router_bandwidth_package_name = transit_router_bandwidth_package_name
        if transit_router_peer_attachment_id is not None:
            self.transit_router_peer_attachment_id = transit_router_peer_attachment_id

    @property
    def local_geographic_region_set_id(self):
        """Gets the local_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The local_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: str
        """
        return self._local_geographic_region_set_id

    @local_geographic_region_set_id.setter
    def local_geographic_region_set_id(self, local_geographic_region_set_id):
        """Sets the local_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.


        :param local_geographic_region_set_id: The local_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: str
        """

        self._local_geographic_region_set_id = local_geographic_region_set_id

    @property
    def page_number(self):
        """Gets the page_number of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The page_number of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this DescribeTransitRouterBandwidthPackagesRequest.


        :param page_number: The page_number of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The page_size of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this DescribeTransitRouterBandwidthPackagesRequest.


        :param page_size: The page_size of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def peer_geographic_region_set_id(self):
        """Gets the peer_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The peer_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: str
        """
        return self._peer_geographic_region_set_id

    @peer_geographic_region_set_id.setter
    def peer_geographic_region_set_id(self, peer_geographic_region_set_id):
        """Sets the peer_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.


        :param peer_geographic_region_set_id: The peer_geographic_region_set_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: str
        """

        self._peer_geographic_region_set_id = peer_geographic_region_set_id

    @property
    def project_name(self):
        """Gets the project_name of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The project_name of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this DescribeTransitRouterBandwidthPackagesRequest.


        :param project_name: The project_name of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def tag_filters(self):
        """Gets the tag_filters of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The tag_filters of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: list[TagFilterForDescribeTransitRouterBandwidthPackagesInput]
        """
        return self._tag_filters

    @tag_filters.setter
    def tag_filters(self, tag_filters):
        """Sets the tag_filters of this DescribeTransitRouterBandwidthPackagesRequest.


        :param tag_filters: The tag_filters of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: list[TagFilterForDescribeTransitRouterBandwidthPackagesInput]
        """

        self._tag_filters = tag_filters

    @property
    def transit_router_bandwidth_package_ids(self):
        """Gets the transit_router_bandwidth_package_ids of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The transit_router_bandwidth_package_ids of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._transit_router_bandwidth_package_ids

    @transit_router_bandwidth_package_ids.setter
    def transit_router_bandwidth_package_ids(self, transit_router_bandwidth_package_ids):
        """Sets the transit_router_bandwidth_package_ids of this DescribeTransitRouterBandwidthPackagesRequest.


        :param transit_router_bandwidth_package_ids: The transit_router_bandwidth_package_ids of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: list[str]
        """

        self._transit_router_bandwidth_package_ids = transit_router_bandwidth_package_ids

    @property
    def transit_router_bandwidth_package_name(self):
        """Gets the transit_router_bandwidth_package_name of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The transit_router_bandwidth_package_name of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_bandwidth_package_name

    @transit_router_bandwidth_package_name.setter
    def transit_router_bandwidth_package_name(self, transit_router_bandwidth_package_name):
        """Sets the transit_router_bandwidth_package_name of this DescribeTransitRouterBandwidthPackagesRequest.


        :param transit_router_bandwidth_package_name: The transit_router_bandwidth_package_name of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: str
        """

        self._transit_router_bandwidth_package_name = transit_router_bandwidth_package_name

    @property
    def transit_router_peer_attachment_id(self):
        """Gets the transit_router_peer_attachment_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501


        :return: The transit_router_peer_attachment_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :rtype: str
        """
        return self._transit_router_peer_attachment_id

    @transit_router_peer_attachment_id.setter
    def transit_router_peer_attachment_id(self, transit_router_peer_attachment_id):
        """Sets the transit_router_peer_attachment_id of this DescribeTransitRouterBandwidthPackagesRequest.


        :param transit_router_peer_attachment_id: The transit_router_peer_attachment_id of this DescribeTransitRouterBandwidthPackagesRequest.  # noqa: E501
        :type: str
        """

        self._transit_router_peer_attachment_id = transit_router_peer_attachment_id

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
        if issubclass(DescribeTransitRouterBandwidthPackagesRequest, dict):
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
        if not isinstance(other, DescribeTransitRouterBandwidthPackagesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeTransitRouterBandwidthPackagesRequest):
            return True

        return self.to_dict() != other.to_dict()
