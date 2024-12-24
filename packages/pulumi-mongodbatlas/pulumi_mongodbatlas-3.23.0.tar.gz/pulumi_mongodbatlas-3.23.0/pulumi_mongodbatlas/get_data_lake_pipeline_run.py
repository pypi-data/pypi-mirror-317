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
    'GetDataLakePipelineRunResult',
    'AwaitableGetDataLakePipelineRunResult',
    'get_data_lake_pipeline_run',
    'get_data_lake_pipeline_run_output',
]

@pulumi.output_type
class GetDataLakePipelineRunResult:
    """
    A collection of values returned by getDataLakePipelineRun.
    """
    def __init__(__self__, backup_frequency_type=None, created_date=None, dataset_name=None, id=None, last_updated_date=None, phase=None, pipeline_id=None, pipeline_name=None, pipeline_run_id=None, project_id=None, snapshot_id=None, state=None, stats=None):
        if backup_frequency_type and not isinstance(backup_frequency_type, str):
            raise TypeError("Expected argument 'backup_frequency_type' to be a str")
        pulumi.set(__self__, "backup_frequency_type", backup_frequency_type)
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if dataset_name and not isinstance(dataset_name, str):
            raise TypeError("Expected argument 'dataset_name' to be a str")
        pulumi.set(__self__, "dataset_name", dataset_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_updated_date and not isinstance(last_updated_date, str):
            raise TypeError("Expected argument 'last_updated_date' to be a str")
        pulumi.set(__self__, "last_updated_date", last_updated_date)
        if phase and not isinstance(phase, str):
            raise TypeError("Expected argument 'phase' to be a str")
        pulumi.set(__self__, "phase", phase)
        if pipeline_id and not isinstance(pipeline_id, str):
            raise TypeError("Expected argument 'pipeline_id' to be a str")
        pulumi.set(__self__, "pipeline_id", pipeline_id)
        if pipeline_name and not isinstance(pipeline_name, str):
            raise TypeError("Expected argument 'pipeline_name' to be a str")
        pulumi.set(__self__, "pipeline_name", pipeline_name)
        if pipeline_run_id and not isinstance(pipeline_run_id, str):
            raise TypeError("Expected argument 'pipeline_run_id' to be a str")
        pulumi.set(__self__, "pipeline_run_id", pipeline_run_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if snapshot_id and not isinstance(snapshot_id, str):
            raise TypeError("Expected argument 'snapshot_id' to be a str")
        pulumi.set(__self__, "snapshot_id", snapshot_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if stats and not isinstance(stats, list):
            raise TypeError("Expected argument 'stats' to be a list")
        pulumi.set(__self__, "stats", stats)

    @property
    @pulumi.getter(name="backupFrequencyType")
    def backup_frequency_type(self) -> str:
        """
        Backup schedule interval of the Data Lake Pipeline.
        """
        return pulumi.get(self, "backup_frequency_type")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        Timestamp that indicates when the pipeline run was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="datasetName")
    def dataset_name(self) -> str:
        """
        Human-readable label that identifies the dataset that Atlas generates during this pipeline run.
        """
        return pulumi.get(self, "dataset_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Unique 24-hexadecimal character string that identifies a Data Lake Pipeline run.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> str:
        """
        Unique 24-hexadecimal character string that identifies a Data Lake Pipeline run.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter
    def phase(self) -> str:
        """
        Processing phase of the Data Lake Pipeline.
        """
        return pulumi.get(self, "phase")

    @property
    @pulumi.getter(name="pipelineId")
    def pipeline_id(self) -> str:
        """
        Unique 24-hexadecimal character string that identifies a Data Lake Pipeline.
        """
        return pulumi.get(self, "pipeline_id")

    @property
    @pulumi.getter(name="pipelineName")
    def pipeline_name(self) -> str:
        return pulumi.get(self, "pipeline_name")

    @property
    @pulumi.getter(name="pipelineRunId")
    def pipeline_run_id(self) -> str:
        return pulumi.get(self, "pipeline_run_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> str:
        """
        Unique 24-hexadecimal character string that identifies the snapshot of a cluster.
        """
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        State of the pipeline run.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def stats(self) -> Sequence['outputs.GetDataLakePipelineRunStatResult']:
        """
        Runtime statistics for this Data Lake Pipeline run.
        """
        return pulumi.get(self, "stats")


class AwaitableGetDataLakePipelineRunResult(GetDataLakePipelineRunResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDataLakePipelineRunResult(
            backup_frequency_type=self.backup_frequency_type,
            created_date=self.created_date,
            dataset_name=self.dataset_name,
            id=self.id,
            last_updated_date=self.last_updated_date,
            phase=self.phase,
            pipeline_id=self.pipeline_id,
            pipeline_name=self.pipeline_name,
            pipeline_run_id=self.pipeline_run_id,
            project_id=self.project_id,
            snapshot_id=self.snapshot_id,
            state=self.state,
            stats=self.stats)


def get_data_lake_pipeline_run(pipeline_name: Optional[str] = None,
                               pipeline_run_id: Optional[str] = None,
                               project_id: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDataLakePipelineRunResult:
    """
    **WARNING:** Data Lake is deprecated. To learn more, see <https://dochub.mongodb.org/core/data-lake-deprecation>

    `get_data_lake_pipeline_run` describes a Data Lake Pipeline Run.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.


    :param str pipeline_name: Human-readable label that identifies the Data Lake Pipeline.
    :param str pipeline_run_id: Unique 24-hexadecimal character string that identifies a Data Lake Pipeline run.
    :param str project_id: Unique 24-hexadecimal digit string that identifies your project.
    """
    __args__ = dict()
    __args__['pipelineName'] = pipeline_name
    __args__['pipelineRunId'] = pipeline_run_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getDataLakePipelineRun:getDataLakePipelineRun', __args__, opts=opts, typ=GetDataLakePipelineRunResult).value

    return AwaitableGetDataLakePipelineRunResult(
        backup_frequency_type=pulumi.get(__ret__, 'backup_frequency_type'),
        created_date=pulumi.get(__ret__, 'created_date'),
        dataset_name=pulumi.get(__ret__, 'dataset_name'),
        id=pulumi.get(__ret__, 'id'),
        last_updated_date=pulumi.get(__ret__, 'last_updated_date'),
        phase=pulumi.get(__ret__, 'phase'),
        pipeline_id=pulumi.get(__ret__, 'pipeline_id'),
        pipeline_name=pulumi.get(__ret__, 'pipeline_name'),
        pipeline_run_id=pulumi.get(__ret__, 'pipeline_run_id'),
        project_id=pulumi.get(__ret__, 'project_id'),
        snapshot_id=pulumi.get(__ret__, 'snapshot_id'),
        state=pulumi.get(__ret__, 'state'),
        stats=pulumi.get(__ret__, 'stats'))
def get_data_lake_pipeline_run_output(pipeline_name: Optional[pulumi.Input[str]] = None,
                                      pipeline_run_id: Optional[pulumi.Input[str]] = None,
                                      project_id: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetDataLakePipelineRunResult]:
    """
    **WARNING:** Data Lake is deprecated. To learn more, see <https://dochub.mongodb.org/core/data-lake-deprecation>

    `get_data_lake_pipeline_run` describes a Data Lake Pipeline Run.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.


    :param str pipeline_name: Human-readable label that identifies the Data Lake Pipeline.
    :param str pipeline_run_id: Unique 24-hexadecimal character string that identifies a Data Lake Pipeline run.
    :param str project_id: Unique 24-hexadecimal digit string that identifies your project.
    """
    __args__ = dict()
    __args__['pipelineName'] = pipeline_name
    __args__['pipelineRunId'] = pipeline_run_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('mongodbatlas:index/getDataLakePipelineRun:getDataLakePipelineRun', __args__, opts=opts, typ=GetDataLakePipelineRunResult)
    return __ret__.apply(lambda __response__: GetDataLakePipelineRunResult(
        backup_frequency_type=pulumi.get(__response__, 'backup_frequency_type'),
        created_date=pulumi.get(__response__, 'created_date'),
        dataset_name=pulumi.get(__response__, 'dataset_name'),
        id=pulumi.get(__response__, 'id'),
        last_updated_date=pulumi.get(__response__, 'last_updated_date'),
        phase=pulumi.get(__response__, 'phase'),
        pipeline_id=pulumi.get(__response__, 'pipeline_id'),
        pipeline_name=pulumi.get(__response__, 'pipeline_name'),
        pipeline_run_id=pulumi.get(__response__, 'pipeline_run_id'),
        project_id=pulumi.get(__response__, 'project_id'),
        snapshot_id=pulumi.get(__response__, 'snapshot_id'),
        state=pulumi.get(__response__, 'state'),
        stats=pulumi.get(__response__, 'stats')))
