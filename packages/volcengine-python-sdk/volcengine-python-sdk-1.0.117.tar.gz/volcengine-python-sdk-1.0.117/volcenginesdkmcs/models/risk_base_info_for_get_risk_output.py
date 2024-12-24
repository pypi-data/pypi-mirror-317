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


class RiskBaseInfoForGetRiskOutput(object):
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
        'affected_resource': 'AffectedResourceForGetRiskOutput',
        'last_detect_time_milli': 'int',
        'last_discover_time_milli': 'int',
        'resource_status': 'str',
        'risk_exempt_meta': 'RiskExemptMetaForGetRiskOutput',
        'risk_id': 'str',
        'risk_level': 'str',
        'risk_meta_id': 'str',
        'risk_model_type': 'str',
        'risk_name': 'str',
        'risk_process_status': 'str',
        'risk_status': 'str',
        'risk_types': 'list[str]',
        'support_repair': 'bool',
        'support_verify': 'bool'
    }

    attribute_map = {
        'affected_resource': 'AffectedResource',
        'last_detect_time_milli': 'LastDetectTimeMilli',
        'last_discover_time_milli': 'LastDiscoverTimeMilli',
        'resource_status': 'ResourceStatus',
        'risk_exempt_meta': 'RiskExemptMeta',
        'risk_id': 'RiskID',
        'risk_level': 'RiskLevel',
        'risk_meta_id': 'RiskMetaID',
        'risk_model_type': 'RiskModelType',
        'risk_name': 'RiskName',
        'risk_process_status': 'RiskProcessStatus',
        'risk_status': 'RiskStatus',
        'risk_types': 'RiskTypes',
        'support_repair': 'SupportRepair',
        'support_verify': 'SupportVerify'
    }

    def __init__(self, affected_resource=None, last_detect_time_milli=None, last_discover_time_milli=None, resource_status=None, risk_exempt_meta=None, risk_id=None, risk_level=None, risk_meta_id=None, risk_model_type=None, risk_name=None, risk_process_status=None, risk_status=None, risk_types=None, support_repair=None, support_verify=None, _configuration=None):  # noqa: E501
        """RiskBaseInfoForGetRiskOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._affected_resource = None
        self._last_detect_time_milli = None
        self._last_discover_time_milli = None
        self._resource_status = None
        self._risk_exempt_meta = None
        self._risk_id = None
        self._risk_level = None
        self._risk_meta_id = None
        self._risk_model_type = None
        self._risk_name = None
        self._risk_process_status = None
        self._risk_status = None
        self._risk_types = None
        self._support_repair = None
        self._support_verify = None
        self.discriminator = None

        if affected_resource is not None:
            self.affected_resource = affected_resource
        if last_detect_time_milli is not None:
            self.last_detect_time_milli = last_detect_time_milli
        if last_discover_time_milli is not None:
            self.last_discover_time_milli = last_discover_time_milli
        if resource_status is not None:
            self.resource_status = resource_status
        if risk_exempt_meta is not None:
            self.risk_exempt_meta = risk_exempt_meta
        if risk_id is not None:
            self.risk_id = risk_id
        if risk_level is not None:
            self.risk_level = risk_level
        if risk_meta_id is not None:
            self.risk_meta_id = risk_meta_id
        if risk_model_type is not None:
            self.risk_model_type = risk_model_type
        if risk_name is not None:
            self.risk_name = risk_name
        if risk_process_status is not None:
            self.risk_process_status = risk_process_status
        if risk_status is not None:
            self.risk_status = risk_status
        if risk_types is not None:
            self.risk_types = risk_types
        if support_repair is not None:
            self.support_repair = support_repair
        if support_verify is not None:
            self.support_verify = support_verify

    @property
    def affected_resource(self):
        """Gets the affected_resource of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The affected_resource of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: AffectedResourceForGetRiskOutput
        """
        return self._affected_resource

    @affected_resource.setter
    def affected_resource(self, affected_resource):
        """Sets the affected_resource of this RiskBaseInfoForGetRiskOutput.


        :param affected_resource: The affected_resource of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: AffectedResourceForGetRiskOutput
        """

        self._affected_resource = affected_resource

    @property
    def last_detect_time_milli(self):
        """Gets the last_detect_time_milli of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The last_detect_time_milli of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: int
        """
        return self._last_detect_time_milli

    @last_detect_time_milli.setter
    def last_detect_time_milli(self, last_detect_time_milli):
        """Sets the last_detect_time_milli of this RiskBaseInfoForGetRiskOutput.


        :param last_detect_time_milli: The last_detect_time_milli of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: int
        """

        self._last_detect_time_milli = last_detect_time_milli

    @property
    def last_discover_time_milli(self):
        """Gets the last_discover_time_milli of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The last_discover_time_milli of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: int
        """
        return self._last_discover_time_milli

    @last_discover_time_milli.setter
    def last_discover_time_milli(self, last_discover_time_milli):
        """Sets the last_discover_time_milli of this RiskBaseInfoForGetRiskOutput.


        :param last_discover_time_milli: The last_discover_time_milli of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: int
        """

        self._last_discover_time_milli = last_discover_time_milli

    @property
    def resource_status(self):
        """Gets the resource_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The resource_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._resource_status

    @resource_status.setter
    def resource_status(self, resource_status):
        """Sets the resource_status of this RiskBaseInfoForGetRiskOutput.


        :param resource_status: The resource_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._resource_status = resource_status

    @property
    def risk_exempt_meta(self):
        """Gets the risk_exempt_meta of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_exempt_meta of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: RiskExemptMetaForGetRiskOutput
        """
        return self._risk_exempt_meta

    @risk_exempt_meta.setter
    def risk_exempt_meta(self, risk_exempt_meta):
        """Sets the risk_exempt_meta of this RiskBaseInfoForGetRiskOutput.


        :param risk_exempt_meta: The risk_exempt_meta of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: RiskExemptMetaForGetRiskOutput
        """

        self._risk_exempt_meta = risk_exempt_meta

    @property
    def risk_id(self):
        """Gets the risk_id of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_id of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._risk_id

    @risk_id.setter
    def risk_id(self, risk_id):
        """Sets the risk_id of this RiskBaseInfoForGetRiskOutput.


        :param risk_id: The risk_id of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._risk_id = risk_id

    @property
    def risk_level(self):
        """Gets the risk_level of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_level of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._risk_level

    @risk_level.setter
    def risk_level(self, risk_level):
        """Sets the risk_level of this RiskBaseInfoForGetRiskOutput.


        :param risk_level: The risk_level of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._risk_level = risk_level

    @property
    def risk_meta_id(self):
        """Gets the risk_meta_id of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_meta_id of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._risk_meta_id

    @risk_meta_id.setter
    def risk_meta_id(self, risk_meta_id):
        """Sets the risk_meta_id of this RiskBaseInfoForGetRiskOutput.


        :param risk_meta_id: The risk_meta_id of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._risk_meta_id = risk_meta_id

    @property
    def risk_model_type(self):
        """Gets the risk_model_type of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_model_type of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._risk_model_type

    @risk_model_type.setter
    def risk_model_type(self, risk_model_type):
        """Sets the risk_model_type of this RiskBaseInfoForGetRiskOutput.


        :param risk_model_type: The risk_model_type of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._risk_model_type = risk_model_type

    @property
    def risk_name(self):
        """Gets the risk_name of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_name of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._risk_name

    @risk_name.setter
    def risk_name(self, risk_name):
        """Sets the risk_name of this RiskBaseInfoForGetRiskOutput.


        :param risk_name: The risk_name of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._risk_name = risk_name

    @property
    def risk_process_status(self):
        """Gets the risk_process_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_process_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._risk_process_status

    @risk_process_status.setter
    def risk_process_status(self, risk_process_status):
        """Sets the risk_process_status of this RiskBaseInfoForGetRiskOutput.


        :param risk_process_status: The risk_process_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._risk_process_status = risk_process_status

    @property
    def risk_status(self):
        """Gets the risk_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._risk_status

    @risk_status.setter
    def risk_status(self, risk_status):
        """Sets the risk_status of this RiskBaseInfoForGetRiskOutput.


        :param risk_status: The risk_status of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._risk_status = risk_status

    @property
    def risk_types(self):
        """Gets the risk_types of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The risk_types of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._risk_types

    @risk_types.setter
    def risk_types(self, risk_types):
        """Sets the risk_types of this RiskBaseInfoForGetRiskOutput.


        :param risk_types: The risk_types of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: list[str]
        """

        self._risk_types = risk_types

    @property
    def support_repair(self):
        """Gets the support_repair of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The support_repair of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: bool
        """
        return self._support_repair

    @support_repair.setter
    def support_repair(self, support_repair):
        """Sets the support_repair of this RiskBaseInfoForGetRiskOutput.


        :param support_repair: The support_repair of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: bool
        """

        self._support_repair = support_repair

    @property
    def support_verify(self):
        """Gets the support_verify of this RiskBaseInfoForGetRiskOutput.  # noqa: E501


        :return: The support_verify of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :rtype: bool
        """
        return self._support_verify

    @support_verify.setter
    def support_verify(self, support_verify):
        """Sets the support_verify of this RiskBaseInfoForGetRiskOutput.


        :param support_verify: The support_verify of this RiskBaseInfoForGetRiskOutput.  # noqa: E501
        :type: bool
        """

        self._support_verify = support_verify

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
        if issubclass(RiskBaseInfoForGetRiskOutput, dict):
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
        if not isinstance(other, RiskBaseInfoForGetRiskOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RiskBaseInfoForGetRiskOutput):
            return True

        return self.to_dict() != other.to_dict()
