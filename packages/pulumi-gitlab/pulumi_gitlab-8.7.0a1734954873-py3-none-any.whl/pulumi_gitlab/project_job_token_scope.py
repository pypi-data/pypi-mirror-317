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

__all__ = ['ProjectJobTokenScopeArgs', 'ProjectJobTokenScope']

@pulumi.input_type
class ProjectJobTokenScopeArgs:
    def __init__(__self__, *,
                 project: pulumi.Input[str],
                 target_project_id: pulumi.Input[int]):
        """
        The set of arguments for constructing a ProjectJobTokenScope resource.
        :param pulumi.Input[str] project: The ID or full path of the project.
        :param pulumi.Input[int] target_project_id: The ID of the project that is in the CI/CD job token inbound allowlist.
        """
        pulumi.set(__self__, "project", project)
        pulumi.set(__self__, "target_project_id", target_project_id)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        The ID or full path of the project.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="targetProjectId")
    def target_project_id(self) -> pulumi.Input[int]:
        """
        The ID of the project that is in the CI/CD job token inbound allowlist.
        """
        return pulumi.get(self, "target_project_id")

    @target_project_id.setter
    def target_project_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "target_project_id", value)


@pulumi.input_type
class _ProjectJobTokenScopeState:
    def __init__(__self__, *,
                 project: Optional[pulumi.Input[str]] = None,
                 target_project_id: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering ProjectJobTokenScope resources.
        :param pulumi.Input[str] project: The ID or full path of the project.
        :param pulumi.Input[int] target_project_id: The ID of the project that is in the CI/CD job token inbound allowlist.
        """
        if project is not None:
            pulumi.set(__self__, "project", project)
        if target_project_id is not None:
            pulumi.set(__self__, "target_project_id", target_project_id)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID or full path of the project.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="targetProjectId")
    def target_project_id(self) -> Optional[pulumi.Input[int]]:
        """
        The ID of the project that is in the CI/CD job token inbound allowlist.
        """
        return pulumi.get(self, "target_project_id")

    @target_project_id.setter
    def target_project_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "target_project_id", value)


class ProjectJobTokenScope(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target_project_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        The `ProjectJobTokenScope` resource allows to manage the CI/CD Job Token scope in a project.
        Any projects added to the CI/CD Job Token scope outside of TF will be untouched by the resource.

        > Conflicts with the use of `ProjectJobTokenScopes` when used on the same project. Use one or the other to ensure the desired state.

        **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/project_job_token_scopes.html)

        ## Import

        Starting in Terraform v1.5.0 you can use an import block to import `gitlab_project_job_token_scope`. For example:

        terraform

        import {

          to = gitlab_project_job_token_scope.example

          id = "see CLI command below for ID"

        }

        Import using the CLI is supported using the following syntax:

        GitLab project job token scopes can be imported using an id made up of `projectId:targetProjectId`, e.g.

        ```sh
        $ pulumi import gitlab:index/projectJobTokenScope:ProjectJobTokenScope bar 123:321
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] project: The ID or full path of the project.
        :param pulumi.Input[int] target_project_id: The ID of the project that is in the CI/CD job token inbound allowlist.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProjectJobTokenScopeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The `ProjectJobTokenScope` resource allows to manage the CI/CD Job Token scope in a project.
        Any projects added to the CI/CD Job Token scope outside of TF will be untouched by the resource.

        > Conflicts with the use of `ProjectJobTokenScopes` when used on the same project. Use one or the other to ensure the desired state.

        **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/project_job_token_scopes.html)

        ## Import

        Starting in Terraform v1.5.0 you can use an import block to import `gitlab_project_job_token_scope`. For example:

        terraform

        import {

          to = gitlab_project_job_token_scope.example

          id = "see CLI command below for ID"

        }

        Import using the CLI is supported using the following syntax:

        GitLab project job token scopes can be imported using an id made up of `projectId:targetProjectId`, e.g.

        ```sh
        $ pulumi import gitlab:index/projectJobTokenScope:ProjectJobTokenScope bar 123:321
        ```

        :param str resource_name: The name of the resource.
        :param ProjectJobTokenScopeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectJobTokenScopeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target_project_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectJobTokenScopeArgs.__new__(ProjectJobTokenScopeArgs)

            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            if target_project_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_project_id'")
            __props__.__dict__["target_project_id"] = target_project_id
        super(ProjectJobTokenScope, __self__).__init__(
            'gitlab:index/projectJobTokenScope:ProjectJobTokenScope',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            project: Optional[pulumi.Input[str]] = None,
            target_project_id: Optional[pulumi.Input[int]] = None) -> 'ProjectJobTokenScope':
        """
        Get an existing ProjectJobTokenScope resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] project: The ID or full path of the project.
        :param pulumi.Input[int] target_project_id: The ID of the project that is in the CI/CD job token inbound allowlist.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectJobTokenScopeState.__new__(_ProjectJobTokenScopeState)

        __props__.__dict__["project"] = project
        __props__.__dict__["target_project_id"] = target_project_id
        return ProjectJobTokenScope(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID or full path of the project.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="targetProjectId")
    def target_project_id(self) -> pulumi.Output[int]:
        """
        The ID of the project that is in the CI/CD job token inbound allowlist.
        """
        return pulumi.get(self, "target_project_id")

