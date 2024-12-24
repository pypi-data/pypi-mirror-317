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
    'GetProjectApiKeyResult',
    'AwaitableGetProjectApiKeyResult',
    'get_project_api_key',
    'get_project_api_key_output',
]

@pulumi.output_type
class GetProjectApiKeyResult:
    """
    A collection of values returned by getProjectApiKey.
    """
    def __init__(__self__, api_key_id=None, description=None, id=None, private_key=None, project_assignments=None, project_id=None, public_key=None):
        if api_key_id and not isinstance(api_key_id, str):
            raise TypeError("Expected argument 'api_key_id' to be a str")
        pulumi.set(__self__, "api_key_id", api_key_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if private_key and not isinstance(private_key, str):
            raise TypeError("Expected argument 'private_key' to be a str")
        pulumi.set(__self__, "private_key", private_key)
        if project_assignments and not isinstance(project_assignments, list):
            raise TypeError("Expected argument 'project_assignments' to be a list")
        pulumi.set(__self__, "project_assignments", project_assignments)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if public_key and not isinstance(public_key, str):
            raise TypeError("Expected argument 'public_key' to be a str")
        pulumi.set(__self__, "public_key", public_key)

    @property
    @pulumi.getter(name="apiKeyId")
    def api_key_id(self) -> str:
        return pulumi.get(self, "api_key_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of this Project API key.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="privateKey")
    def private_key(self) -> str:
        """
        Private key for this Organization API key.
        """
        return pulumi.get(self, "private_key")

    @property
    @pulumi.getter(name="projectAssignments")
    def project_assignments(self) -> Sequence['outputs.GetProjectApiKeyProjectAssignmentResult']:
        return pulumi.get(self, "project_assignments")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        """
        Project ID to assign to Access Key
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> str:
        """
        Public key for this Organization API key.
        """
        return pulumi.get(self, "public_key")


class AwaitableGetProjectApiKeyResult(GetProjectApiKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectApiKeyResult(
            api_key_id=self.api_key_id,
            description=self.description,
            id=self.id,
            private_key=self.private_key,
            project_assignments=self.project_assignments,
            project_id=self.project_id,
            public_key=self.public_key)


def get_project_api_key(api_key_id: Optional[str] = None,
                        project_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectApiKeyResult:
    """
    ## Example Usage

    ### Using project_id and api_key_id attribute to query
    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_project_api_key = mongodbatlas.ProjectApiKey("test",
        description="Description of your API key",
        project_assignments=[{
            "project_id": "64259ee860c43338194b0f8e",
            "role_names": ["GROUP_READ_ONLY"],
        }])
    test = mongodbatlas.get_project_api_key(project_id="64259ee860c43338194b0f8e",
        api_key_id=test_mongodbatlas_api_key["apiKeyId"])
    ```


    :param str api_key_id: Unique identifier for this Project API key.
    :param str project_id: The unique ID for the project.
    """
    __args__ = dict()
    __args__['apiKeyId'] = api_key_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getProjectApiKey:getProjectApiKey', __args__, opts=opts, typ=GetProjectApiKeyResult).value

    return AwaitableGetProjectApiKeyResult(
        api_key_id=pulumi.get(__ret__, 'api_key_id'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        private_key=pulumi.get(__ret__, 'private_key'),
        project_assignments=pulumi.get(__ret__, 'project_assignments'),
        project_id=pulumi.get(__ret__, 'project_id'),
        public_key=pulumi.get(__ret__, 'public_key'))
def get_project_api_key_output(api_key_id: Optional[pulumi.Input[str]] = None,
                               project_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetProjectApiKeyResult]:
    """
    ## Example Usage

    ### Using project_id and api_key_id attribute to query
    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_project_api_key = mongodbatlas.ProjectApiKey("test",
        description="Description of your API key",
        project_assignments=[{
            "project_id": "64259ee860c43338194b0f8e",
            "role_names": ["GROUP_READ_ONLY"],
        }])
    test = mongodbatlas.get_project_api_key(project_id="64259ee860c43338194b0f8e",
        api_key_id=test_mongodbatlas_api_key["apiKeyId"])
    ```


    :param str api_key_id: Unique identifier for this Project API key.
    :param str project_id: The unique ID for the project.
    """
    __args__ = dict()
    __args__['apiKeyId'] = api_key_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('mongodbatlas:index/getProjectApiKey:getProjectApiKey', __args__, opts=opts, typ=GetProjectApiKeyResult)
    return __ret__.apply(lambda __response__: GetProjectApiKeyResult(
        api_key_id=pulumi.get(__response__, 'api_key_id'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        private_key=pulumi.get(__response__, 'private_key'),
        project_assignments=pulumi.get(__response__, 'project_assignments'),
        project_id=pulumi.get(__response__, 'project_id'),
        public_key=pulumi.get(__response__, 'public_key')))
