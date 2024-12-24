# coding: utf-8

"""
    mcs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput(object):
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
        'vendor_alert_data_uuid': 'str',
        'vendor_alert_threat_direction': 'str',
        'vendor_alert_type': 'str'
    }

    attribute_map = {
        'vendor_alert_data_uuid': 'vendor_alert_data_uuid',
        'vendor_alert_threat_direction': 'vendor_alert_threat_direction',
        'vendor_alert_type': 'vendor_alert_type'
    }

    def __init__(self, vendor_alert_data_uuid=None, vendor_alert_threat_direction=None, vendor_alert_type=None, _configuration=None):  # noqa: E501
        """AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._vendor_alert_data_uuid = None
        self._vendor_alert_threat_direction = None
        self._vendor_alert_type = None
        self.discriminator = None

        if vendor_alert_data_uuid is not None:
            self.vendor_alert_data_uuid = vendor_alert_data_uuid
        if vendor_alert_threat_direction is not None:
            self.vendor_alert_threat_direction = vendor_alert_threat_direction
        if vendor_alert_type is not None:
            self.vendor_alert_type = vendor_alert_type

    @property
    def vendor_alert_data_uuid(self):
        """Gets the vendor_alert_data_uuid of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501


        :return: The vendor_alert_data_uuid of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._vendor_alert_data_uuid

    @vendor_alert_data_uuid.setter
    def vendor_alert_data_uuid(self, vendor_alert_data_uuid):
        """Sets the vendor_alert_data_uuid of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.


        :param vendor_alert_data_uuid: The vendor_alert_data_uuid of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501
        :type: str
        """

        self._vendor_alert_data_uuid = vendor_alert_data_uuid

    @property
    def vendor_alert_threat_direction(self):
        """Gets the vendor_alert_threat_direction of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501


        :return: The vendor_alert_threat_direction of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._vendor_alert_threat_direction

    @vendor_alert_threat_direction.setter
    def vendor_alert_threat_direction(self, vendor_alert_threat_direction):
        """Sets the vendor_alert_threat_direction of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.


        :param vendor_alert_threat_direction: The vendor_alert_threat_direction of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501
        :type: str
        """

        self._vendor_alert_threat_direction = vendor_alert_threat_direction

    @property
    def vendor_alert_type(self):
        """Gets the vendor_alert_type of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501


        :return: The vendor_alert_type of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._vendor_alert_type

    @vendor_alert_type.setter
    def vendor_alert_type(self, vendor_alert_type):
        """Sets the vendor_alert_type of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.


        :param vendor_alert_type: The vendor_alert_type of this AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput.  # noqa: E501
        :type: str
        """

        self._vendor_alert_type = vendor_alert_type

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
        if issubclass(AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput, dict):
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
        if not isinstance(other, AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AlarmVendorAlertMetaForGetApiV1AlarmDetailOutput):
            return True

        return self.to_dict() != other.to_dict()
