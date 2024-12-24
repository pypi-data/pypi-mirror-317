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

__all__ = ['ProjectIpAccessListArgs', 'ProjectIpAccessList']

@pulumi.input_type
class ProjectIpAccessListArgs:
    def __init__(__self__, *,
                 project_id: pulumi.Input[str],
                 aws_security_group: Optional[pulumi.Input[str]] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input['ProjectIpAccessListTimeoutsArgs']] = None):
        """
        The set of arguments for constructing a ProjectIpAccessList resource.
        :param pulumi.Input[str] project_id: Unique identifier for the project to which you want to add one or more access list entries.
        :param pulumi.Input[str] aws_security_group: Unique identifier of the AWS security group to add to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] cidr_block: Range of IP addresses in CIDR notation to be added to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] comment: Comment to add to the access list entry.
               
               > **NOTE:** One of the following attributes must set:  `aws_security_group`, `cidr_block`  or `ip_address`.
        :param pulumi.Input[str] ip_address: Single IP address to be added to the access list. Mutually exclusive with `awsSecurityGroup` and `cidrBlock`.
        """
        pulumi.set(__self__, "project_id", project_id)
        if aws_security_group is not None:
            pulumi.set(__self__, "aws_security_group", aws_security_group)
        if cidr_block is not None:
            pulumi.set(__self__, "cidr_block", cidr_block)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[str]:
        """
        Unique identifier for the project to which you want to add one or more access list entries.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="awsSecurityGroup")
    def aws_security_group(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the AWS security group to add to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        """
        return pulumi.get(self, "aws_security_group")

    @aws_security_group.setter
    def aws_security_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_security_group", value)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        Range of IP addresses in CIDR notation to be added to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Comment to add to the access list entry.

        > **NOTE:** One of the following attributes must set:  `aws_security_group`, `cidr_block`  or `ip_address`.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Single IP address to be added to the access list. Mutually exclusive with `awsSecurityGroup` and `cidrBlock`.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['ProjectIpAccessListTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['ProjectIpAccessListTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


@pulumi.input_type
class _ProjectIpAccessListState:
    def __init__(__self__, *,
                 aws_security_group: Optional[pulumi.Input[str]] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input['ProjectIpAccessListTimeoutsArgs']] = None):
        """
        Input properties used for looking up and filtering ProjectIpAccessList resources.
        :param pulumi.Input[str] aws_security_group: Unique identifier of the AWS security group to add to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] cidr_block: Range of IP addresses in CIDR notation to be added to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] comment: Comment to add to the access list entry.
               
               > **NOTE:** One of the following attributes must set:  `aws_security_group`, `cidr_block`  or `ip_address`.
        :param pulumi.Input[str] ip_address: Single IP address to be added to the access list. Mutually exclusive with `awsSecurityGroup` and `cidrBlock`.
        :param pulumi.Input[str] project_id: Unique identifier for the project to which you want to add one or more access list entries.
        """
        if aws_security_group is not None:
            pulumi.set(__self__, "aws_security_group", aws_security_group)
        if cidr_block is not None:
            pulumi.set(__self__, "cidr_block", cidr_block)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="awsSecurityGroup")
    def aws_security_group(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the AWS security group to add to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        """
        return pulumi.get(self, "aws_security_group")

    @aws_security_group.setter
    def aws_security_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_security_group", value)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        Range of IP addresses in CIDR notation to be added to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Comment to add to the access list entry.

        > **NOTE:** One of the following attributes must set:  `aws_security_group`, `cidr_block`  or `ip_address`.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Single IP address to be added to the access list. Mutually exclusive with `awsSecurityGroup` and `cidrBlock`.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier for the project to which you want to add one or more access list entries.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['ProjectIpAccessListTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['ProjectIpAccessListTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


class ProjectIpAccessList(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_security_group: Optional[pulumi.Input[str]] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[Union['ProjectIpAccessListTimeoutsArgs', 'ProjectIpAccessListTimeoutsArgsDict']]] = None,
                 __props__=None):
        """
        ## # Resource: ProjectIpAccessList

        `ProjectIpAccessList` provides an IP Access List entry resource. The access list grants access from IPs, CIDRs or AWS Security Groups (if VPC Peering is enabled) to clusters within the Project.

        > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

        > **IMPORTANT:**
        When you remove an entry from the access list, existing connections from the removed address(es) may remain open for a variable amount of time. How much time passes before Atlas closes the connection depends on several factors, including how the connection was established, the particular behavior of the application or driver using the address, and the connection protocol (e.g., TCP or UDP). This is particularly important to consider when changing an existing IP address or CIDR block as they cannot be updated via the Provider (comments can however), hence a change will force the destruction and recreation of entries.

        ## Example Usage

        ### Using CIDR Block
        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        test = mongodbatlas.ProjectIpAccessList("test",
            project_id="<PROJECT-ID>",
            cidr_block="1.2.3.4/32",
            comment="cidr block for tf acc testing")
        ```

        ### Using IP Address
        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        test = mongodbatlas.ProjectIpAccessList("test",
            project_id="<PROJECT-ID>",
            ip_address="2.3.4.5",
            comment="ip address for tf acc testing")
        ```

        ### Using an AWS Security Group
        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        test = mongodbatlas.NetworkContainer("test",
            project_id="<PROJECT-ID>",
            atlas_cidr_block="192.168.208.0/21",
            provider_name="AWS",
            region_name="US_EAST_1")
        test_network_peering = mongodbatlas.NetworkPeering("test",
            project_id="<PROJECT-ID>",
            container_id=test.container_id,
            accepter_region_name="us-east-1",
            provider_name="AWS",
            route_table_cidr_block="172.31.0.0/16",
            vpc_id="vpc-0d93d6f69f1578bd8",
            aws_account_id="232589400519")
        test_project_ip_access_list = mongodbatlas.ProjectIpAccessList("test",
            project_id="<PROJECT-ID>",
            aws_security_group="sg-0026348ec11780bd1",
            comment="TestAcc for awsSecurityGroup",
            opts = pulumi.ResourceOptions(depends_on=[test_network_peering]))
        ```

        > **IMPORTANT:** In order to use AWS Security Group(s) VPC Peering must be enabled like above example.

        ## Import

        IP Access List entries can be imported using the `project_id` and `cidr_block` or `ip_address`, e.g.

        ```sh
        $ pulumi import mongodbatlas:index/projectIpAccessList:ProjectIpAccessList test 5d0f1f74cf09a29120e123cd-10.242.88.0/21
        ```
        For more information see: [MongoDB Atlas API Reference.](https://docs.atlas.mongodb.com/reference/api/access-lists/)

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aws_security_group: Unique identifier of the AWS security group to add to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] cidr_block: Range of IP addresses in CIDR notation to be added to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] comment: Comment to add to the access list entry.
               
               > **NOTE:** One of the following attributes must set:  `aws_security_group`, `cidr_block`  or `ip_address`.
        :param pulumi.Input[str] ip_address: Single IP address to be added to the access list. Mutually exclusive with `awsSecurityGroup` and `cidrBlock`.
        :param pulumi.Input[str] project_id: Unique identifier for the project to which you want to add one or more access list entries.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProjectIpAccessListArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## # Resource: ProjectIpAccessList

        `ProjectIpAccessList` provides an IP Access List entry resource. The access list grants access from IPs, CIDRs or AWS Security Groups (if VPC Peering is enabled) to clusters within the Project.

        > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

        > **IMPORTANT:**
        When you remove an entry from the access list, existing connections from the removed address(es) may remain open for a variable amount of time. How much time passes before Atlas closes the connection depends on several factors, including how the connection was established, the particular behavior of the application or driver using the address, and the connection protocol (e.g., TCP or UDP). This is particularly important to consider when changing an existing IP address or CIDR block as they cannot be updated via the Provider (comments can however), hence a change will force the destruction and recreation of entries.

        ## Example Usage

        ### Using CIDR Block
        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        test = mongodbatlas.ProjectIpAccessList("test",
            project_id="<PROJECT-ID>",
            cidr_block="1.2.3.4/32",
            comment="cidr block for tf acc testing")
        ```

        ### Using IP Address
        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        test = mongodbatlas.ProjectIpAccessList("test",
            project_id="<PROJECT-ID>",
            ip_address="2.3.4.5",
            comment="ip address for tf acc testing")
        ```

        ### Using an AWS Security Group
        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        test = mongodbatlas.NetworkContainer("test",
            project_id="<PROJECT-ID>",
            atlas_cidr_block="192.168.208.0/21",
            provider_name="AWS",
            region_name="US_EAST_1")
        test_network_peering = mongodbatlas.NetworkPeering("test",
            project_id="<PROJECT-ID>",
            container_id=test.container_id,
            accepter_region_name="us-east-1",
            provider_name="AWS",
            route_table_cidr_block="172.31.0.0/16",
            vpc_id="vpc-0d93d6f69f1578bd8",
            aws_account_id="232589400519")
        test_project_ip_access_list = mongodbatlas.ProjectIpAccessList("test",
            project_id="<PROJECT-ID>",
            aws_security_group="sg-0026348ec11780bd1",
            comment="TestAcc for awsSecurityGroup",
            opts = pulumi.ResourceOptions(depends_on=[test_network_peering]))
        ```

        > **IMPORTANT:** In order to use AWS Security Group(s) VPC Peering must be enabled like above example.

        ## Import

        IP Access List entries can be imported using the `project_id` and `cidr_block` or `ip_address`, e.g.

        ```sh
        $ pulumi import mongodbatlas:index/projectIpAccessList:ProjectIpAccessList test 5d0f1f74cf09a29120e123cd-10.242.88.0/21
        ```
        For more information see: [MongoDB Atlas API Reference.](https://docs.atlas.mongodb.com/reference/api/access-lists/)

        :param str resource_name: The name of the resource.
        :param ProjectIpAccessListArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectIpAccessListArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_security_group: Optional[pulumi.Input[str]] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[Union['ProjectIpAccessListTimeoutsArgs', 'ProjectIpAccessListTimeoutsArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectIpAccessListArgs.__new__(ProjectIpAccessListArgs)

            __props__.__dict__["aws_security_group"] = aws_security_group
            __props__.__dict__["cidr_block"] = cidr_block
            __props__.__dict__["comment"] = comment
            __props__.__dict__["ip_address"] = ip_address
            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
            __props__.__dict__["timeouts"] = timeouts
        super(ProjectIpAccessList, __self__).__init__(
            'mongodbatlas:index/projectIpAccessList:ProjectIpAccessList',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            aws_security_group: Optional[pulumi.Input[str]] = None,
            cidr_block: Optional[pulumi.Input[str]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            ip_address: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            timeouts: Optional[pulumi.Input[Union['ProjectIpAccessListTimeoutsArgs', 'ProjectIpAccessListTimeoutsArgsDict']]] = None) -> 'ProjectIpAccessList':
        """
        Get an existing ProjectIpAccessList resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aws_security_group: Unique identifier of the AWS security group to add to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] cidr_block: Range of IP addresses in CIDR notation to be added to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        :param pulumi.Input[str] comment: Comment to add to the access list entry.
               
               > **NOTE:** One of the following attributes must set:  `aws_security_group`, `cidr_block`  or `ip_address`.
        :param pulumi.Input[str] ip_address: Single IP address to be added to the access list. Mutually exclusive with `awsSecurityGroup` and `cidrBlock`.
        :param pulumi.Input[str] project_id: Unique identifier for the project to which you want to add one or more access list entries.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectIpAccessListState.__new__(_ProjectIpAccessListState)

        __props__.__dict__["aws_security_group"] = aws_security_group
        __props__.__dict__["cidr_block"] = cidr_block
        __props__.__dict__["comment"] = comment
        __props__.__dict__["ip_address"] = ip_address
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["timeouts"] = timeouts
        return ProjectIpAccessList(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="awsSecurityGroup")
    def aws_security_group(self) -> pulumi.Output[str]:
        """
        Unique identifier of the AWS security group to add to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        """
        return pulumi.get(self, "aws_security_group")

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Output[str]:
        """
        Range of IP addresses in CIDR notation to be added to the access list. Your access list entry can include only one `awsSecurityGroup`, one `cidrBlock`, or one `ipAddress`.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[str]:
        """
        Comment to add to the access list entry.

        > **NOTE:** One of the following attributes must set:  `aws_security_group`, `cidr_block`  or `ip_address`.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[str]:
        """
        Single IP address to be added to the access list. Mutually exclusive with `awsSecurityGroup` and `cidrBlock`.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        Unique identifier for the project to which you want to add one or more access list entries.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def timeouts(self) -> pulumi.Output[Optional['outputs.ProjectIpAccessListTimeouts']]:
        return pulumi.get(self, "timeouts")

