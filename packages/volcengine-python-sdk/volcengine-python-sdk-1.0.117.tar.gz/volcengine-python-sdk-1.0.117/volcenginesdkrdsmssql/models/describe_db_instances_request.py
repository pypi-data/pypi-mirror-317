# coding: utf-8

"""
    rds_mssql

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeDBInstancesRequest(object):
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
        'charge_type': 'str',
        'create_time_end': 'str',
        'create_time_start': 'str',
        'db_engine_version': 'str',
        'instance_category': 'str',
        'instance_id': 'str',
        'instance_name': 'str',
        'instance_status': 'str',
        'instance_type': 'str',
        'page_number': 'int',
        'page_size': 'int',
        'primary_instance_id': 'str',
        'tag_filters': 'list[TagFilterForDescribeDBInstancesInput]',
        'zone_id': 'str'
    }

    attribute_map = {
        'charge_type': 'ChargeType',
        'create_time_end': 'CreateTimeEnd',
        'create_time_start': 'CreateTimeStart',
        'db_engine_version': 'DBEngineVersion',
        'instance_category': 'InstanceCategory',
        'instance_id': 'InstanceId',
        'instance_name': 'InstanceName',
        'instance_status': 'InstanceStatus',
        'instance_type': 'InstanceType',
        'page_number': 'PageNumber',
        'page_size': 'PageSize',
        'primary_instance_id': 'PrimaryInstanceId',
        'tag_filters': 'TagFilters',
        'zone_id': 'ZoneId'
    }

    def __init__(self, charge_type=None, create_time_end=None, create_time_start=None, db_engine_version=None, instance_category=None, instance_id=None, instance_name=None, instance_status=None, instance_type=None, page_number=None, page_size=None, primary_instance_id=None, tag_filters=None, zone_id=None, _configuration=None):  # noqa: E501
        """DescribeDBInstancesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._charge_type = None
        self._create_time_end = None
        self._create_time_start = None
        self._db_engine_version = None
        self._instance_category = None
        self._instance_id = None
        self._instance_name = None
        self._instance_status = None
        self._instance_type = None
        self._page_number = None
        self._page_size = None
        self._primary_instance_id = None
        self._tag_filters = None
        self._zone_id = None
        self.discriminator = None

        if charge_type is not None:
            self.charge_type = charge_type
        if create_time_end is not None:
            self.create_time_end = create_time_end
        if create_time_start is not None:
            self.create_time_start = create_time_start
        if db_engine_version is not None:
            self.db_engine_version = db_engine_version
        if instance_category is not None:
            self.instance_category = instance_category
        if instance_id is not None:
            self.instance_id = instance_id
        if instance_name is not None:
            self.instance_name = instance_name
        if instance_status is not None:
            self.instance_status = instance_status
        if instance_type is not None:
            self.instance_type = instance_type
        if page_number is not None:
            self.page_number = page_number
        if page_size is not None:
            self.page_size = page_size
        if primary_instance_id is not None:
            self.primary_instance_id = primary_instance_id
        if tag_filters is not None:
            self.tag_filters = tag_filters
        if zone_id is not None:
            self.zone_id = zone_id

    @property
    def charge_type(self):
        """Gets the charge_type of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The charge_type of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._charge_type

    @charge_type.setter
    def charge_type(self, charge_type):
        """Sets the charge_type of this DescribeDBInstancesRequest.


        :param charge_type: The charge_type of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._charge_type = charge_type

    @property
    def create_time_end(self):
        """Gets the create_time_end of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The create_time_end of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._create_time_end

    @create_time_end.setter
    def create_time_end(self, create_time_end):
        """Sets the create_time_end of this DescribeDBInstancesRequest.


        :param create_time_end: The create_time_end of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._create_time_end = create_time_end

    @property
    def create_time_start(self):
        """Gets the create_time_start of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The create_time_start of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._create_time_start

    @create_time_start.setter
    def create_time_start(self, create_time_start):
        """Sets the create_time_start of this DescribeDBInstancesRequest.


        :param create_time_start: The create_time_start of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._create_time_start = create_time_start

    @property
    def db_engine_version(self):
        """Gets the db_engine_version of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The db_engine_version of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._db_engine_version

    @db_engine_version.setter
    def db_engine_version(self, db_engine_version):
        """Sets the db_engine_version of this DescribeDBInstancesRequest.


        :param db_engine_version: The db_engine_version of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._db_engine_version = db_engine_version

    @property
    def instance_category(self):
        """Gets the instance_category of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The instance_category of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_category

    @instance_category.setter
    def instance_category(self, instance_category):
        """Sets the instance_category of this DescribeDBInstancesRequest.


        :param instance_category: The instance_category of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._instance_category = instance_category

    @property
    def instance_id(self):
        """Gets the instance_id of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The instance_id of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this DescribeDBInstancesRequest.


        :param instance_id: The instance_id of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._instance_id = instance_id

    @property
    def instance_name(self):
        """Gets the instance_name of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The instance_name of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """Sets the instance_name of this DescribeDBInstancesRequest.


        :param instance_name: The instance_name of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._instance_name = instance_name

    @property
    def instance_status(self):
        """Gets the instance_status of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The instance_status of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_status

    @instance_status.setter
    def instance_status(self, instance_status):
        """Sets the instance_status of this DescribeDBInstancesRequest.


        :param instance_status: The instance_status of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._instance_status = instance_status

    @property
    def instance_type(self):
        """Gets the instance_type of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The instance_type of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """Sets the instance_type of this DescribeDBInstancesRequest.


        :param instance_type: The instance_type of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._instance_type = instance_type

    @property
    def page_number(self):
        """Gets the page_number of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The page_number of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this DescribeDBInstancesRequest.


        :param page_number: The page_number of this DescribeDBInstancesRequest.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The page_size of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this DescribeDBInstancesRequest.


        :param page_size: The page_size of this DescribeDBInstancesRequest.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def primary_instance_id(self):
        """Gets the primary_instance_id of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The primary_instance_id of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._primary_instance_id

    @primary_instance_id.setter
    def primary_instance_id(self, primary_instance_id):
        """Sets the primary_instance_id of this DescribeDBInstancesRequest.


        :param primary_instance_id: The primary_instance_id of this DescribeDBInstancesRequest.  # noqa: E501
        :type: str
        """

        self._primary_instance_id = primary_instance_id

    @property
    def tag_filters(self):
        """Gets the tag_filters of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The tag_filters of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: list[TagFilterForDescribeDBInstancesInput]
        """
        return self._tag_filters

    @tag_filters.setter
    def tag_filters(self, tag_filters):
        """Sets the tag_filters of this DescribeDBInstancesRequest.


        :param tag_filters: The tag_filters of this DescribeDBInstancesRequest.  # noqa: E501
        :type: list[TagFilterForDescribeDBInstancesInput]
        """

        self._tag_filters = tag_filters

    @property
    def zone_id(self):
        """Gets the zone_id of this DescribeDBInstancesRequest.  # noqa: E501


        :return: The zone_id of this DescribeDBInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._zone_id

    @zone_id.setter
    def zone_id(self, zone_id):
        """Sets the zone_id of this DescribeDBInstancesRequest.


        :param zone_id: The zone_id of this DescribeDBInstancesRequest.  # noqa: E501
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
        if issubclass(DescribeDBInstancesRequest, dict):
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
        if not isinstance(other, DescribeDBInstancesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeDBInstancesRequest):
            return True

        return self.to_dict() != other.to_dict()
