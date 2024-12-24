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


class CreateRouteTableRequest(object):
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
        'client_token': 'str',
        'description': 'str',
        'project_name': 'str',
        'route_table_name': 'str',
        'tags': 'list[TagForCreateRouteTableInput]',
        'vpc_id': 'str'
    }

    attribute_map = {
        'client_token': 'ClientToken',
        'description': 'Description',
        'project_name': 'ProjectName',
        'route_table_name': 'RouteTableName',
        'tags': 'Tags',
        'vpc_id': 'VpcId'
    }

    def __init__(self, client_token=None, description=None, project_name=None, route_table_name=None, tags=None, vpc_id=None, _configuration=None):  # noqa: E501
        """CreateRouteTableRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._client_token = None
        self._description = None
        self._project_name = None
        self._route_table_name = None
        self._tags = None
        self._vpc_id = None
        self.discriminator = None

        if client_token is not None:
            self.client_token = client_token
        if description is not None:
            self.description = description
        if project_name is not None:
            self.project_name = project_name
        if route_table_name is not None:
            self.route_table_name = route_table_name
        if tags is not None:
            self.tags = tags
        self.vpc_id = vpc_id

    @property
    def client_token(self):
        """Gets the client_token of this CreateRouteTableRequest.  # noqa: E501


        :return: The client_token of this CreateRouteTableRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this CreateRouteTableRequest.


        :param client_token: The client_token of this CreateRouteTableRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def description(self):
        """Gets the description of this CreateRouteTableRequest.  # noqa: E501


        :return: The description of this CreateRouteTableRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateRouteTableRequest.


        :param description: The description of this CreateRouteTableRequest.  # noqa: E501
        :type: str
        """
        if (self._configuration.client_side_validation and
                description is not None and len(description) > 255):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `255`")  # noqa: E501
        if (self._configuration.client_side_validation and
                description is not None and len(description) < 1):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501

        self._description = description

    @property
    def project_name(self):
        """Gets the project_name of this CreateRouteTableRequest.  # noqa: E501


        :return: The project_name of this CreateRouteTableRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this CreateRouteTableRequest.


        :param project_name: The project_name of this CreateRouteTableRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def route_table_name(self):
        """Gets the route_table_name of this CreateRouteTableRequest.  # noqa: E501


        :return: The route_table_name of this CreateRouteTableRequest.  # noqa: E501
        :rtype: str
        """
        return self._route_table_name

    @route_table_name.setter
    def route_table_name(self, route_table_name):
        """Sets the route_table_name of this CreateRouteTableRequest.


        :param route_table_name: The route_table_name of this CreateRouteTableRequest.  # noqa: E501
        :type: str
        """
        if (self._configuration.client_side_validation and
                route_table_name is not None and len(route_table_name) > 128):
            raise ValueError("Invalid value for `route_table_name`, length must be less than or equal to `128`")  # noqa: E501
        if (self._configuration.client_side_validation and
                route_table_name is not None and len(route_table_name) < 1):
            raise ValueError("Invalid value for `route_table_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._route_table_name = route_table_name

    @property
    def tags(self):
        """Gets the tags of this CreateRouteTableRequest.  # noqa: E501


        :return: The tags of this CreateRouteTableRequest.  # noqa: E501
        :rtype: list[TagForCreateRouteTableInput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateRouteTableRequest.


        :param tags: The tags of this CreateRouteTableRequest.  # noqa: E501
        :type: list[TagForCreateRouteTableInput]
        """

        self._tags = tags

    @property
    def vpc_id(self):
        """Gets the vpc_id of this CreateRouteTableRequest.  # noqa: E501


        :return: The vpc_id of this CreateRouteTableRequest.  # noqa: E501
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this CreateRouteTableRequest.


        :param vpc_id: The vpc_id of this CreateRouteTableRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and vpc_id is None:
            raise ValueError("Invalid value for `vpc_id`, must not be `None`")  # noqa: E501

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
        if issubclass(CreateRouteTableRequest, dict):
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
        if not isinstance(other, CreateRouteTableRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateRouteTableRequest):
            return True

        return self.to_dict() != other.to_dict()
