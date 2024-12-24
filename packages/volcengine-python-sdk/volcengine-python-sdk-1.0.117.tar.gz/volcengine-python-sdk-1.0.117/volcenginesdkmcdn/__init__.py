# coding: utf-8

# flake8: noqa

"""
    mcdn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

# import apis into sdk package
from volcenginesdkmcdn.api.mcdn_api import MCDNApi

# import models into sdk package
from volcenginesdkmcdn.models.active_weight_for_describe_dns_schedule_active_weights_output import ActiveWeightForDescribeDnsScheduleActiveWeightsOutput
from volcenginesdkmcdn.models.add_dns_schedule_static_weight_request import AddDnsScheduleStaticWeightRequest
from volcenginesdkmcdn.models.add_dns_schedule_static_weight_response import AddDnsScheduleStaticWeightResponse
from volcenginesdkmcdn.models.alert_rule_for_describe_alert_strategy_output import AlertRuleForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.alert_rule_for_list_alert_strategies_output import AlertRuleForListAlertStrategiesOutput
from volcenginesdkmcdn.models.alert_strategy_for_describe_alert_strategy_output import AlertStrategyForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.aws_for_list_cloud_accounts_output import AwsForListCloudAccountsOutput
from volcenginesdkmcdn.models.certificate_for_list_cdn_domains_output import CertificateForListCdnDomainsOutput
from volcenginesdkmcdn.models.child_for_list_alert_meta_metrics_output import ChildForListAlertMetaMetricsOutput
from volcenginesdkmcdn.models.cloud_account_for_list_cloud_accounts_output import CloudAccountForListCloudAccountsOutput
from volcenginesdkmcdn.models.condition_for_describe_alert_strategy_output import ConditionForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.condition_for_list_alert_strategies_output import ConditionForListAlertStrategiesOutput
from volcenginesdkmcdn.models.contact_group_for_describe_alert_strategy_output import ContactGroupForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.contact_group_for_list_alert_strategies_output import ContactGroupForListAlertStrategiesOutput
from volcenginesdkmcdn.models.contact_robot_for_describe_alert_strategy_output import ContactRobotForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.contact_robot_for_list_alert_strategies_output import ContactRobotForListAlertStrategiesOutput
from volcenginesdkmcdn.models.content_settings_for_list_cloud_accounts_output import ContentSettingsForListCloudAccountsOutput
from volcenginesdkmcdn.models.convert_aws_for_list_cloud_accounts_output import ConvertAwsForListCloudAccountsOutput
from volcenginesdkmcdn.models.country_for_describe_cdn_region_and_isp_output import CountryForDescribeCdnRegionAndIspOutput
from volcenginesdkmcdn.models.country_for_list_views_output import CountryForListViewsOutput
from volcenginesdkmcdn.models.data_for_list_alert_meta_metrics_output import DataForListAlertMetaMetricsOutput
from volcenginesdkmcdn.models.data_for_list_alert_strategies_output import DataForListAlertStrategiesOutput
from volcenginesdkmcdn.models.delete_dns_schedule_static_weight_request import DeleteDnsScheduleStaticWeightRequest
from volcenginesdkmcdn.models.delete_dns_schedule_static_weight_response import DeleteDnsScheduleStaticWeightResponse
from volcenginesdkmcdn.models.describe_alert_strategy_request import DescribeAlertStrategyRequest
from volcenginesdkmcdn.models.describe_alert_strategy_response import DescribeAlertStrategyResponse
from volcenginesdkmcdn.models.describe_cdn_access_log_request import DescribeCdnAccessLogRequest
from volcenginesdkmcdn.models.describe_cdn_access_log_response import DescribeCdnAccessLogResponse
from volcenginesdkmcdn.models.describe_cdn_data_offline_request import DescribeCdnDataOfflineRequest
from volcenginesdkmcdn.models.describe_cdn_data_offline_response import DescribeCdnDataOfflineResponse
from volcenginesdkmcdn.models.describe_cdn_origin_data_offline_request import DescribeCdnOriginDataOfflineRequest
from volcenginesdkmcdn.models.describe_cdn_origin_data_offline_response import DescribeCdnOriginDataOfflineResponse
from volcenginesdkmcdn.models.describe_cdn_region_and_isp_request import DescribeCdnRegionAndIspRequest
from volcenginesdkmcdn.models.describe_cdn_region_and_isp_response import DescribeCdnRegionAndIspResponse
from volcenginesdkmcdn.models.describe_content_quota_request import DescribeContentQuotaRequest
from volcenginesdkmcdn.models.describe_content_quota_response import DescribeContentQuotaResponse
from volcenginesdkmcdn.models.describe_content_task_by_task_id_request import DescribeContentTaskByTaskIdRequest
from volcenginesdkmcdn.models.describe_content_task_by_task_id_response import DescribeContentTaskByTaskIdResponse
from volcenginesdkmcdn.models.describe_dns_schedule_active_weights_request import DescribeDnsScheduleActiveWeightsRequest
from volcenginesdkmcdn.models.describe_dns_schedule_active_weights_response import DescribeDnsScheduleActiveWeightsResponse
from volcenginesdkmcdn.models.describe_dns_schedule_request import DescribeDnsScheduleRequest
from volcenginesdkmcdn.models.describe_dns_schedule_response import DescribeDnsScheduleResponse
from volcenginesdkmcdn.models.describe_dns_schedule_static_weights_request import DescribeDnsScheduleStaticWeightsRequest
from volcenginesdkmcdn.models.describe_dns_schedule_static_weights_response import DescribeDnsScheduleStaticWeightsResponse
from volcenginesdkmcdn.models.disable_dns_schedule_domain_request import DisableDnsScheduleDomainRequest
from volcenginesdkmcdn.models.disable_dns_schedule_domain_response import DisableDnsScheduleDomainResponse
from volcenginesdkmcdn.models.dns_schedule_for_list_dns_schedules_output import DnsScheduleForListDnsSchedulesOutput
from volcenginesdkmcdn.models.dns_schedule_info_for_describe_dns_schedule_output import DnsScheduleInfoForDescribeDnsScheduleOutput
from volcenginesdkmcdn.models.domain_for_describe_alert_strategy_output import DomainForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.domain_for_list_alert_strategies_output import DomainForListAlertStrategiesOutput
from volcenginesdkmcdn.models.domain_for_list_cdn_domains_output import DomainForListCdnDomainsOutput
from volcenginesdkmcdn.models.domain_settings_for_list_cloud_accounts_output import DomainSettingsForListCloudAccountsOutput
from volcenginesdkmcdn.models.domain_sync_status_state_for_list_cloud_accounts_output import DomainSyncStatusStateForListCloudAccountsOutput
from volcenginesdkmcdn.models.domestic_domain_for_describe_dns_schedule_output import DomesticDomainForDescribeDnsScheduleOutput
from volcenginesdkmcdn.models.enable_dns_schedule_domain_request import EnableDnsScheduleDomainRequest
from volcenginesdkmcdn.models.enable_dns_schedule_domain_response import EnableDnsScheduleDomainResponse
from volcenginesdkmcdn.models.error_for_describe_content_quota_output import ErrorForDescribeContentQuotaOutput
from volcenginesdkmcdn.models.error_for_describe_content_task_by_task_id_output import ErrorForDescribeContentTaskByTaskIdOutput
from volcenginesdkmcdn.models.extra_for_list_cloud_accounts_output import ExtraForListCloudAccountsOutput
from volcenginesdkmcdn.models.global_domain_for_describe_dns_schedule_output import GlobalDomainForDescribeDnsScheduleOutput
from volcenginesdkmcdn.models.isp_for_describe_cdn_region_and_isp_output import IspForDescribeCdnRegionAndIspOutput
from volcenginesdkmcdn.models.isp_for_list_views_output import IspForListViewsOutput
from volcenginesdkmcdn.models.list_alert_meta_metrics_request import ListAlertMetaMetricsRequest
from volcenginesdkmcdn.models.list_alert_meta_metrics_response import ListAlertMetaMetricsResponse
from volcenginesdkmcdn.models.list_alert_strategies_request import ListAlertStrategiesRequest
from volcenginesdkmcdn.models.list_alert_strategies_response import ListAlertStrategiesResponse
from volcenginesdkmcdn.models.list_cdn_domains_request import ListCdnDomainsRequest
from volcenginesdkmcdn.models.list_cdn_domains_response import ListCdnDomainsResponse
from volcenginesdkmcdn.models.list_cloud_accounts_request import ListCloudAccountsRequest
from volcenginesdkmcdn.models.list_cloud_accounts_response import ListCloudAccountsResponse
from volcenginesdkmcdn.models.list_content_tasks_request import ListContentTasksRequest
from volcenginesdkmcdn.models.list_content_tasks_response import ListContentTasksResponse
from volcenginesdkmcdn.models.list_dns_schedules_request import ListDnsSchedulesRequest
from volcenginesdkmcdn.models.list_dns_schedules_response import ListDnsSchedulesResponse
from volcenginesdkmcdn.models.list_vendor_content_task_request import ListVendorContentTaskRequest
from volcenginesdkmcdn.models.list_vendor_content_task_response import ListVendorContentTaskResponse
from volcenginesdkmcdn.models.list_views_request import ListViewsRequest
from volcenginesdkmcdn.models.list_views_response import ListViewsResponse
from volcenginesdkmcdn.models.log_for_describe_cdn_access_log_output import LogForDescribeCdnAccessLogOutput
from volcenginesdkmcdn.models.log_info_for_describe_cdn_access_log_output import LogInfoForDescribeCdnAccessLogOutput
from volcenginesdkmcdn.models.metric_for_describe_cdn_data_offline_output import MetricForDescribeCdnDataOfflineOutput
from volcenginesdkmcdn.models.metric_for_describe_cdn_origin_data_offline_output import MetricForDescribeCdnOriginDataOfflineOutput
from volcenginesdkmcdn.models.name_pair_for_describe_cdn_region_and_isp_output import NamePairForDescribeCdnRegionAndIspOutput
from volcenginesdkmcdn.models.network_for_list_cdn_domains_output import NetworkForListCdnDomainsOutput
from volcenginesdkmcdn.models.notify_config_for_describe_alert_strategy_output import NotifyConfigForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.notify_config_for_list_alert_strategies_output import NotifyConfigForListAlertStrategiesOutput
from volcenginesdkmcdn.models.offline_data_setting_for_list_cloud_accounts_output import OfflineDataSettingForListCloudAccountsOutput
from volcenginesdkmcdn.models.pagination_for_describe_cdn_access_log_input import PaginationForDescribeCdnAccessLogInput
from volcenginesdkmcdn.models.pagination_for_describe_cdn_access_log_output import PaginationForDescribeCdnAccessLogOutput
from volcenginesdkmcdn.models.pagination_for_list_alert_meta_metrics_output import PaginationForListAlertMetaMetricsOutput
from volcenginesdkmcdn.models.pagination_for_list_alert_strategies_input import PaginationForListAlertStrategiesInput
from volcenginesdkmcdn.models.pagination_for_list_alert_strategies_output import PaginationForListAlertStrategiesOutput
from volcenginesdkmcdn.models.pagination_for_list_cdn_domains_input import PaginationForListCdnDomainsInput
from volcenginesdkmcdn.models.pagination_for_list_cdn_domains_output import PaginationForListCdnDomainsOutput
from volcenginesdkmcdn.models.pagination_for_list_cloud_accounts_input import PaginationForListCloudAccountsInput
from volcenginesdkmcdn.models.pagination_for_list_cloud_accounts_output import PaginationForListCloudAccountsOutput
from volcenginesdkmcdn.models.pagination_for_list_content_tasks_input import PaginationForListContentTasksInput
from volcenginesdkmcdn.models.pagination_for_list_content_tasks_output import PaginationForListContentTasksOutput
from volcenginesdkmcdn.models.pagination_for_list_dns_schedules_input import PaginationForListDnsSchedulesInput
from volcenginesdkmcdn.models.pagination_for_list_dns_schedules_output import PaginationForListDnsSchedulesOutput
from volcenginesdkmcdn.models.pagination_for_list_vendor_content_task_input import PaginationForListVendorContentTaskInput
from volcenginesdkmcdn.models.pagination_for_list_vendor_content_task_output import PaginationForListVendorContentTaskOutput
from volcenginesdkmcdn.models.paging_option_for_list_alert_meta_metrics_input import PagingOptionForListAlertMetaMetricsInput
from volcenginesdkmcdn.models.permission_state_for_list_cloud_accounts_output import PermissionStateForListCloudAccountsOutput
from volcenginesdkmcdn.models.preload_for_list_cloud_accounts_output import PreloadForListCloudAccountsOutput
from volcenginesdkmcdn.models.probe_task_for_describe_alert_strategy_output import ProbeTaskForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.probe_task_for_list_alert_strategies_output import ProbeTaskForListAlertStrategiesOutput
from volcenginesdkmcdn.models.province_for_list_views_output import ProvinceForListViewsOutput
from volcenginesdkmcdn.models.quota_for_describe_content_quota_output import QuotaForDescribeContentQuotaOutput
from volcenginesdkmcdn.models.region_for_describe_cdn_region_and_isp_output import RegionForDescribeCdnRegionAndIspOutput
from volcenginesdkmcdn.models.resource_for_describe_cdn_data_offline_output import ResourceForDescribeCdnDataOfflineOutput
from volcenginesdkmcdn.models.resource_for_describe_cdn_origin_data_offline_output import ResourceForDescribeCdnOriginDataOfflineOutput
from volcenginesdkmcdn.models.stat_settings_for_list_cloud_accounts_output import StatSettingsForListCloudAccountsOutput
from volcenginesdkmcdn.models.stat_sync_status_state_for_list_cloud_accounts_output import StatSyncStatusStateForListCloudAccountsOutput
from volcenginesdkmcdn.models.static_weight_for_add_dns_schedule_static_weight_output import StaticWeightForAddDnsScheduleStaticWeightOutput
from volcenginesdkmcdn.models.static_weight_for_describe_dns_schedule_static_weights_output import StaticWeightForDescribeDnsScheduleStaticWeightsOutput
from volcenginesdkmcdn.models.sub_task_for_describe_content_task_by_task_id_output import SubTaskForDescribeContentTaskByTaskIdOutput
from volcenginesdkmcdn.models.sub_task_for_list_content_tasks_output import SubTaskForListContentTasksOutput
from volcenginesdkmcdn.models.submit_preload_task_request import SubmitPreloadTaskRequest
from volcenginesdkmcdn.models.submit_preload_task_response import SubmitPreloadTaskResponse
from volcenginesdkmcdn.models.submit_refresh_task_request import SubmitRefreshTaskRequest
from volcenginesdkmcdn.models.submit_refresh_task_response import SubmitRefreshTaskResponse
from volcenginesdkmcdn.models.subscribe_rule_for_describe_alert_strategy_output import SubscribeRuleForDescribeAlertStrategyOutput
from volcenginesdkmcdn.models.subscribe_rule_for_list_alert_strategies_output import SubscribeRuleForListAlertStrategiesOutput
from volcenginesdkmcdn.models.sync_detail_for_list_cdn_domains_output import SyncDetailForListCdnDomainsOutput
from volcenginesdkmcdn.models.sync_status_state_for_list_cloud_accounts_output import SyncStatusStateForListCloudAccountsOutput
from volcenginesdkmcdn.models.tag_filter_for_list_cdn_domains_input import TagFilterForListCdnDomainsInput
from volcenginesdkmcdn.models.tag_for_list_cdn_domains_output import TagForListCdnDomainsOutput
from volcenginesdkmcdn.models.task_for_list_content_tasks_output import TaskForListContentTasksOutput
from volcenginesdkmcdn.models.task_for_list_vendor_content_task_output import TaskForListVendorContentTaskOutput
from volcenginesdkmcdn.models.template_info_for_describe_dns_schedule_static_weights_output import TemplateInfoForDescribeDnsScheduleStaticWeightsOutput
from volcenginesdkmcdn.models.u_cloud_for_list_cloud_accounts_output import UCloudForListCloudAccountsOutput
from volcenginesdkmcdn.models.update_dns_schedule_static_weight_request import UpdateDnsScheduleStaticWeightRequest
from volcenginesdkmcdn.models.update_dns_schedule_static_weight_response import UpdateDnsScheduleStaticWeightResponse
from volcenginesdkmcdn.models.value_for_describe_cdn_data_offline_output import ValueForDescribeCdnDataOfflineOutput
from volcenginesdkmcdn.models.value_for_describe_cdn_origin_data_offline_output import ValueForDescribeCdnOriginDataOfflineOutput
from volcenginesdkmcdn.models.vendors_meta_data_for_describe_content_quota_output import VendorsMetaDataForDescribeContentQuotaOutput
from volcenginesdkmcdn.models.vendors_meta_data_for_describe_content_task_by_task_id_output import VendorsMetaDataForDescribeContentTaskByTaskIdOutput
from volcenginesdkmcdn.models.volc_ids_sync_detail_for_list_cdn_domains_output import VolcIdsSyncDetailForListCdnDomainsOutput
from volcenginesdkmcdn.models.weight_failover_info_for_describe_dns_schedule_active_weights_output import WeightFailoverInfoForDescribeDnsScheduleActiveWeightsOutput
from volcenginesdkmcdn.models.weight_failover_info_for_describe_dns_schedule_output import WeightFailoverInfoForDescribeDnsScheduleOutput
from volcenginesdkmcdn.models.weight_info_for_describe_dns_schedule_output import WeightInfoForDescribeDnsScheduleOutput
from volcenginesdkmcdn.models.weight_info_item_for_describe_dns_schedule_active_weights_output import WeightInfoItemForDescribeDnsScheduleActiveWeightsOutput
from volcenginesdkmcdn.models.weight_info_item_for_describe_dns_schedule_output import WeightInfoItemForDescribeDnsScheduleOutput
from volcenginesdkmcdn.models.weight_item_for_add_dns_schedule_static_weight_input import WeightItemForAddDnsScheduleStaticWeightInput
from volcenginesdkmcdn.models.weight_item_for_add_dns_schedule_static_weight_output import WeightItemForAddDnsScheduleStaticWeightOutput
from volcenginesdkmcdn.models.weight_item_for_describe_dns_schedule_static_weights_output import WeightItemForDescribeDnsScheduleStaticWeightsOutput
from volcenginesdkmcdn.models.weight_item_for_update_dns_schedule_static_weight_input import WeightItemForUpdateDnsScheduleStaticWeightInput
