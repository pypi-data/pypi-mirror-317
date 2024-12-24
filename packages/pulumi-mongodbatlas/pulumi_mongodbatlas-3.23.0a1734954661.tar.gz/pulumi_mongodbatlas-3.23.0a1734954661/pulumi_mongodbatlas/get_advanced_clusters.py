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
    'GetAdvancedClustersResult',
    'AwaitableGetAdvancedClustersResult',
    'get_advanced_clusters',
    'get_advanced_clusters_output',
]

@pulumi.output_type
class GetAdvancedClustersResult:
    """
    A collection of values returned by getAdvancedClusters.
    """
    def __init__(__self__, id=None, project_id=None, results=None, use_replication_spec_per_shard=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if results and not isinstance(results, list):
            raise TypeError("Expected argument 'results' to be a list")
        pulumi.set(__self__, "results", results)
        if use_replication_spec_per_shard and not isinstance(use_replication_spec_per_shard, bool):
            raise TypeError("Expected argument 'use_replication_spec_per_shard' to be a bool")
        pulumi.set(__self__, "use_replication_spec_per_shard", use_replication_spec_per_shard)

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
    def results(self) -> Sequence['outputs.GetAdvancedClustersResultResult']:
        """
        A list where each represents a Cluster. See below for more details.
        """
        return pulumi.get(self, "results")

    @property
    @pulumi.getter(name="useReplicationSpecPerShard")
    def use_replication_spec_per_shard(self) -> Optional[bool]:
        return pulumi.get(self, "use_replication_spec_per_shard")


class AwaitableGetAdvancedClustersResult(GetAdvancedClustersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAdvancedClustersResult(
            id=self.id,
            project_id=self.project_id,
            results=self.results,
            use_replication_spec_per_shard=self.use_replication_spec_per_shard)


def get_advanced_clusters(project_id: Optional[str] = None,
                          use_replication_spec_per_shard: Optional[bool] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAdvancedClustersResult:
    """
    ## # Data Source: get_advanced_clusters

    `get_advanced_clusters` describes all Advanced Clusters by the provided project_id. The data source requires your Project ID.

    > **NOTE:** Groups and projects are synonymous terms. You may find group_id in the official documentation.

    > **IMPORTANT:**
    <br> &#8226; Changes to cluster configurations can affect costs. Before making changes, please see [Billing](https://docs.atlas.mongodb.com/billing/).
    <br> &#8226; If your Atlas project contains a custom role that uses actions introduced in a specific MongoDB version, you cannot create a cluster with a MongoDB version less than that version unless you delete the custom role.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    example_advanced_cluster = mongodbatlas.AdvancedCluster("example",
        project_id="<YOUR-PROJECT-ID>",
        name="cluster-test",
        cluster_type="REPLICASET",
        replication_specs=[{
            "region_configs": [{
                "electable_specs": {
                    "instance_size": "M0",
                },
                "provider_name": "TENANT",
                "backing_provider_name": "AWS",
                "region_name": "US_EAST_1",
                "priority": 7,
            }],
        }])
    example = mongodbatlas.get_advanced_clusters_output(project_id=example_advanced_cluster.project_id)
    ```

    **NOTE:** There can only be one M0 cluster per project.

    ## Example using latest sharding configurations with independent shard scaling in the cluster

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    example = mongodbatlas.AdvancedCluster("example",
        project_id="<YOUR-PROJECT-ID>",
        name="cluster-test",
        backup_enabled=False,
        cluster_type="SHARDED",
        replication_specs=[
            {
                "region_configs": [{
                    "electable_specs": {
                        "instance_size": "M30",
                        "disk_iops": 3000,
                        "node_count": 3,
                    },
                    "provider_name": "AWS",
                    "priority": 7,
                    "region_name": "EU_WEST_1",
                }],
            },
            {
                "region_configs": [{
                    "electable_specs": {
                        "instance_size": "M40",
                        "disk_iops": 3000,
                        "node_count": 3,
                    },
                    "provider_name": "AWS",
                    "priority": 7,
                    "region_name": "EU_WEST_1",
                }],
            },
        ])
    example_asym = mongodbatlas.get_advanced_cluster_output(project_id=example.project_id,
        name=example.name,
        use_replication_spec_per_shard=True)
    ```


    :param str project_id: The unique ID for the project to get the clusters.
    :param bool use_replication_spec_per_shard: Set this field to true to allow the data source to use the latest schema representing each shard with an individual `replication_specs` object. This enables representing clusters with independent shard scaling. **Note:** If not set to true, this data source return all clusters except clusters with asymmetric shards.
    """
    __args__ = dict()
    __args__['projectId'] = project_id
    __args__['useReplicationSpecPerShard'] = use_replication_spec_per_shard
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getAdvancedClusters:getAdvancedClusters', __args__, opts=opts, typ=GetAdvancedClustersResult).value

    return AwaitableGetAdvancedClustersResult(
        id=pulumi.get(__ret__, 'id'),
        project_id=pulumi.get(__ret__, 'project_id'),
        results=pulumi.get(__ret__, 'results'),
        use_replication_spec_per_shard=pulumi.get(__ret__, 'use_replication_spec_per_shard'))
def get_advanced_clusters_output(project_id: Optional[pulumi.Input[str]] = None,
                                 use_replication_spec_per_shard: Optional[pulumi.Input[Optional[bool]]] = None,
                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetAdvancedClustersResult]:
    """
    ## # Data Source: get_advanced_clusters

    `get_advanced_clusters` describes all Advanced Clusters by the provided project_id. The data source requires your Project ID.

    > **NOTE:** Groups and projects are synonymous terms. You may find group_id in the official documentation.

    > **IMPORTANT:**
    <br> &#8226; Changes to cluster configurations can affect costs. Before making changes, please see [Billing](https://docs.atlas.mongodb.com/billing/).
    <br> &#8226; If your Atlas project contains a custom role that uses actions introduced in a specific MongoDB version, you cannot create a cluster with a MongoDB version less than that version unless you delete the custom role.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    example_advanced_cluster = mongodbatlas.AdvancedCluster("example",
        project_id="<YOUR-PROJECT-ID>",
        name="cluster-test",
        cluster_type="REPLICASET",
        replication_specs=[{
            "region_configs": [{
                "electable_specs": {
                    "instance_size": "M0",
                },
                "provider_name": "TENANT",
                "backing_provider_name": "AWS",
                "region_name": "US_EAST_1",
                "priority": 7,
            }],
        }])
    example = mongodbatlas.get_advanced_clusters_output(project_id=example_advanced_cluster.project_id)
    ```

    **NOTE:** There can only be one M0 cluster per project.

    ## Example using latest sharding configurations with independent shard scaling in the cluster

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    example = mongodbatlas.AdvancedCluster("example",
        project_id="<YOUR-PROJECT-ID>",
        name="cluster-test",
        backup_enabled=False,
        cluster_type="SHARDED",
        replication_specs=[
            {
                "region_configs": [{
                    "electable_specs": {
                        "instance_size": "M30",
                        "disk_iops": 3000,
                        "node_count": 3,
                    },
                    "provider_name": "AWS",
                    "priority": 7,
                    "region_name": "EU_WEST_1",
                }],
            },
            {
                "region_configs": [{
                    "electable_specs": {
                        "instance_size": "M40",
                        "disk_iops": 3000,
                        "node_count": 3,
                    },
                    "provider_name": "AWS",
                    "priority": 7,
                    "region_name": "EU_WEST_1",
                }],
            },
        ])
    example_asym = mongodbatlas.get_advanced_cluster_output(project_id=example.project_id,
        name=example.name,
        use_replication_spec_per_shard=True)
    ```


    :param str project_id: The unique ID for the project to get the clusters.
    :param bool use_replication_spec_per_shard: Set this field to true to allow the data source to use the latest schema representing each shard with an individual `replication_specs` object. This enables representing clusters with independent shard scaling. **Note:** If not set to true, this data source return all clusters except clusters with asymmetric shards.
    """
    __args__ = dict()
    __args__['projectId'] = project_id
    __args__['useReplicationSpecPerShard'] = use_replication_spec_per_shard
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('mongodbatlas:index/getAdvancedClusters:getAdvancedClusters', __args__, opts=opts, typ=GetAdvancedClustersResult)
    return __ret__.apply(lambda __response__: GetAdvancedClustersResult(
        id=pulumi.get(__response__, 'id'),
        project_id=pulumi.get(__response__, 'project_id'),
        results=pulumi.get(__response__, 'results'),
        use_replication_spec_per_shard=pulumi.get(__response__, 'use_replication_spec_per_shard')))
