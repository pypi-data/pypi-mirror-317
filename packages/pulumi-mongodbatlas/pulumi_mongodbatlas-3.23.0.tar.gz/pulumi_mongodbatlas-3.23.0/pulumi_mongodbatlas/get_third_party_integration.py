# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities

__all__ = [
    'GetThirdPartyIntegrationResult',
    'AwaitableGetThirdPartyIntegrationResult',
    'get_third_party_integration',
    'get_third_party_integration_output',
]

@pulumi.output_type
class GetThirdPartyIntegrationResult:
    """
    A collection of values returned by getThirdPartyIntegration.
    """
    def __init__(__self__, account_id=None, api_key=None, channel_name=None, enabled=None, id=None, microsoft_teams_webhook_url=None, project_id=None, region=None, routing_key=None, secret=None, service_discovery=None, service_key=None, team_name=None, type=None, url=None, user_name=None):
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)
        if api_key and not isinstance(api_key, str):
            raise TypeError("Expected argument 'api_key' to be a str")
        pulumi.set(__self__, "api_key", api_key)
        if channel_name and not isinstance(channel_name, str):
            raise TypeError("Expected argument 'channel_name' to be a str")
        pulumi.set(__self__, "channel_name", channel_name)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if microsoft_teams_webhook_url and not isinstance(microsoft_teams_webhook_url, str):
            raise TypeError("Expected argument 'microsoft_teams_webhook_url' to be a str")
        pulumi.set(__self__, "microsoft_teams_webhook_url", microsoft_teams_webhook_url)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if routing_key and not isinstance(routing_key, str):
            raise TypeError("Expected argument 'routing_key' to be a str")
        pulumi.set(__self__, "routing_key", routing_key)
        if secret and not isinstance(secret, str):
            raise TypeError("Expected argument 'secret' to be a str")
        pulumi.set(__self__, "secret", secret)
        if service_discovery and not isinstance(service_discovery, str):
            raise TypeError("Expected argument 'service_discovery' to be a str")
        pulumi.set(__self__, "service_discovery", service_discovery)
        if service_key and not isinstance(service_key, str):
            raise TypeError("Expected argument 'service_key' to be a str")
        pulumi.set(__self__, "service_key", service_key)
        if team_name and not isinstance(team_name, str):
            raise TypeError("Expected argument 'team_name' to be a str")
        pulumi.set(__self__, "team_name", team_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> str:
        """
        Your API Key.
        """
        return pulumi.get(self, "api_key")

    @property
    @pulumi.getter(name="channelName")
    def channel_name(self) -> str:
        return pulumi.get(self, "channel_name")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Whether your cluster has Prometheus enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Unique identifier of the integration.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="microsoftTeamsWebhookUrl")
    def microsoft_teams_webhook_url(self) -> Optional[str]:
        """
        Your Microsoft Teams incoming webhook URL.
        * `PROMETHEUS`
        """
        return pulumi.get(self, "microsoft_teams_webhook_url")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        Two-letter code that indicates which API URL to use. See the `region` response field of [MongoDB API Third-Party Service Integration documentation](https://www.mongodb.com/docs/atlas/reference/api-resources-spec/v2/#tag/Third-Party-Integrations/operation/getThirdPartyIntegration) for more details. Opsgenie will use US by default.
        * `VICTOR_OPS`
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="routingKey")
    def routing_key(self) -> str:
        """
        An optional field for your Routing Key.
        * `WEBHOOK`
        """
        return pulumi.get(self, "routing_key")

    @property
    @pulumi.getter
    def secret(self) -> str:
        """
        An optional field for your webhook secret.
        * `MICROSOFT_TEAMS`
        """
        return pulumi.get(self, "secret")

    @property
    @pulumi.getter(name="serviceDiscovery")
    def service_discovery(self) -> Optional[str]:
        """
        Indicates which service discovery method is used, either file or http.
        """
        return pulumi.get(self, "service_discovery")

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> str:
        """
        Your Service Key.
        * `DATADOG`
        """
        return pulumi.get(self, "service_key")

    @property
    @pulumi.getter(name="teamName")
    def team_name(self) -> str:
        return pulumi.get(self, "team_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        Your webhook URL.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[str]:
        """
        Your Prometheus username.
        """
        return pulumi.get(self, "user_name")


class AwaitableGetThirdPartyIntegrationResult(GetThirdPartyIntegrationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetThirdPartyIntegrationResult(
            account_id=self.account_id,
            api_key=self.api_key,
            channel_name=self.channel_name,
            enabled=self.enabled,
            id=self.id,
            microsoft_teams_webhook_url=self.microsoft_teams_webhook_url,
            project_id=self.project_id,
            region=self.region,
            routing_key=self.routing_key,
            secret=self.secret,
            service_discovery=self.service_discovery,
            service_key=self.service_key,
            team_name=self.team_name,
            type=self.type,
            url=self.url,
            user_name=self.user_name)


def get_third_party_integration(enabled: Optional[bool] = None,
                                microsoft_teams_webhook_url: Optional[str] = None,
                                project_id: Optional[str] = None,
                                service_discovery: Optional[str] = None,
                                type: Optional[str] = None,
                                user_name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetThirdPartyIntegrationResult:
    """
    ## # Data Source: ThirdPartyIntegration

    `ThirdPartyIntegration` describes a Third-Party Integration Settings for the given type.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_datadog = mongodbatlas.ThirdPartyIntegration("test_datadog",
        project_id="<PROJECT-ID>",
        type="DATADOG",
        api_key="<API-KEY>",
        region="<REGION>")
    test = mongodbatlas.get_third_party_integration_output(project_id=test_datadog.project_id,
        type="DATADOG")
    ```


    :param bool enabled: Whether your cluster has Prometheus enabled.
    :param str microsoft_teams_webhook_url: Your Microsoft Teams incoming webhook URL.
           * `PROMETHEUS`
    :param str project_id: The unique ID for the project to get all Third-Party service integrations
    :param str service_discovery: Indicates which service discovery method is used, either file or http.
    :param str type: Third-Party service integration type
           * PAGER_DUTY
           * DATADOG
           * OPS_GENIE
           * VICTOR_OPS
           * WEBHOOK
           * MICROSOFT_TEAMS
           * PROMETHEUS
    :param str user_name: Your Prometheus username.
    """
    __args__ = dict()
    __args__['enabled'] = enabled
    __args__['microsoftTeamsWebhookUrl'] = microsoft_teams_webhook_url
    __args__['projectId'] = project_id
    __args__['serviceDiscovery'] = service_discovery
    __args__['type'] = type
    __args__['userName'] = user_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getThirdPartyIntegration:getThirdPartyIntegration', __args__, opts=opts, typ=GetThirdPartyIntegrationResult).value

    return AwaitableGetThirdPartyIntegrationResult(
        account_id=pulumi.get(__ret__, 'account_id'),
        api_key=pulumi.get(__ret__, 'api_key'),
        channel_name=pulumi.get(__ret__, 'channel_name'),
        enabled=pulumi.get(__ret__, 'enabled'),
        id=pulumi.get(__ret__, 'id'),
        microsoft_teams_webhook_url=pulumi.get(__ret__, 'microsoft_teams_webhook_url'),
        project_id=pulumi.get(__ret__, 'project_id'),
        region=pulumi.get(__ret__, 'region'),
        routing_key=pulumi.get(__ret__, 'routing_key'),
        secret=pulumi.get(__ret__, 'secret'),
        service_discovery=pulumi.get(__ret__, 'service_discovery'),
        service_key=pulumi.get(__ret__, 'service_key'),
        team_name=pulumi.get(__ret__, 'team_name'),
        type=pulumi.get(__ret__, 'type'),
        url=pulumi.get(__ret__, 'url'),
        user_name=pulumi.get(__ret__, 'user_name'))
def get_third_party_integration_output(enabled: Optional[pulumi.Input[Optional[bool]]] = None,
                                       microsoft_teams_webhook_url: Optional[pulumi.Input[Optional[str]]] = None,
                                       project_id: Optional[pulumi.Input[str]] = None,
                                       service_discovery: Optional[pulumi.Input[Optional[str]]] = None,
                                       type: Optional[pulumi.Input[str]] = None,
                                       user_name: Optional[pulumi.Input[Optional[str]]] = None,
                                       opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetThirdPartyIntegrationResult]:
    """
    ## # Data Source: ThirdPartyIntegration

    `ThirdPartyIntegration` describes a Third-Party Integration Settings for the given type.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_datadog = mongodbatlas.ThirdPartyIntegration("test_datadog",
        project_id="<PROJECT-ID>",
        type="DATADOG",
        api_key="<API-KEY>",
        region="<REGION>")
    test = mongodbatlas.get_third_party_integration_output(project_id=test_datadog.project_id,
        type="DATADOG")
    ```


    :param bool enabled: Whether your cluster has Prometheus enabled.
    :param str microsoft_teams_webhook_url: Your Microsoft Teams incoming webhook URL.
           * `PROMETHEUS`
    :param str project_id: The unique ID for the project to get all Third-Party service integrations
    :param str service_discovery: Indicates which service discovery method is used, either file or http.
    :param str type: Third-Party service integration type
           * PAGER_DUTY
           * DATADOG
           * OPS_GENIE
           * VICTOR_OPS
           * WEBHOOK
           * MICROSOFT_TEAMS
           * PROMETHEUS
    :param str user_name: Your Prometheus username.
    """
    __args__ = dict()
    __args__['enabled'] = enabled
    __args__['microsoftTeamsWebhookUrl'] = microsoft_teams_webhook_url
    __args__['projectId'] = project_id
    __args__['serviceDiscovery'] = service_discovery
    __args__['type'] = type
    __args__['userName'] = user_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('mongodbatlas:index/getThirdPartyIntegration:getThirdPartyIntegration', __args__, opts=opts, typ=GetThirdPartyIntegrationResult)
    return __ret__.apply(lambda __response__: GetThirdPartyIntegrationResult(
        account_id=pulumi.get(__response__, 'account_id'),
        api_key=pulumi.get(__response__, 'api_key'),
        channel_name=pulumi.get(__response__, 'channel_name'),
        enabled=pulumi.get(__response__, 'enabled'),
        id=pulumi.get(__response__, 'id'),
        microsoft_teams_webhook_url=pulumi.get(__response__, 'microsoft_teams_webhook_url'),
        project_id=pulumi.get(__response__, 'project_id'),
        region=pulumi.get(__response__, 'region'),
        routing_key=pulumi.get(__response__, 'routing_key'),
        secret=pulumi.get(__response__, 'secret'),
        service_discovery=pulumi.get(__response__, 'service_discovery'),
        service_key=pulumi.get(__response__, 'service_key'),
        team_name=pulumi.get(__response__, 'team_name'),
        type=pulumi.get(__response__, 'type'),
        url=pulumi.get(__response__, 'url'),
        user_name=pulumi.get(__response__, 'user_name')))
