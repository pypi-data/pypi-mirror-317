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


class SecurityGroupRuleInfoForGetRiskOutput(object):
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
        'policy': 'str',
        'port_range_infos': 'list[PortRangeInfoForGetRiskOutput]',
        'priority': 'int',
        'protocol_type': 'str',
        'security_group_name': 'str',
        'security_group_rule_uid': 'str',
        'security_group_uid': 'str',
        'serivce_name_cn': 'str',
        'serivce_name_en': 'str',
        'srouce_cidr_ip': 'str',
        'srouce_ip_type': 'str'
    }

    attribute_map = {
        'policy': 'Policy',
        'port_range_infos': 'PortRangeInfos',
        'priority': 'Priority',
        'protocol_type': 'ProtocolType',
        'security_group_name': 'SecurityGroupName',
        'security_group_rule_uid': 'SecurityGroupRuleUID',
        'security_group_uid': 'SecurityGroupUID',
        'serivce_name_cn': 'SerivceNameCN',
        'serivce_name_en': 'SerivceNameEN',
        'srouce_cidr_ip': 'SrouceCidrIP',
        'srouce_ip_type': 'SrouceIPType'
    }

    def __init__(self, policy=None, port_range_infos=None, priority=None, protocol_type=None, security_group_name=None, security_group_rule_uid=None, security_group_uid=None, serivce_name_cn=None, serivce_name_en=None, srouce_cidr_ip=None, srouce_ip_type=None, _configuration=None):  # noqa: E501
        """SecurityGroupRuleInfoForGetRiskOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._policy = None
        self._port_range_infos = None
        self._priority = None
        self._protocol_type = None
        self._security_group_name = None
        self._security_group_rule_uid = None
        self._security_group_uid = None
        self._serivce_name_cn = None
        self._serivce_name_en = None
        self._srouce_cidr_ip = None
        self._srouce_ip_type = None
        self.discriminator = None

        if policy is not None:
            self.policy = policy
        if port_range_infos is not None:
            self.port_range_infos = port_range_infos
        if priority is not None:
            self.priority = priority
        if protocol_type is not None:
            self.protocol_type = protocol_type
        if security_group_name is not None:
            self.security_group_name = security_group_name
        if security_group_rule_uid is not None:
            self.security_group_rule_uid = security_group_rule_uid
        if security_group_uid is not None:
            self.security_group_uid = security_group_uid
        if serivce_name_cn is not None:
            self.serivce_name_cn = serivce_name_cn
        if serivce_name_en is not None:
            self.serivce_name_en = serivce_name_en
        if srouce_cidr_ip is not None:
            self.srouce_cidr_ip = srouce_cidr_ip
        if srouce_ip_type is not None:
            self.srouce_ip_type = srouce_ip_type

    @property
    def policy(self):
        """Gets the policy of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The policy of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """Sets the policy of this SecurityGroupRuleInfoForGetRiskOutput.


        :param policy: The policy of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._policy = policy

    @property
    def port_range_infos(self):
        """Gets the port_range_infos of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The port_range_infos of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: list[PortRangeInfoForGetRiskOutput]
        """
        return self._port_range_infos

    @port_range_infos.setter
    def port_range_infos(self, port_range_infos):
        """Sets the port_range_infos of this SecurityGroupRuleInfoForGetRiskOutput.


        :param port_range_infos: The port_range_infos of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: list[PortRangeInfoForGetRiskOutput]
        """

        self._port_range_infos = port_range_infos

    @property
    def priority(self):
        """Gets the priority of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The priority of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this SecurityGroupRuleInfoForGetRiskOutput.


        :param priority: The priority of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def protocol_type(self):
        """Gets the protocol_type of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The protocol_type of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._protocol_type

    @protocol_type.setter
    def protocol_type(self, protocol_type):
        """Sets the protocol_type of this SecurityGroupRuleInfoForGetRiskOutput.


        :param protocol_type: The protocol_type of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._protocol_type = protocol_type

    @property
    def security_group_name(self):
        """Gets the security_group_name of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The security_group_name of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._security_group_name

    @security_group_name.setter
    def security_group_name(self, security_group_name):
        """Sets the security_group_name of this SecurityGroupRuleInfoForGetRiskOutput.


        :param security_group_name: The security_group_name of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._security_group_name = security_group_name

    @property
    def security_group_rule_uid(self):
        """Gets the security_group_rule_uid of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The security_group_rule_uid of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._security_group_rule_uid

    @security_group_rule_uid.setter
    def security_group_rule_uid(self, security_group_rule_uid):
        """Sets the security_group_rule_uid of this SecurityGroupRuleInfoForGetRiskOutput.


        :param security_group_rule_uid: The security_group_rule_uid of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._security_group_rule_uid = security_group_rule_uid

    @property
    def security_group_uid(self):
        """Gets the security_group_uid of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The security_group_uid of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._security_group_uid

    @security_group_uid.setter
    def security_group_uid(self, security_group_uid):
        """Sets the security_group_uid of this SecurityGroupRuleInfoForGetRiskOutput.


        :param security_group_uid: The security_group_uid of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._security_group_uid = security_group_uid

    @property
    def serivce_name_cn(self):
        """Gets the serivce_name_cn of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The serivce_name_cn of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._serivce_name_cn

    @serivce_name_cn.setter
    def serivce_name_cn(self, serivce_name_cn):
        """Sets the serivce_name_cn of this SecurityGroupRuleInfoForGetRiskOutput.


        :param serivce_name_cn: The serivce_name_cn of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._serivce_name_cn = serivce_name_cn

    @property
    def serivce_name_en(self):
        """Gets the serivce_name_en of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The serivce_name_en of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._serivce_name_en

    @serivce_name_en.setter
    def serivce_name_en(self, serivce_name_en):
        """Sets the serivce_name_en of this SecurityGroupRuleInfoForGetRiskOutput.


        :param serivce_name_en: The serivce_name_en of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._serivce_name_en = serivce_name_en

    @property
    def srouce_cidr_ip(self):
        """Gets the srouce_cidr_ip of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The srouce_cidr_ip of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._srouce_cidr_ip

    @srouce_cidr_ip.setter
    def srouce_cidr_ip(self, srouce_cidr_ip):
        """Sets the srouce_cidr_ip of this SecurityGroupRuleInfoForGetRiskOutput.


        :param srouce_cidr_ip: The srouce_cidr_ip of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._srouce_cidr_ip = srouce_cidr_ip

    @property
    def srouce_ip_type(self):
        """Gets the srouce_ip_type of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501


        :return: The srouce_ip_type of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._srouce_ip_type

    @srouce_ip_type.setter
    def srouce_ip_type(self, srouce_ip_type):
        """Sets the srouce_ip_type of this SecurityGroupRuleInfoForGetRiskOutput.


        :param srouce_ip_type: The srouce_ip_type of this SecurityGroupRuleInfoForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._srouce_ip_type = srouce_ip_type

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
        if issubclass(SecurityGroupRuleInfoForGetRiskOutput, dict):
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
        if not isinstance(other, SecurityGroupRuleInfoForGetRiskOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SecurityGroupRuleInfoForGetRiskOutput):
            return True

        return self.to_dict() != other.to_dict()
