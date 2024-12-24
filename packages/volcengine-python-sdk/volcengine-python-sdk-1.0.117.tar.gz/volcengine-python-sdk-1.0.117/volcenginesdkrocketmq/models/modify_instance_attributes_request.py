# coding: utf-8

"""
    rocketmq

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ModifyInstanceAttributesRequest(object):
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
        'instance_description': 'str',
        'instance_id': 'str',
        'instance_name': 'str',
        'product_info': 'ProductInfoForModifyInstanceAttributesInput'
    }

    attribute_map = {
        'instance_description': 'InstanceDescription',
        'instance_id': 'InstanceId',
        'instance_name': 'InstanceName',
        'product_info': 'ProductInfo'
    }

    def __init__(self, instance_description=None, instance_id=None, instance_name=None, product_info=None, _configuration=None):  # noqa: E501
        """ModifyInstanceAttributesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._instance_description = None
        self._instance_id = None
        self._instance_name = None
        self._product_info = None
        self.discriminator = None

        if instance_description is not None:
            self.instance_description = instance_description
        self.instance_id = instance_id
        if instance_name is not None:
            self.instance_name = instance_name
        if product_info is not None:
            self.product_info = product_info

    @property
    def instance_description(self):
        """Gets the instance_description of this ModifyInstanceAttributesRequest.  # noqa: E501


        :return: The instance_description of this ModifyInstanceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_description

    @instance_description.setter
    def instance_description(self, instance_description):
        """Sets the instance_description of this ModifyInstanceAttributesRequest.


        :param instance_description: The instance_description of this ModifyInstanceAttributesRequest.  # noqa: E501
        :type: str
        """

        self._instance_description = instance_description

    @property
    def instance_id(self):
        """Gets the instance_id of this ModifyInstanceAttributesRequest.  # noqa: E501


        :return: The instance_id of this ModifyInstanceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ModifyInstanceAttributesRequest.


        :param instance_id: The instance_id of this ModifyInstanceAttributesRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def instance_name(self):
        """Gets the instance_name of this ModifyInstanceAttributesRequest.  # noqa: E501


        :return: The instance_name of this ModifyInstanceAttributesRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """Sets the instance_name of this ModifyInstanceAttributesRequest.


        :param instance_name: The instance_name of this ModifyInstanceAttributesRequest.  # noqa: E501
        :type: str
        """

        self._instance_name = instance_name

    @property
    def product_info(self):
        """Gets the product_info of this ModifyInstanceAttributesRequest.  # noqa: E501


        :return: The product_info of this ModifyInstanceAttributesRequest.  # noqa: E501
        :rtype: ProductInfoForModifyInstanceAttributesInput
        """
        return self._product_info

    @product_info.setter
    def product_info(self, product_info):
        """Sets the product_info of this ModifyInstanceAttributesRequest.


        :param product_info: The product_info of this ModifyInstanceAttributesRequest.  # noqa: E501
        :type: ProductInfoForModifyInstanceAttributesInput
        """

        self._product_info = product_info

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
        if issubclass(ModifyInstanceAttributesRequest, dict):
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
        if not isinstance(other, ModifyInstanceAttributesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyInstanceAttributesRequest):
            return True

        return self.to_dict() != other.to_dict()
