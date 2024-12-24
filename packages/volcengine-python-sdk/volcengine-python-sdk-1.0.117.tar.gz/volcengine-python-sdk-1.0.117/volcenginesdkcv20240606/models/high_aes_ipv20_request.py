# coding: utf-8

"""
    cv20240606

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class HighAesIPV20Request(object):
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
        'binary_data_base64': 'list[str]',
        'cfg_rescale': 'float',
        'ddim_steps': 'int',
        'height': 'int',
        'image_urls': 'list[str]',
        'logo_info': 'LogoInfoForHighAesIPV20Input',
        'prompt': 'str',
        'ref_id_weight': 'float',
        'ref_ip_weight': 'float',
        'req_key': 'str',
        'return_url': 'bool',
        'scale': 'float',
        'seed': 'int',
        'use_sr': 'bool',
        'width': 'int'
    }

    attribute_map = {
        'binary_data_base64': 'binary_data_base64',
        'cfg_rescale': 'cfg_rescale',
        'ddim_steps': 'ddim_steps',
        'height': 'height',
        'image_urls': 'image_urls',
        'logo_info': 'logo_info',
        'prompt': 'prompt',
        'ref_id_weight': 'ref_id_weight',
        'ref_ip_weight': 'ref_ip_weight',
        'req_key': 'req_key',
        'return_url': 'return_url',
        'scale': 'scale',
        'seed': 'seed',
        'use_sr': 'use_sr',
        'width': 'width'
    }

    def __init__(self, binary_data_base64=None, cfg_rescale=None, ddim_steps=None, height=None, image_urls=None, logo_info=None, prompt=None, ref_id_weight=None, ref_ip_weight=None, req_key=None, return_url=None, scale=None, seed=None, use_sr=None, width=None, _configuration=None):  # noqa: E501
        """HighAesIPV20Request - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._binary_data_base64 = None
        self._cfg_rescale = None
        self._ddim_steps = None
        self._height = None
        self._image_urls = None
        self._logo_info = None
        self._prompt = None
        self._ref_id_weight = None
        self._ref_ip_weight = None
        self._req_key = None
        self._return_url = None
        self._scale = None
        self._seed = None
        self._use_sr = None
        self._width = None
        self.discriminator = None

        if binary_data_base64 is not None:
            self.binary_data_base64 = binary_data_base64
        if cfg_rescale is not None:
            self.cfg_rescale = cfg_rescale
        if ddim_steps is not None:
            self.ddim_steps = ddim_steps
        if height is not None:
            self.height = height
        if image_urls is not None:
            self.image_urls = image_urls
        if logo_info is not None:
            self.logo_info = logo_info
        self.prompt = prompt
        if ref_id_weight is not None:
            self.ref_id_weight = ref_id_weight
        if ref_ip_weight is not None:
            self.ref_ip_weight = ref_ip_weight
        self.req_key = req_key
        if return_url is not None:
            self.return_url = return_url
        if scale is not None:
            self.scale = scale
        if seed is not None:
            self.seed = seed
        if use_sr is not None:
            self.use_sr = use_sr
        if width is not None:
            self.width = width

    @property
    def binary_data_base64(self):
        """Gets the binary_data_base64 of this HighAesIPV20Request.  # noqa: E501


        :return: The binary_data_base64 of this HighAesIPV20Request.  # noqa: E501
        :rtype: list[str]
        """
        return self._binary_data_base64

    @binary_data_base64.setter
    def binary_data_base64(self, binary_data_base64):
        """Sets the binary_data_base64 of this HighAesIPV20Request.


        :param binary_data_base64: The binary_data_base64 of this HighAesIPV20Request.  # noqa: E501
        :type: list[str]
        """

        self._binary_data_base64 = binary_data_base64

    @property
    def cfg_rescale(self):
        """Gets the cfg_rescale of this HighAesIPV20Request.  # noqa: E501


        :return: The cfg_rescale of this HighAesIPV20Request.  # noqa: E501
        :rtype: float
        """
        return self._cfg_rescale

    @cfg_rescale.setter
    def cfg_rescale(self, cfg_rescale):
        """Sets the cfg_rescale of this HighAesIPV20Request.


        :param cfg_rescale: The cfg_rescale of this HighAesIPV20Request.  # noqa: E501
        :type: float
        """

        self._cfg_rescale = cfg_rescale

    @property
    def ddim_steps(self):
        """Gets the ddim_steps of this HighAesIPV20Request.  # noqa: E501


        :return: The ddim_steps of this HighAesIPV20Request.  # noqa: E501
        :rtype: int
        """
        return self._ddim_steps

    @ddim_steps.setter
    def ddim_steps(self, ddim_steps):
        """Sets the ddim_steps of this HighAesIPV20Request.


        :param ddim_steps: The ddim_steps of this HighAesIPV20Request.  # noqa: E501
        :type: int
        """

        self._ddim_steps = ddim_steps

    @property
    def height(self):
        """Gets the height of this HighAesIPV20Request.  # noqa: E501


        :return: The height of this HighAesIPV20Request.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this HighAesIPV20Request.


        :param height: The height of this HighAesIPV20Request.  # noqa: E501
        :type: int
        """

        self._height = height

    @property
    def image_urls(self):
        """Gets the image_urls of this HighAesIPV20Request.  # noqa: E501


        :return: The image_urls of this HighAesIPV20Request.  # noqa: E501
        :rtype: list[str]
        """
        return self._image_urls

    @image_urls.setter
    def image_urls(self, image_urls):
        """Sets the image_urls of this HighAesIPV20Request.


        :param image_urls: The image_urls of this HighAesIPV20Request.  # noqa: E501
        :type: list[str]
        """

        self._image_urls = image_urls

    @property
    def logo_info(self):
        """Gets the logo_info of this HighAesIPV20Request.  # noqa: E501


        :return: The logo_info of this HighAesIPV20Request.  # noqa: E501
        :rtype: LogoInfoForHighAesIPV20Input
        """
        return self._logo_info

    @logo_info.setter
    def logo_info(self, logo_info):
        """Sets the logo_info of this HighAesIPV20Request.


        :param logo_info: The logo_info of this HighAesIPV20Request.  # noqa: E501
        :type: LogoInfoForHighAesIPV20Input
        """

        self._logo_info = logo_info

    @property
    def prompt(self):
        """Gets the prompt of this HighAesIPV20Request.  # noqa: E501


        :return: The prompt of this HighAesIPV20Request.  # noqa: E501
        :rtype: str
        """
        return self._prompt

    @prompt.setter
    def prompt(self, prompt):
        """Sets the prompt of this HighAesIPV20Request.


        :param prompt: The prompt of this HighAesIPV20Request.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and prompt is None:
            raise ValueError("Invalid value for `prompt`, must not be `None`")  # noqa: E501

        self._prompt = prompt

    @property
    def ref_id_weight(self):
        """Gets the ref_id_weight of this HighAesIPV20Request.  # noqa: E501


        :return: The ref_id_weight of this HighAesIPV20Request.  # noqa: E501
        :rtype: float
        """
        return self._ref_id_weight

    @ref_id_weight.setter
    def ref_id_weight(self, ref_id_weight):
        """Sets the ref_id_weight of this HighAesIPV20Request.


        :param ref_id_weight: The ref_id_weight of this HighAesIPV20Request.  # noqa: E501
        :type: float
        """

        self._ref_id_weight = ref_id_weight

    @property
    def ref_ip_weight(self):
        """Gets the ref_ip_weight of this HighAesIPV20Request.  # noqa: E501


        :return: The ref_ip_weight of this HighAesIPV20Request.  # noqa: E501
        :rtype: float
        """
        return self._ref_ip_weight

    @ref_ip_weight.setter
    def ref_ip_weight(self, ref_ip_weight):
        """Sets the ref_ip_weight of this HighAesIPV20Request.


        :param ref_ip_weight: The ref_ip_weight of this HighAesIPV20Request.  # noqa: E501
        :type: float
        """

        self._ref_ip_weight = ref_ip_weight

    @property
    def req_key(self):
        """Gets the req_key of this HighAesIPV20Request.  # noqa: E501


        :return: The req_key of this HighAesIPV20Request.  # noqa: E501
        :rtype: str
        """
        return self._req_key

    @req_key.setter
    def req_key(self, req_key):
        """Sets the req_key of this HighAesIPV20Request.


        :param req_key: The req_key of this HighAesIPV20Request.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and req_key is None:
            raise ValueError("Invalid value for `req_key`, must not be `None`")  # noqa: E501

        self._req_key = req_key

    @property
    def return_url(self):
        """Gets the return_url of this HighAesIPV20Request.  # noqa: E501


        :return: The return_url of this HighAesIPV20Request.  # noqa: E501
        :rtype: bool
        """
        return self._return_url

    @return_url.setter
    def return_url(self, return_url):
        """Sets the return_url of this HighAesIPV20Request.


        :param return_url: The return_url of this HighAesIPV20Request.  # noqa: E501
        :type: bool
        """

        self._return_url = return_url

    @property
    def scale(self):
        """Gets the scale of this HighAesIPV20Request.  # noqa: E501


        :return: The scale of this HighAesIPV20Request.  # noqa: E501
        :rtype: float
        """
        return self._scale

    @scale.setter
    def scale(self, scale):
        """Sets the scale of this HighAesIPV20Request.


        :param scale: The scale of this HighAesIPV20Request.  # noqa: E501
        :type: float
        """

        self._scale = scale

    @property
    def seed(self):
        """Gets the seed of this HighAesIPV20Request.  # noqa: E501


        :return: The seed of this HighAesIPV20Request.  # noqa: E501
        :rtype: int
        """
        return self._seed

    @seed.setter
    def seed(self, seed):
        """Sets the seed of this HighAesIPV20Request.


        :param seed: The seed of this HighAesIPV20Request.  # noqa: E501
        :type: int
        """

        self._seed = seed

    @property
    def use_sr(self):
        """Gets the use_sr of this HighAesIPV20Request.  # noqa: E501


        :return: The use_sr of this HighAesIPV20Request.  # noqa: E501
        :rtype: bool
        """
        return self._use_sr

    @use_sr.setter
    def use_sr(self, use_sr):
        """Sets the use_sr of this HighAesIPV20Request.


        :param use_sr: The use_sr of this HighAesIPV20Request.  # noqa: E501
        :type: bool
        """

        self._use_sr = use_sr

    @property
    def width(self):
        """Gets the width of this HighAesIPV20Request.  # noqa: E501


        :return: The width of this HighAesIPV20Request.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this HighAesIPV20Request.


        :param width: The width of this HighAesIPV20Request.  # noqa: E501
        :type: int
        """

        self._width = width

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
        if issubclass(HighAesIPV20Request, dict):
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
        if not isinstance(other, HighAesIPV20Request):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HighAesIPV20Request):
            return True

        return self.to_dict() != other.to_dict()
