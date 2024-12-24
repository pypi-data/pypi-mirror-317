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
from . import outputs
from ._inputs import *

__all__ = ['FederatedSettingsOrgConfigArgs', 'FederatedSettingsOrgConfig']

@pulumi.input_type
class FederatedSettingsOrgConfigArgs:
    def __init__(__self__, *,
                 domain_restriction_enabled: pulumi.Input[bool],
                 federation_settings_id: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 data_access_identity_provider_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domain_allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 identity_provider_id: Optional[pulumi.Input[str]] = None,
                 post_auth_role_grants: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a FederatedSettingsOrgConfig resource.
        :param pulumi.Input[bool] domain_restriction_enabled: Flag that indicates whether domain restriction is enabled for the connected organization.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] data_access_identity_provider_ids: The collection of unique ids representing the identity providers that can be used for data access in this organization.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domain_allow_lists: List that contains the approved domains from which organization users can log in.
        :param pulumi.Input[str] identity_provider_id: Legacy 20-hexadecimal digit string that identifies the SAML access identity provider that this connected org config is associated with. Removing the attribute or providing the value `""` will detach/remove the SAML identity provider. This id can be found in two ways:
               1. Within the Federation Management UI in Atlas in the Identity Providers tab by clicking the info icon in the IdP ID row of a configured SAML identity provider
               2. `okta_idp_id` on the `FederatedSettingsIdentityProvider` resource
        :param pulumi.Input[Sequence[pulumi.Input[str]]] post_auth_role_grants: List that contains the default [roles](https://www.mongodb.com/docs/atlas/reference/user-roles/#std-label-organization-roles) granted to users who authenticate through the IdP in a connected organization.
        """
        pulumi.set(__self__, "domain_restriction_enabled", domain_restriction_enabled)
        pulumi.set(__self__, "federation_settings_id", federation_settings_id)
        pulumi.set(__self__, "org_id", org_id)
        if data_access_identity_provider_ids is not None:
            pulumi.set(__self__, "data_access_identity_provider_ids", data_access_identity_provider_ids)
        if domain_allow_lists is not None:
            pulumi.set(__self__, "domain_allow_lists", domain_allow_lists)
        if identity_provider_id is not None:
            pulumi.set(__self__, "identity_provider_id", identity_provider_id)
        if post_auth_role_grants is not None:
            pulumi.set(__self__, "post_auth_role_grants", post_auth_role_grants)

    @property
    @pulumi.getter(name="domainRestrictionEnabled")
    def domain_restriction_enabled(self) -> pulumi.Input[bool]:
        """
        Flag that indicates whether domain restriction is enabled for the connected organization.
        """
        return pulumi.get(self, "domain_restriction_enabled")

    @domain_restriction_enabled.setter
    def domain_restriction_enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "domain_restriction_enabled", value)

    @property
    @pulumi.getter(name="federationSettingsId")
    def federation_settings_id(self) -> pulumi.Input[str]:
        """
        Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        """
        return pulumi.get(self, "federation_settings_id")

    @federation_settings_id.setter
    def federation_settings_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "federation_settings_id", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        """
        Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="dataAccessIdentityProviderIds")
    def data_access_identity_provider_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The collection of unique ids representing the identity providers that can be used for data access in this organization.
        """
        return pulumi.get(self, "data_access_identity_provider_ids")

    @data_access_identity_provider_ids.setter
    def data_access_identity_provider_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "data_access_identity_provider_ids", value)

    @property
    @pulumi.getter(name="domainAllowLists")
    def domain_allow_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List that contains the approved domains from which organization users can log in.
        """
        return pulumi.get(self, "domain_allow_lists")

    @domain_allow_lists.setter
    def domain_allow_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "domain_allow_lists", value)

    @property
    @pulumi.getter(name="identityProviderId")
    def identity_provider_id(self) -> Optional[pulumi.Input[str]]:
        """
        Legacy 20-hexadecimal digit string that identifies the SAML access identity provider that this connected org config is associated with. Removing the attribute or providing the value `""` will detach/remove the SAML identity provider. This id can be found in two ways:
        1. Within the Federation Management UI in Atlas in the Identity Providers tab by clicking the info icon in the IdP ID row of a configured SAML identity provider
        2. `okta_idp_id` on the `FederatedSettingsIdentityProvider` resource
        """
        return pulumi.get(self, "identity_provider_id")

    @identity_provider_id.setter
    def identity_provider_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_provider_id", value)

    @property
    @pulumi.getter(name="postAuthRoleGrants")
    def post_auth_role_grants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List that contains the default [roles](https://www.mongodb.com/docs/atlas/reference/user-roles/#std-label-organization-roles) granted to users who authenticate through the IdP in a connected organization.
        """
        return pulumi.get(self, "post_auth_role_grants")

    @post_auth_role_grants.setter
    def post_auth_role_grants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "post_auth_role_grants", value)


@pulumi.input_type
class _FederatedSettingsOrgConfigState:
    def __init__(__self__, *,
                 data_access_identity_provider_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domain_allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domain_restriction_enabled: Optional[pulumi.Input[bool]] = None,
                 federation_settings_id: Optional[pulumi.Input[str]] = None,
                 identity_provider_id: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 post_auth_role_grants: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 user_conflicts: Optional[pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgConfigUserConflictArgs']]]] = None):
        """
        Input properties used for looking up and filtering FederatedSettingsOrgConfig resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] data_access_identity_provider_ids: The collection of unique ids representing the identity providers that can be used for data access in this organization.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domain_allow_lists: List that contains the approved domains from which organization users can log in.
        :param pulumi.Input[bool] domain_restriction_enabled: Flag that indicates whether domain restriction is enabled for the connected organization.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] identity_provider_id: Legacy 20-hexadecimal digit string that identifies the SAML access identity provider that this connected org config is associated with. Removing the attribute or providing the value `""` will detach/remove the SAML identity provider. This id can be found in two ways:
               1. Within the Federation Management UI in Atlas in the Identity Providers tab by clicking the info icon in the IdP ID row of a configured SAML identity provider
               2. `okta_idp_id` on the `FederatedSettingsIdentityProvider` resource
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] post_auth_role_grants: List that contains the default [roles](https://www.mongodb.com/docs/atlas/reference/user-roles/#std-label-organization-roles) granted to users who authenticate through the IdP in a connected organization.
        :param pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgConfigUserConflictArgs']]] user_conflicts: List that contains the users who have an email address that doesn't match any domain on the allowed list. See below
        """
        if data_access_identity_provider_ids is not None:
            pulumi.set(__self__, "data_access_identity_provider_ids", data_access_identity_provider_ids)
        if domain_allow_lists is not None:
            pulumi.set(__self__, "domain_allow_lists", domain_allow_lists)
        if domain_restriction_enabled is not None:
            pulumi.set(__self__, "domain_restriction_enabled", domain_restriction_enabled)
        if federation_settings_id is not None:
            pulumi.set(__self__, "federation_settings_id", federation_settings_id)
        if identity_provider_id is not None:
            pulumi.set(__self__, "identity_provider_id", identity_provider_id)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if post_auth_role_grants is not None:
            pulumi.set(__self__, "post_auth_role_grants", post_auth_role_grants)
        if user_conflicts is not None:
            pulumi.set(__self__, "user_conflicts", user_conflicts)

    @property
    @pulumi.getter(name="dataAccessIdentityProviderIds")
    def data_access_identity_provider_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The collection of unique ids representing the identity providers that can be used for data access in this organization.
        """
        return pulumi.get(self, "data_access_identity_provider_ids")

    @data_access_identity_provider_ids.setter
    def data_access_identity_provider_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "data_access_identity_provider_ids", value)

    @property
    @pulumi.getter(name="domainAllowLists")
    def domain_allow_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List that contains the approved domains from which organization users can log in.
        """
        return pulumi.get(self, "domain_allow_lists")

    @domain_allow_lists.setter
    def domain_allow_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "domain_allow_lists", value)

    @property
    @pulumi.getter(name="domainRestrictionEnabled")
    def domain_restriction_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that indicates whether domain restriction is enabled for the connected organization.
        """
        return pulumi.get(self, "domain_restriction_enabled")

    @domain_restriction_enabled.setter
    def domain_restriction_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "domain_restriction_enabled", value)

    @property
    @pulumi.getter(name="federationSettingsId")
    def federation_settings_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        """
        return pulumi.get(self, "federation_settings_id")

    @federation_settings_id.setter
    def federation_settings_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "federation_settings_id", value)

    @property
    @pulumi.getter(name="identityProviderId")
    def identity_provider_id(self) -> Optional[pulumi.Input[str]]:
        """
        Legacy 20-hexadecimal digit string that identifies the SAML access identity provider that this connected org config is associated with. Removing the attribute or providing the value `""` will detach/remove the SAML identity provider. This id can be found in two ways:
        1. Within the Federation Management UI in Atlas in the Identity Providers tab by clicking the info icon in the IdP ID row of a configured SAML identity provider
        2. `okta_idp_id` on the `FederatedSettingsIdentityProvider` resource
        """
        return pulumi.get(self, "identity_provider_id")

    @identity_provider_id.setter
    def identity_provider_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_provider_id", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="postAuthRoleGrants")
    def post_auth_role_grants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List that contains the default [roles](https://www.mongodb.com/docs/atlas/reference/user-roles/#std-label-organization-roles) granted to users who authenticate through the IdP in a connected organization.
        """
        return pulumi.get(self, "post_auth_role_grants")

    @post_auth_role_grants.setter
    def post_auth_role_grants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "post_auth_role_grants", value)

    @property
    @pulumi.getter(name="userConflicts")
    def user_conflicts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgConfigUserConflictArgs']]]]:
        """
        List that contains the users who have an email address that doesn't match any domain on the allowed list. See below
        """
        return pulumi.get(self, "user_conflicts")

    @user_conflicts.setter
    def user_conflicts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgConfigUserConflictArgs']]]]):
        pulumi.set(self, "user_conflicts", value)


class FederatedSettingsOrgConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_access_identity_provider_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domain_allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domain_restriction_enabled: Optional[pulumi.Input[bool]] = None,
                 federation_settings_id: Optional[pulumi.Input[str]] = None,
                 identity_provider_id: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 post_auth_role_grants: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ## # Resource: FederatedSettingsOrgConfig

        `FederatedSettingsOrgConfig` provides an Federated Settings Identity Providers datasource. Atlas Cloud Federated Settings Identity Providers provides federated settings outputs for the configured Identity Providers.

        ## Example Usage

        > **IMPORTANT** You **MUST** import this resource before you can manage it with this provider.

        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        org_connection = mongodbatlas.FederatedSettingsOrgConfig("org_connection",
            federation_settings_id="627a9687f7f7f7f774de306f14",
            org_id="627a9683ea7ff7f74de306f14",
            data_access_identity_provider_ids=["64d613677e1ad50839cce4db"],
            domain_restriction_enabled=False,
            domain_allow_lists=["mydomain.com"],
            post_auth_role_grants=["ORG_MEMBER"],
            identity_provider_id="0oaqyt9fc2ySTWnA0357")
        org_configs_ds = mongodbatlas.get_federated_settings_org_configs(federation_settings_id=org_connection_mongodbatlas_federated_settings_org_config["id"])
        ```

        ## Import

        FederatedSettingsOrgConfig must be imported using federation_settings_id-org_id, e.g.

        ```sh
        $ pulumi import mongodbatlas:index/federatedSettingsOrgConfig:FederatedSettingsOrgConfig org_connection 627a9687f7f7f7f774de306f14-627a9683ea7ff7f74de306f14
        ```
        For more information see: [MongoDB Atlas API Reference.](https://www.mongodb.com/docs/atlas/reference/api/federation-configuration/)

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] data_access_identity_provider_ids: The collection of unique ids representing the identity providers that can be used for data access in this organization.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domain_allow_lists: List that contains the approved domains from which organization users can log in.
        :param pulumi.Input[bool] domain_restriction_enabled: Flag that indicates whether domain restriction is enabled for the connected organization.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] identity_provider_id: Legacy 20-hexadecimal digit string that identifies the SAML access identity provider that this connected org config is associated with. Removing the attribute or providing the value `""` will detach/remove the SAML identity provider. This id can be found in two ways:
               1. Within the Federation Management UI in Atlas in the Identity Providers tab by clicking the info icon in the IdP ID row of a configured SAML identity provider
               2. `okta_idp_id` on the `FederatedSettingsIdentityProvider` resource
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] post_auth_role_grants: List that contains the default [roles](https://www.mongodb.com/docs/atlas/reference/user-roles/#std-label-organization-roles) granted to users who authenticate through the IdP in a connected organization.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FederatedSettingsOrgConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## # Resource: FederatedSettingsOrgConfig

        `FederatedSettingsOrgConfig` provides an Federated Settings Identity Providers datasource. Atlas Cloud Federated Settings Identity Providers provides federated settings outputs for the configured Identity Providers.

        ## Example Usage

        > **IMPORTANT** You **MUST** import this resource before you can manage it with this provider.

        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        org_connection = mongodbatlas.FederatedSettingsOrgConfig("org_connection",
            federation_settings_id="627a9687f7f7f7f774de306f14",
            org_id="627a9683ea7ff7f74de306f14",
            data_access_identity_provider_ids=["64d613677e1ad50839cce4db"],
            domain_restriction_enabled=False,
            domain_allow_lists=["mydomain.com"],
            post_auth_role_grants=["ORG_MEMBER"],
            identity_provider_id="0oaqyt9fc2ySTWnA0357")
        org_configs_ds = mongodbatlas.get_federated_settings_org_configs(federation_settings_id=org_connection_mongodbatlas_federated_settings_org_config["id"])
        ```

        ## Import

        FederatedSettingsOrgConfig must be imported using federation_settings_id-org_id, e.g.

        ```sh
        $ pulumi import mongodbatlas:index/federatedSettingsOrgConfig:FederatedSettingsOrgConfig org_connection 627a9687f7f7f7f774de306f14-627a9683ea7ff7f74de306f14
        ```
        For more information see: [MongoDB Atlas API Reference.](https://www.mongodb.com/docs/atlas/reference/api/federation-configuration/)

        :param str resource_name: The name of the resource.
        :param FederatedSettingsOrgConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FederatedSettingsOrgConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_access_identity_provider_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domain_allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domain_restriction_enabled: Optional[pulumi.Input[bool]] = None,
                 federation_settings_id: Optional[pulumi.Input[str]] = None,
                 identity_provider_id: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 post_auth_role_grants: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FederatedSettingsOrgConfigArgs.__new__(FederatedSettingsOrgConfigArgs)

            __props__.__dict__["data_access_identity_provider_ids"] = data_access_identity_provider_ids
            __props__.__dict__["domain_allow_lists"] = domain_allow_lists
            if domain_restriction_enabled is None and not opts.urn:
                raise TypeError("Missing required property 'domain_restriction_enabled'")
            __props__.__dict__["domain_restriction_enabled"] = domain_restriction_enabled
            if federation_settings_id is None and not opts.urn:
                raise TypeError("Missing required property 'federation_settings_id'")
            __props__.__dict__["federation_settings_id"] = federation_settings_id
            __props__.__dict__["identity_provider_id"] = identity_provider_id
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["post_auth_role_grants"] = post_auth_role_grants
            __props__.__dict__["user_conflicts"] = None
        super(FederatedSettingsOrgConfig, __self__).__init__(
            'mongodbatlas:index/federatedSettingsOrgConfig:FederatedSettingsOrgConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            data_access_identity_provider_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            domain_allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            domain_restriction_enabled: Optional[pulumi.Input[bool]] = None,
            federation_settings_id: Optional[pulumi.Input[str]] = None,
            identity_provider_id: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            post_auth_role_grants: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            user_conflicts: Optional[pulumi.Input[Sequence[pulumi.Input[Union['FederatedSettingsOrgConfigUserConflictArgs', 'FederatedSettingsOrgConfigUserConflictArgsDict']]]]] = None) -> 'FederatedSettingsOrgConfig':
        """
        Get an existing FederatedSettingsOrgConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] data_access_identity_provider_ids: The collection of unique ids representing the identity providers that can be used for data access in this organization.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domain_allow_lists: List that contains the approved domains from which organization users can log in.
        :param pulumi.Input[bool] domain_restriction_enabled: Flag that indicates whether domain restriction is enabled for the connected organization.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] identity_provider_id: Legacy 20-hexadecimal digit string that identifies the SAML access identity provider that this connected org config is associated with. Removing the attribute or providing the value `""` will detach/remove the SAML identity provider. This id can be found in two ways:
               1. Within the Federation Management UI in Atlas in the Identity Providers tab by clicking the info icon in the IdP ID row of a configured SAML identity provider
               2. `okta_idp_id` on the `FederatedSettingsIdentityProvider` resource
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] post_auth_role_grants: List that contains the default [roles](https://www.mongodb.com/docs/atlas/reference/user-roles/#std-label-organization-roles) granted to users who authenticate through the IdP in a connected organization.
        :param pulumi.Input[Sequence[pulumi.Input[Union['FederatedSettingsOrgConfigUserConflictArgs', 'FederatedSettingsOrgConfigUserConflictArgsDict']]]] user_conflicts: List that contains the users who have an email address that doesn't match any domain on the allowed list. See below
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FederatedSettingsOrgConfigState.__new__(_FederatedSettingsOrgConfigState)

        __props__.__dict__["data_access_identity_provider_ids"] = data_access_identity_provider_ids
        __props__.__dict__["domain_allow_lists"] = domain_allow_lists
        __props__.__dict__["domain_restriction_enabled"] = domain_restriction_enabled
        __props__.__dict__["federation_settings_id"] = federation_settings_id
        __props__.__dict__["identity_provider_id"] = identity_provider_id
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["post_auth_role_grants"] = post_auth_role_grants
        __props__.__dict__["user_conflicts"] = user_conflicts
        return FederatedSettingsOrgConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataAccessIdentityProviderIds")
    def data_access_identity_provider_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The collection of unique ids representing the identity providers that can be used for data access in this organization.
        """
        return pulumi.get(self, "data_access_identity_provider_ids")

    @property
    @pulumi.getter(name="domainAllowLists")
    def domain_allow_lists(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List that contains the approved domains from which organization users can log in.
        """
        return pulumi.get(self, "domain_allow_lists")

    @property
    @pulumi.getter(name="domainRestrictionEnabled")
    def domain_restriction_enabled(self) -> pulumi.Output[bool]:
        """
        Flag that indicates whether domain restriction is enabled for the connected organization.
        """
        return pulumi.get(self, "domain_restriction_enabled")

    @property
    @pulumi.getter(name="federationSettingsId")
    def federation_settings_id(self) -> pulumi.Output[str]:
        """
        Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        """
        return pulumi.get(self, "federation_settings_id")

    @property
    @pulumi.getter(name="identityProviderId")
    def identity_provider_id(self) -> pulumi.Output[Optional[str]]:
        """
        Legacy 20-hexadecimal digit string that identifies the SAML access identity provider that this connected org config is associated with. Removing the attribute or providing the value `""` will detach/remove the SAML identity provider. This id can be found in two ways:
        1. Within the Federation Management UI in Atlas in the Identity Providers tab by clicking the info icon in the IdP ID row of a configured SAML identity provider
        2. `okta_idp_id` on the `FederatedSettingsIdentityProvider` resource
        """
        return pulumi.get(self, "identity_provider_id")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        """
        Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="postAuthRoleGrants")
    def post_auth_role_grants(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List that contains the default [roles](https://www.mongodb.com/docs/atlas/reference/user-roles/#std-label-organization-roles) granted to users who authenticate through the IdP in a connected organization.
        """
        return pulumi.get(self, "post_auth_role_grants")

    @property
    @pulumi.getter(name="userConflicts")
    def user_conflicts(self) -> pulumi.Output[Sequence['outputs.FederatedSettingsOrgConfigUserConflict']]:
        """
        List that contains the users who have an email address that doesn't match any domain on the allowed list. See below
        """
        return pulumi.get(self, "user_conflicts")

