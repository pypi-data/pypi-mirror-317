# coding: utf-8

"""
    cdn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ServiceInfoForDescribeCdnServiceOutput(object):
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
        'begin_time': 'str',
        'billing_code': 'str',
        'billing_cycle': 'str',
        'billing_data': 'str',
        'billing_desc': 'str',
        'create_time': 'str',
        'instance_category': 'str',
        'instance_no': 'str',
        'instance_type': 'str',
        'metric_type': 'str',
        'service_region': 'str',
        'start_time': 'str',
        'status': 'str'
    }

    attribute_map = {
        'begin_time': 'BeginTime',
        'billing_code': 'BillingCode',
        'billing_cycle': 'BillingCycle',
        'billing_data': 'BillingData',
        'billing_desc': 'BillingDesc',
        'create_time': 'CreateTime',
        'instance_category': 'InstanceCategory',
        'instance_no': 'InstanceNo',
        'instance_type': 'InstanceType',
        'metric_type': 'MetricType',
        'service_region': 'ServiceRegion',
        'start_time': 'StartTime',
        'status': 'Status'
    }

    def __init__(self, begin_time=None, billing_code=None, billing_cycle=None, billing_data=None, billing_desc=None, create_time=None, instance_category=None, instance_no=None, instance_type=None, metric_type=None, service_region=None, start_time=None, status=None, _configuration=None):  # noqa: E501
        """ServiceInfoForDescribeCdnServiceOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._begin_time = None
        self._billing_code = None
        self._billing_cycle = None
        self._billing_data = None
        self._billing_desc = None
        self._create_time = None
        self._instance_category = None
        self._instance_no = None
        self._instance_type = None
        self._metric_type = None
        self._service_region = None
        self._start_time = None
        self._status = None
        self.discriminator = None

        if begin_time is not None:
            self.begin_time = begin_time
        if billing_code is not None:
            self.billing_code = billing_code
        if billing_cycle is not None:
            self.billing_cycle = billing_cycle
        if billing_data is not None:
            self.billing_data = billing_data
        if billing_desc is not None:
            self.billing_desc = billing_desc
        if create_time is not None:
            self.create_time = create_time
        if instance_category is not None:
            self.instance_category = instance_category
        if instance_no is not None:
            self.instance_no = instance_no
        if instance_type is not None:
            self.instance_type = instance_type
        if metric_type is not None:
            self.metric_type = metric_type
        if service_region is not None:
            self.service_region = service_region
        if start_time is not None:
            self.start_time = start_time
        if status is not None:
            self.status = status

    @property
    def begin_time(self):
        """Gets the begin_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The begin_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._begin_time

    @begin_time.setter
    def begin_time(self, begin_time):
        """Sets the begin_time of this ServiceInfoForDescribeCdnServiceOutput.


        :param begin_time: The begin_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._begin_time = begin_time

    @property
    def billing_code(self):
        """Gets the billing_code of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The billing_code of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._billing_code

    @billing_code.setter
    def billing_code(self, billing_code):
        """Sets the billing_code of this ServiceInfoForDescribeCdnServiceOutput.


        :param billing_code: The billing_code of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._billing_code = billing_code

    @property
    def billing_cycle(self):
        """Gets the billing_cycle of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The billing_cycle of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._billing_cycle

    @billing_cycle.setter
    def billing_cycle(self, billing_cycle):
        """Sets the billing_cycle of this ServiceInfoForDescribeCdnServiceOutput.


        :param billing_cycle: The billing_cycle of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._billing_cycle = billing_cycle

    @property
    def billing_data(self):
        """Gets the billing_data of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The billing_data of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._billing_data

    @billing_data.setter
    def billing_data(self, billing_data):
        """Sets the billing_data of this ServiceInfoForDescribeCdnServiceOutput.


        :param billing_data: The billing_data of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._billing_data = billing_data

    @property
    def billing_desc(self):
        """Gets the billing_desc of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The billing_desc of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._billing_desc

    @billing_desc.setter
    def billing_desc(self, billing_desc):
        """Sets the billing_desc of this ServiceInfoForDescribeCdnServiceOutput.


        :param billing_desc: The billing_desc of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._billing_desc = billing_desc

    @property
    def create_time(self):
        """Gets the create_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The create_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this ServiceInfoForDescribeCdnServiceOutput.


        :param create_time: The create_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._create_time = create_time

    @property
    def instance_category(self):
        """Gets the instance_category of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The instance_category of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._instance_category

    @instance_category.setter
    def instance_category(self, instance_category):
        """Sets the instance_category of this ServiceInfoForDescribeCdnServiceOutput.


        :param instance_category: The instance_category of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._instance_category = instance_category

    @property
    def instance_no(self):
        """Gets the instance_no of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The instance_no of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._instance_no

    @instance_no.setter
    def instance_no(self, instance_no):
        """Sets the instance_no of this ServiceInfoForDescribeCdnServiceOutput.


        :param instance_no: The instance_no of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._instance_no = instance_no

    @property
    def instance_type(self):
        """Gets the instance_type of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The instance_type of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """Sets the instance_type of this ServiceInfoForDescribeCdnServiceOutput.


        :param instance_type: The instance_type of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._instance_type = instance_type

    @property
    def metric_type(self):
        """Gets the metric_type of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The metric_type of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._metric_type

    @metric_type.setter
    def metric_type(self, metric_type):
        """Sets the metric_type of this ServiceInfoForDescribeCdnServiceOutput.


        :param metric_type: The metric_type of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._metric_type = metric_type

    @property
    def service_region(self):
        """Gets the service_region of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The service_region of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._service_region

    @service_region.setter
    def service_region(self, service_region):
        """Sets the service_region of this ServiceInfoForDescribeCdnServiceOutput.


        :param service_region: The service_region of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._service_region = service_region

    @property
    def start_time(self):
        """Gets the start_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The start_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this ServiceInfoForDescribeCdnServiceOutput.


        :param start_time: The start_time of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._start_time = start_time

    @property
    def status(self):
        """Gets the status of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501


        :return: The status of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ServiceInfoForDescribeCdnServiceOutput.


        :param status: The status of this ServiceInfoForDescribeCdnServiceOutput.  # noqa: E501
        :type: str
        """

        self._status = status

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
        if issubclass(ServiceInfoForDescribeCdnServiceOutput, dict):
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
        if not isinstance(other, ServiceInfoForDescribeCdnServiceOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ServiceInfoForDescribeCdnServiceOutput):
            return True

        return self.to_dict() != other.to_dict()
