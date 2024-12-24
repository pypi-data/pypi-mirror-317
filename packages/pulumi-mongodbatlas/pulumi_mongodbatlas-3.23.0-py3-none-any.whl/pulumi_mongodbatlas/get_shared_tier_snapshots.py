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

__all__ = [
    'GetSharedTierSnapshotsResult',
    'AwaitableGetSharedTierSnapshotsResult',
    'get_shared_tier_snapshots',
    'get_shared_tier_snapshots_output',
]

@pulumi.output_type
class GetSharedTierSnapshotsResult:
    """
    A collection of values returned by getSharedTierSnapshots.
    """
    def __init__(__self__, cluster_name=None, id=None, project_id=None, results=None, total_count=None):
        if cluster_name and not isinstance(cluster_name, str):
            raise TypeError("Expected argument 'cluster_name' to be a str")
        pulumi.set(__self__, "cluster_name", cluster_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if results and not isinstance(results, list):
            raise TypeError("Expected argument 'results' to be a list")
        pulumi.set(__self__, "results", results)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> str:
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def results(self) -> Sequence['outputs.GetSharedTierSnapshotsResultResult']:
        return pulumi.get(self, "results")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        return pulumi.get(self, "total_count")


class AwaitableGetSharedTierSnapshotsResult(GetSharedTierSnapshotsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharedTierSnapshotsResult(
            cluster_name=self.cluster_name,
            id=self.id,
            project_id=self.project_id,
            results=self.results,
            total_count=self.total_count)


def get_shared_tier_snapshots(cluster_name: Optional[str] = None,
                              project_id: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSharedTierSnapshotsResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getSharedTierSnapshots:getSharedTierSnapshots', __args__, opts=opts, typ=GetSharedTierSnapshotsResult).value

    return AwaitableGetSharedTierSnapshotsResult(
        cluster_name=pulumi.get(__ret__, 'cluster_name'),
        id=pulumi.get(__ret__, 'id'),
        project_id=pulumi.get(__ret__, 'project_id'),
        results=pulumi.get(__ret__, 'results'),
        total_count=pulumi.get(__ret__, 'total_count'))
def get_shared_tier_snapshots_output(cluster_name: Optional[pulumi.Input[str]] = None,
                                     project_id: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSharedTierSnapshotsResult]:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('mongodbatlas:index/getSharedTierSnapshots:getSharedTierSnapshots', __args__, opts=opts, typ=GetSharedTierSnapshotsResult)
    return __ret__.apply(lambda __response__: GetSharedTierSnapshotsResult(
        cluster_name=pulumi.get(__response__, 'cluster_name'),
        id=pulumi.get(__response__, 'id'),
        project_id=pulumi.get(__response__, 'project_id'),
        results=pulumi.get(__response__, 'results'),
        total_count=pulumi.get(__response__, 'total_count')))
