# coding: utf-8

"""
    mcdn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DomainForListCdnDomainsOutput(object):
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
        'biz_node_id': 'str',
        'biz_node_name': 'str',
        'biz_node_path': 'str',
        'cdn_type': 'str',
        'certificates': 'list[CertificateForListCdnDomainsOutput]',
        'cloud_account_id': 'str',
        'cloud_account_name': 'str',
        'cname': 'str',
        'created_at': 'str',
        'id': 'str',
        'imported_at': 'str',
        'name': 'str',
        'networks': 'list[NetworkForListCdnDomainsOutput]',
        'region': 'str',
        'schedule_created': 'bool',
        'status': 'str',
        'sub_product': 'str',
        'synced_at': 'str',
        'tags': 'list[TagForListCdnDomainsOutput]',
        'top_account_id': 'str',
        'updated_at': 'str',
        'vendor': 'str',
        'vendor_id': 'str'
    }

    attribute_map = {
        'biz_node_id': 'BizNodeId',
        'biz_node_name': 'BizNodeName',
        'biz_node_path': 'BizNodePath',
        'cdn_type': 'CdnType',
        'certificates': 'Certificates',
        'cloud_account_id': 'CloudAccountId',
        'cloud_account_name': 'CloudAccountName',
        'cname': 'Cname',
        'created_at': 'CreatedAt',
        'id': 'Id',
        'imported_at': 'ImportedAt',
        'name': 'Name',
        'networks': 'Networks',
        'region': 'Region',
        'schedule_created': 'ScheduleCreated',
        'status': 'Status',
        'sub_product': 'SubProduct',
        'synced_at': 'SyncedAt',
        'tags': 'Tags',
        'top_account_id': 'TopAccountId',
        'updated_at': 'UpdatedAt',
        'vendor': 'Vendor',
        'vendor_id': 'VendorId'
    }

    def __init__(self, biz_node_id=None, biz_node_name=None, biz_node_path=None, cdn_type=None, certificates=None, cloud_account_id=None, cloud_account_name=None, cname=None, created_at=None, id=None, imported_at=None, name=None, networks=None, region=None, schedule_created=None, status=None, sub_product=None, synced_at=None, tags=None, top_account_id=None, updated_at=None, vendor=None, vendor_id=None, _configuration=None):  # noqa: E501
        """DomainForListCdnDomainsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._biz_node_id = None
        self._biz_node_name = None
        self._biz_node_path = None
        self._cdn_type = None
        self._certificates = None
        self._cloud_account_id = None
        self._cloud_account_name = None
        self._cname = None
        self._created_at = None
        self._id = None
        self._imported_at = None
        self._name = None
        self._networks = None
        self._region = None
        self._schedule_created = None
        self._status = None
        self._sub_product = None
        self._synced_at = None
        self._tags = None
        self._top_account_id = None
        self._updated_at = None
        self._vendor = None
        self._vendor_id = None
        self.discriminator = None

        if biz_node_id is not None:
            self.biz_node_id = biz_node_id
        if biz_node_name is not None:
            self.biz_node_name = biz_node_name
        if biz_node_path is not None:
            self.biz_node_path = biz_node_path
        if cdn_type is not None:
            self.cdn_type = cdn_type
        if certificates is not None:
            self.certificates = certificates
        if cloud_account_id is not None:
            self.cloud_account_id = cloud_account_id
        if cloud_account_name is not None:
            self.cloud_account_name = cloud_account_name
        if cname is not None:
            self.cname = cname
        if created_at is not None:
            self.created_at = created_at
        if id is not None:
            self.id = id
        if imported_at is not None:
            self.imported_at = imported_at
        if name is not None:
            self.name = name
        if networks is not None:
            self.networks = networks
        if region is not None:
            self.region = region
        if schedule_created is not None:
            self.schedule_created = schedule_created
        if status is not None:
            self.status = status
        if sub_product is not None:
            self.sub_product = sub_product
        if synced_at is not None:
            self.synced_at = synced_at
        if tags is not None:
            self.tags = tags
        if top_account_id is not None:
            self.top_account_id = top_account_id
        if updated_at is not None:
            self.updated_at = updated_at
        if vendor is not None:
            self.vendor = vendor
        if vendor_id is not None:
            self.vendor_id = vendor_id

    @property
    def biz_node_id(self):
        """Gets the biz_node_id of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The biz_node_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._biz_node_id

    @biz_node_id.setter
    def biz_node_id(self, biz_node_id):
        """Sets the biz_node_id of this DomainForListCdnDomainsOutput.


        :param biz_node_id: The biz_node_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._biz_node_id = biz_node_id

    @property
    def biz_node_name(self):
        """Gets the biz_node_name of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The biz_node_name of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._biz_node_name

    @biz_node_name.setter
    def biz_node_name(self, biz_node_name):
        """Sets the biz_node_name of this DomainForListCdnDomainsOutput.


        :param biz_node_name: The biz_node_name of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._biz_node_name = biz_node_name

    @property
    def biz_node_path(self):
        """Gets the biz_node_path of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The biz_node_path of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._biz_node_path

    @biz_node_path.setter
    def biz_node_path(self, biz_node_path):
        """Sets the biz_node_path of this DomainForListCdnDomainsOutput.


        :param biz_node_path: The biz_node_path of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._biz_node_path = biz_node_path

    @property
    def cdn_type(self):
        """Gets the cdn_type of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The cdn_type of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._cdn_type

    @cdn_type.setter
    def cdn_type(self, cdn_type):
        """Sets the cdn_type of this DomainForListCdnDomainsOutput.


        :param cdn_type: The cdn_type of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._cdn_type = cdn_type

    @property
    def certificates(self):
        """Gets the certificates of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The certificates of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: list[CertificateForListCdnDomainsOutput]
        """
        return self._certificates

    @certificates.setter
    def certificates(self, certificates):
        """Sets the certificates of this DomainForListCdnDomainsOutput.


        :param certificates: The certificates of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: list[CertificateForListCdnDomainsOutput]
        """

        self._certificates = certificates

    @property
    def cloud_account_id(self):
        """Gets the cloud_account_id of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The cloud_account_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._cloud_account_id

    @cloud_account_id.setter
    def cloud_account_id(self, cloud_account_id):
        """Sets the cloud_account_id of this DomainForListCdnDomainsOutput.


        :param cloud_account_id: The cloud_account_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._cloud_account_id = cloud_account_id

    @property
    def cloud_account_name(self):
        """Gets the cloud_account_name of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The cloud_account_name of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._cloud_account_name

    @cloud_account_name.setter
    def cloud_account_name(self, cloud_account_name):
        """Sets the cloud_account_name of this DomainForListCdnDomainsOutput.


        :param cloud_account_name: The cloud_account_name of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._cloud_account_name = cloud_account_name

    @property
    def cname(self):
        """Gets the cname of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The cname of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._cname

    @cname.setter
    def cname(self, cname):
        """Sets the cname of this DomainForListCdnDomainsOutput.


        :param cname: The cname of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._cname = cname

    @property
    def created_at(self):
        """Gets the created_at of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The created_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DomainForListCdnDomainsOutput.


        :param created_at: The created_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def id(self):
        """Gets the id of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DomainForListCdnDomainsOutput.


        :param id: The id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def imported_at(self):
        """Gets the imported_at of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The imported_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._imported_at

    @imported_at.setter
    def imported_at(self, imported_at):
        """Sets the imported_at of this DomainForListCdnDomainsOutput.


        :param imported_at: The imported_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._imported_at = imported_at

    @property
    def name(self):
        """Gets the name of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The name of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DomainForListCdnDomainsOutput.


        :param name: The name of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def networks(self):
        """Gets the networks of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The networks of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: list[NetworkForListCdnDomainsOutput]
        """
        return self._networks

    @networks.setter
    def networks(self, networks):
        """Sets the networks of this DomainForListCdnDomainsOutput.


        :param networks: The networks of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: list[NetworkForListCdnDomainsOutput]
        """

        self._networks = networks

    @property
    def region(self):
        """Gets the region of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The region of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this DomainForListCdnDomainsOutput.


        :param region: The region of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def schedule_created(self):
        """Gets the schedule_created of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The schedule_created of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: bool
        """
        return self._schedule_created

    @schedule_created.setter
    def schedule_created(self, schedule_created):
        """Sets the schedule_created of this DomainForListCdnDomainsOutput.


        :param schedule_created: The schedule_created of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: bool
        """

        self._schedule_created = schedule_created

    @property
    def status(self):
        """Gets the status of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The status of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DomainForListCdnDomainsOutput.


        :param status: The status of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def sub_product(self):
        """Gets the sub_product of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The sub_product of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._sub_product

    @sub_product.setter
    def sub_product(self, sub_product):
        """Sets the sub_product of this DomainForListCdnDomainsOutput.


        :param sub_product: The sub_product of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._sub_product = sub_product

    @property
    def synced_at(self):
        """Gets the synced_at of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The synced_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._synced_at

    @synced_at.setter
    def synced_at(self, synced_at):
        """Sets the synced_at of this DomainForListCdnDomainsOutput.


        :param synced_at: The synced_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._synced_at = synced_at

    @property
    def tags(self):
        """Gets the tags of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The tags of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: list[TagForListCdnDomainsOutput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this DomainForListCdnDomainsOutput.


        :param tags: The tags of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: list[TagForListCdnDomainsOutput]
        """

        self._tags = tags

    @property
    def top_account_id(self):
        """Gets the top_account_id of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The top_account_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._top_account_id

    @top_account_id.setter
    def top_account_id(self, top_account_id):
        """Sets the top_account_id of this DomainForListCdnDomainsOutput.


        :param top_account_id: The top_account_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._top_account_id = top_account_id

    @property
    def updated_at(self):
        """Gets the updated_at of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The updated_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this DomainForListCdnDomainsOutput.


        :param updated_at: The updated_at of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

    @property
    def vendor(self):
        """Gets the vendor of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The vendor of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor):
        """Sets the vendor of this DomainForListCdnDomainsOutput.


        :param vendor: The vendor of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._vendor = vendor

    @property
    def vendor_id(self):
        """Gets the vendor_id of this DomainForListCdnDomainsOutput.  # noqa: E501


        :return: The vendor_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :rtype: str
        """
        return self._vendor_id

    @vendor_id.setter
    def vendor_id(self, vendor_id):
        """Sets the vendor_id of this DomainForListCdnDomainsOutput.


        :param vendor_id: The vendor_id of this DomainForListCdnDomainsOutput.  # noqa: E501
        :type: str
        """

        self._vendor_id = vendor_id

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
        if issubclass(DomainForListCdnDomainsOutput, dict):
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
        if not isinstance(other, DomainForListCdnDomainsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DomainForListCdnDomainsOutput):
            return True

        return self.to_dict() != other.to_dict()
