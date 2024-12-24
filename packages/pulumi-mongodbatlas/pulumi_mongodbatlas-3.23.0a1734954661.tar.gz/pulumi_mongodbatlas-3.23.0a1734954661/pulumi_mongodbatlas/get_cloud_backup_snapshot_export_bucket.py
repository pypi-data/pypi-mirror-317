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
    'GetCloudBackupSnapshotExportBucketResult',
    'AwaitableGetCloudBackupSnapshotExportBucketResult',
    'get_cloud_backup_snapshot_export_bucket',
    'get_cloud_backup_snapshot_export_bucket_output',
]

@pulumi.output_type
class GetCloudBackupSnapshotExportBucketResult:
    """
    A collection of values returned by getCloudBackupSnapshotExportBucket.
    """
    def __init__(__self__, bucket_name=None, cloud_provider=None, export_bucket_id=None, iam_role_id=None, id=None, project_id=None, role_id=None, service_url=None, tenant_id=None):
        if bucket_name and not isinstance(bucket_name, str):
            raise TypeError("Expected argument 'bucket_name' to be a str")
        pulumi.set(__self__, "bucket_name", bucket_name)
        if cloud_provider and not isinstance(cloud_provider, str):
            raise TypeError("Expected argument 'cloud_provider' to be a str")
        pulumi.set(__self__, "cloud_provider", cloud_provider)
        if export_bucket_id and not isinstance(export_bucket_id, str):
            raise TypeError("Expected argument 'export_bucket_id' to be a str")
        pulumi.set(__self__, "export_bucket_id", export_bucket_id)
        if iam_role_id and not isinstance(iam_role_id, str):
            raise TypeError("Expected argument 'iam_role_id' to be a str")
        pulumi.set(__self__, "iam_role_id", iam_role_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if role_id and not isinstance(role_id, str):
            raise TypeError("Expected argument 'role_id' to be a str")
        pulumi.set(__self__, "role_id", role_id)
        if service_url and not isinstance(service_url, str):
            raise TypeError("Expected argument 'service_url' to be a str")
        pulumi.set(__self__, "service_url", service_url)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        """
        Name of the bucket that the provided role ID is authorized to access.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="cloudProvider")
    def cloud_provider(self) -> str:
        """
        Name of the provider of the cloud service where Atlas can access the S3 bucket.
        """
        return pulumi.get(self, "cloud_provider")

    @property
    @pulumi.getter(name="exportBucketId")
    def export_bucket_id(self) -> str:
        return pulumi.get(self, "export_bucket_id")

    @property
    @pulumi.getter(name="iamRoleId")
    def iam_role_id(self) -> str:
        """
        Unique identifier of the role that Atlas can use to access the bucket.
        """
        return pulumi.get(self, "iam_role_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> str:
        """
        Unique identifier of the Azure Service Principal that Atlas can use to access the Azure Blob Storage Container.
        """
        return pulumi.get(self, "role_id")

    @property
    @pulumi.getter(name="serviceUrl")
    def service_url(self) -> str:
        """
        URL that identifies the blob Endpoint of the Azure Blob Storage Account.
        """
        return pulumi.get(self, "service_url")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        UUID that identifies the Azure Active Directory Tenant ID.
        """
        return pulumi.get(self, "tenant_id")


class AwaitableGetCloudBackupSnapshotExportBucketResult(GetCloudBackupSnapshotExportBucketResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudBackupSnapshotExportBucketResult(
            bucket_name=self.bucket_name,
            cloud_provider=self.cloud_provider,
            export_bucket_id=self.export_bucket_id,
            iam_role_id=self.iam_role_id,
            id=self.id,
            project_id=self.project_id,
            role_id=self.role_id,
            service_url=self.service_url,
            tenant_id=self.tenant_id)


def get_cloud_backup_snapshot_export_bucket(export_bucket_id: Optional[str] = None,
                                            project_id: Optional[str] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudBackupSnapshotExportBucketResult:
    """
    ## # Data Source: CloudBackupSnapshotExportBucket

    `CloudBackupSnapshotExportBucket` datasource allows you to retrieve all the buckets for the specified project.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_cloud_backup_snapshot_export_bucket = mongodbatlas.CloudBackupSnapshotExportBucket("test",
        project_id="{PROJECT_ID}",
        iam_role_id="{IAM_ROLE_ID}",
        bucket_name="example-bucket",
        cloud_provider="AWS")
    test = mongodbatlas.get_cloud_backup_snapshot_export_bucket_output(project_id="{PROJECT_ID}",
        export_bucket_id=test_cloud_backup_snapshot_export_bucket.export_bucket_id)
    ```


    :param str export_bucket_id: Unique identifier of the snapshot export bucket.
    :param str project_id: The unique identifier of the project for the Atlas cluster.
    """
    __args__ = dict()
    __args__['exportBucketId'] = export_bucket_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getCloudBackupSnapshotExportBucket:getCloudBackupSnapshotExportBucket', __args__, opts=opts, typ=GetCloudBackupSnapshotExportBucketResult).value

    return AwaitableGetCloudBackupSnapshotExportBucketResult(
        bucket_name=pulumi.get(__ret__, 'bucket_name'),
        cloud_provider=pulumi.get(__ret__, 'cloud_provider'),
        export_bucket_id=pulumi.get(__ret__, 'export_bucket_id'),
        iam_role_id=pulumi.get(__ret__, 'iam_role_id'),
        id=pulumi.get(__ret__, 'id'),
        project_id=pulumi.get(__ret__, 'project_id'),
        role_id=pulumi.get(__ret__, 'role_id'),
        service_url=pulumi.get(__ret__, 'service_url'),
        tenant_id=pulumi.get(__ret__, 'tenant_id'))
def get_cloud_backup_snapshot_export_bucket_output(export_bucket_id: Optional[pulumi.Input[str]] = None,
                                                   project_id: Optional[pulumi.Input[str]] = None,
                                                   opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetCloudBackupSnapshotExportBucketResult]:
    """
    ## # Data Source: CloudBackupSnapshotExportBucket

    `CloudBackupSnapshotExportBucket` datasource allows you to retrieve all the buckets for the specified project.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_cloud_backup_snapshot_export_bucket = mongodbatlas.CloudBackupSnapshotExportBucket("test",
        project_id="{PROJECT_ID}",
        iam_role_id="{IAM_ROLE_ID}",
        bucket_name="example-bucket",
        cloud_provider="AWS")
    test = mongodbatlas.get_cloud_backup_snapshot_export_bucket_output(project_id="{PROJECT_ID}",
        export_bucket_id=test_cloud_backup_snapshot_export_bucket.export_bucket_id)
    ```


    :param str export_bucket_id: Unique identifier of the snapshot export bucket.
    :param str project_id: The unique identifier of the project for the Atlas cluster.
    """
    __args__ = dict()
    __args__['exportBucketId'] = export_bucket_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('mongodbatlas:index/getCloudBackupSnapshotExportBucket:getCloudBackupSnapshotExportBucket', __args__, opts=opts, typ=GetCloudBackupSnapshotExportBucketResult)
    return __ret__.apply(lambda __response__: GetCloudBackupSnapshotExportBucketResult(
        bucket_name=pulumi.get(__response__, 'bucket_name'),
        cloud_provider=pulumi.get(__response__, 'cloud_provider'),
        export_bucket_id=pulumi.get(__response__, 'export_bucket_id'),
        iam_role_id=pulumi.get(__response__, 'iam_role_id'),
        id=pulumi.get(__response__, 'id'),
        project_id=pulumi.get(__response__, 'project_id'),
        role_id=pulumi.get(__response__, 'role_id'),
        service_url=pulumi.get(__response__, 'service_url'),
        tenant_id=pulumi.get(__response__, 'tenant_id')))
