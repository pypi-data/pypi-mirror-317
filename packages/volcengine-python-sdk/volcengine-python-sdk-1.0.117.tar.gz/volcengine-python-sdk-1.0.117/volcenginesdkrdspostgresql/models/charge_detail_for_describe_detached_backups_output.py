# coding: utf-8

"""
    rds_postgresql

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ChargeDetailForDescribeDetachedBackupsOutput(object):
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
        'auto_renew': 'bool',
        'charge_end_time': 'str',
        'charge_start_time': 'str',
        'charge_status': 'str',
        'charge_type': 'str',
        'number': 'int',
        'overdue_reclaim_time': 'str',
        'overdue_time': 'str',
        'period': 'int',
        'period_unit': 'str',
        'temp_modify_end_time': 'str',
        'temp_modify_start_time': 'str'
    }

    attribute_map = {
        'auto_renew': 'AutoRenew',
        'charge_end_time': 'ChargeEndTime',
        'charge_start_time': 'ChargeStartTime',
        'charge_status': 'ChargeStatus',
        'charge_type': 'ChargeType',
        'number': 'Number',
        'overdue_reclaim_time': 'OverdueReclaimTime',
        'overdue_time': 'OverdueTime',
        'period': 'Period',
        'period_unit': 'PeriodUnit',
        'temp_modify_end_time': 'TempModifyEndTime',
        'temp_modify_start_time': 'TempModifyStartTime'
    }

    def __init__(self, auto_renew=None, charge_end_time=None, charge_start_time=None, charge_status=None, charge_type=None, number=None, overdue_reclaim_time=None, overdue_time=None, period=None, period_unit=None, temp_modify_end_time=None, temp_modify_start_time=None, _configuration=None):  # noqa: E501
        """ChargeDetailForDescribeDetachedBackupsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._auto_renew = None
        self._charge_end_time = None
        self._charge_start_time = None
        self._charge_status = None
        self._charge_type = None
        self._number = None
        self._overdue_reclaim_time = None
        self._overdue_time = None
        self._period = None
        self._period_unit = None
        self._temp_modify_end_time = None
        self._temp_modify_start_time = None
        self.discriminator = None

        if auto_renew is not None:
            self.auto_renew = auto_renew
        if charge_end_time is not None:
            self.charge_end_time = charge_end_time
        if charge_start_time is not None:
            self.charge_start_time = charge_start_time
        if charge_status is not None:
            self.charge_status = charge_status
        if charge_type is not None:
            self.charge_type = charge_type
        if number is not None:
            self.number = number
        if overdue_reclaim_time is not None:
            self.overdue_reclaim_time = overdue_reclaim_time
        if overdue_time is not None:
            self.overdue_time = overdue_time
        if period is not None:
            self.period = period
        if period_unit is not None:
            self.period_unit = period_unit
        if temp_modify_end_time is not None:
            self.temp_modify_end_time = temp_modify_end_time
        if temp_modify_start_time is not None:
            self.temp_modify_start_time = temp_modify_start_time

    @property
    def auto_renew(self):
        """Gets the auto_renew of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The auto_renew of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: bool
        """
        return self._auto_renew

    @auto_renew.setter
    def auto_renew(self, auto_renew):
        """Sets the auto_renew of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param auto_renew: The auto_renew of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: bool
        """

        self._auto_renew = auto_renew

    @property
    def charge_end_time(self):
        """Gets the charge_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The charge_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._charge_end_time

    @charge_end_time.setter
    def charge_end_time(self, charge_end_time):
        """Sets the charge_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param charge_end_time: The charge_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._charge_end_time = charge_end_time

    @property
    def charge_start_time(self):
        """Gets the charge_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The charge_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._charge_start_time

    @charge_start_time.setter
    def charge_start_time(self, charge_start_time):
        """Sets the charge_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param charge_start_time: The charge_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._charge_start_time = charge_start_time

    @property
    def charge_status(self):
        """Gets the charge_status of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The charge_status of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._charge_status

    @charge_status.setter
    def charge_status(self, charge_status):
        """Sets the charge_status of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param charge_status: The charge_status of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._charge_status = charge_status

    @property
    def charge_type(self):
        """Gets the charge_type of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The charge_type of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._charge_type

    @charge_type.setter
    def charge_type(self, charge_type):
        """Sets the charge_type of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param charge_type: The charge_type of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._charge_type = charge_type

    @property
    def number(self):
        """Gets the number of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The number of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param number: The number of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: int
        """

        self._number = number

    @property
    def overdue_reclaim_time(self):
        """Gets the overdue_reclaim_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The overdue_reclaim_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._overdue_reclaim_time

    @overdue_reclaim_time.setter
    def overdue_reclaim_time(self, overdue_reclaim_time):
        """Sets the overdue_reclaim_time of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param overdue_reclaim_time: The overdue_reclaim_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._overdue_reclaim_time = overdue_reclaim_time

    @property
    def overdue_time(self):
        """Gets the overdue_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The overdue_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._overdue_time

    @overdue_time.setter
    def overdue_time(self, overdue_time):
        """Sets the overdue_time of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param overdue_time: The overdue_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._overdue_time = overdue_time

    @property
    def period(self):
        """Gets the period of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The period of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: int
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param period: The period of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: int
        """

        self._period = period

    @property
    def period_unit(self):
        """Gets the period_unit of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The period_unit of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._period_unit

    @period_unit.setter
    def period_unit(self, period_unit):
        """Sets the period_unit of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param period_unit: The period_unit of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._period_unit = period_unit

    @property
    def temp_modify_end_time(self):
        """Gets the temp_modify_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The temp_modify_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._temp_modify_end_time

    @temp_modify_end_time.setter
    def temp_modify_end_time(self, temp_modify_end_time):
        """Sets the temp_modify_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param temp_modify_end_time: The temp_modify_end_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._temp_modify_end_time = temp_modify_end_time

    @property
    def temp_modify_start_time(self):
        """Gets the temp_modify_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501


        :return: The temp_modify_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :rtype: str
        """
        return self._temp_modify_start_time

    @temp_modify_start_time.setter
    def temp_modify_start_time(self, temp_modify_start_time):
        """Sets the temp_modify_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.


        :param temp_modify_start_time: The temp_modify_start_time of this ChargeDetailForDescribeDetachedBackupsOutput.  # noqa: E501
        :type: str
        """

        self._temp_modify_start_time = temp_modify_start_time

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
        if issubclass(ChargeDetailForDescribeDetachedBackupsOutput, dict):
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
        if not isinstance(other, ChargeDetailForDescribeDetachedBackupsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChargeDetailForDescribeDetachedBackupsOutput):
            return True

        return self.to_dict() != other.to_dict()
