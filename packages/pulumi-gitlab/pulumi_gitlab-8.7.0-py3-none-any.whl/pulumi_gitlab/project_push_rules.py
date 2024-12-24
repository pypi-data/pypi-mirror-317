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

__all__ = ['ProjectPushRulesInitArgs', 'ProjectPushRules']

@pulumi.input_type
class ProjectPushRulesInitArgs:
    def __init__(__self__, *,
                 project: pulumi.Input[str],
                 author_email_regex: Optional[pulumi.Input[str]] = None,
                 branch_name_regex: Optional[pulumi.Input[str]] = None,
                 commit_committer_check: Optional[pulumi.Input[bool]] = None,
                 commit_committer_name_check: Optional[pulumi.Input[bool]] = None,
                 commit_message_negative_regex: Optional[pulumi.Input[str]] = None,
                 commit_message_regex: Optional[pulumi.Input[str]] = None,
                 deny_delete_tag: Optional[pulumi.Input[bool]] = None,
                 file_name_regex: Optional[pulumi.Input[str]] = None,
                 max_file_size: Optional[pulumi.Input[int]] = None,
                 member_check: Optional[pulumi.Input[bool]] = None,
                 prevent_secrets: Optional[pulumi.Input[bool]] = None,
                 reject_non_dco_commits: Optional[pulumi.Input[bool]] = None,
                 reject_unsigned_commits: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a ProjectPushRules resource.
        :param pulumi.Input[str] project: The ID or URL-encoded path of the project.
        :param pulumi.Input[str] author_email_regex: All commit author emails must match this regex, e.g. `@my-company.com$`.
        :param pulumi.Input[str] branch_name_regex: All branch names must match this regex, e.g. `(feature|hotfix)\\/*`.
        :param pulumi.Input[bool] commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails.
        :param pulumi.Input[bool] commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.
        :param pulumi.Input[str] commit_message_negative_regex: No commit message is allowed to match this regex, e.g. `ssh\\:\\/\\/`.
        :param pulumi.Input[str] commit_message_regex: All commit messages must match this regex, e.g. `Fixed \\d+\\..*`.
        :param pulumi.Input[bool] deny_delete_tag: Deny deleting a tag.
        :param pulumi.Input[str] file_name_regex: All committed filenames must not match this regex, e.g. `(jar|exe)$`.
        :param pulumi.Input[int] max_file_size: Maximum file size (MB).
        :param pulumi.Input[bool] member_check: Restrict commits by author (email) to existing GitLab users.
        :param pulumi.Input[bool] prevent_secrets: GitLab will reject any files that are likely to contain secrets.
        :param pulumi.Input[bool] reject_non_dco_commits: Reject commit when it’s not DCO certified.
        :param pulumi.Input[bool] reject_unsigned_commits: Reject commit when it’s not signed.
        """
        pulumi.set(__self__, "project", project)
        if author_email_regex is not None:
            pulumi.set(__self__, "author_email_regex", author_email_regex)
        if branch_name_regex is not None:
            pulumi.set(__self__, "branch_name_regex", branch_name_regex)
        if commit_committer_check is not None:
            pulumi.set(__self__, "commit_committer_check", commit_committer_check)
        if commit_committer_name_check is not None:
            pulumi.set(__self__, "commit_committer_name_check", commit_committer_name_check)
        if commit_message_negative_regex is not None:
            pulumi.set(__self__, "commit_message_negative_regex", commit_message_negative_regex)
        if commit_message_regex is not None:
            pulumi.set(__self__, "commit_message_regex", commit_message_regex)
        if deny_delete_tag is not None:
            pulumi.set(__self__, "deny_delete_tag", deny_delete_tag)
        if file_name_regex is not None:
            pulumi.set(__self__, "file_name_regex", file_name_regex)
        if max_file_size is not None:
            pulumi.set(__self__, "max_file_size", max_file_size)
        if member_check is not None:
            pulumi.set(__self__, "member_check", member_check)
        if prevent_secrets is not None:
            pulumi.set(__self__, "prevent_secrets", prevent_secrets)
        if reject_non_dco_commits is not None:
            pulumi.set(__self__, "reject_non_dco_commits", reject_non_dco_commits)
        if reject_unsigned_commits is not None:
            pulumi.set(__self__, "reject_unsigned_commits", reject_unsigned_commits)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        The ID or URL-encoded path of the project.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="authorEmailRegex")
    def author_email_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All commit author emails must match this regex, e.g. `@my-company.com$`.
        """
        return pulumi.get(self, "author_email_regex")

    @author_email_regex.setter
    def author_email_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "author_email_regex", value)

    @property
    @pulumi.getter(name="branchNameRegex")
    def branch_name_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All branch names must match this regex, e.g. `(feature|hotfix)\\/*`.
        """
        return pulumi.get(self, "branch_name_regex")

    @branch_name_regex.setter
    def branch_name_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "branch_name_regex", value)

    @property
    @pulumi.getter(name="commitCommitterCheck")
    def commit_committer_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Users can only push commits to this repository that were committed with one of their own verified emails.
        """
        return pulumi.get(self, "commit_committer_check")

    @commit_committer_check.setter
    def commit_committer_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "commit_committer_check", value)

    @property
    @pulumi.getter(name="commitCommitterNameCheck")
    def commit_committer_name_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.
        """
        return pulumi.get(self, "commit_committer_name_check")

    @commit_committer_name_check.setter
    def commit_committer_name_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "commit_committer_name_check", value)

    @property
    @pulumi.getter(name="commitMessageNegativeRegex")
    def commit_message_negative_regex(self) -> Optional[pulumi.Input[str]]:
        """
        No commit message is allowed to match this regex, e.g. `ssh\\:\\/\\/`.
        """
        return pulumi.get(self, "commit_message_negative_regex")

    @commit_message_negative_regex.setter
    def commit_message_negative_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "commit_message_negative_regex", value)

    @property
    @pulumi.getter(name="commitMessageRegex")
    def commit_message_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All commit messages must match this regex, e.g. `Fixed \\d+\\..*`.
        """
        return pulumi.get(self, "commit_message_regex")

    @commit_message_regex.setter
    def commit_message_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "commit_message_regex", value)

    @property
    @pulumi.getter(name="denyDeleteTag")
    def deny_delete_tag(self) -> Optional[pulumi.Input[bool]]:
        """
        Deny deleting a tag.
        """
        return pulumi.get(self, "deny_delete_tag")

    @deny_delete_tag.setter
    def deny_delete_tag(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "deny_delete_tag", value)

    @property
    @pulumi.getter(name="fileNameRegex")
    def file_name_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All committed filenames must not match this regex, e.g. `(jar|exe)$`.
        """
        return pulumi.get(self, "file_name_regex")

    @file_name_regex.setter
    def file_name_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_name_regex", value)

    @property
    @pulumi.getter(name="maxFileSize")
    def max_file_size(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum file size (MB).
        """
        return pulumi.get(self, "max_file_size")

    @max_file_size.setter
    def max_file_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_file_size", value)

    @property
    @pulumi.getter(name="memberCheck")
    def member_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Restrict commits by author (email) to existing GitLab users.
        """
        return pulumi.get(self, "member_check")

    @member_check.setter
    def member_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "member_check", value)

    @property
    @pulumi.getter(name="preventSecrets")
    def prevent_secrets(self) -> Optional[pulumi.Input[bool]]:
        """
        GitLab will reject any files that are likely to contain secrets.
        """
        return pulumi.get(self, "prevent_secrets")

    @prevent_secrets.setter
    def prevent_secrets(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "prevent_secrets", value)

    @property
    @pulumi.getter(name="rejectNonDcoCommits")
    def reject_non_dco_commits(self) -> Optional[pulumi.Input[bool]]:
        """
        Reject commit when it’s not DCO certified.
        """
        return pulumi.get(self, "reject_non_dco_commits")

    @reject_non_dco_commits.setter
    def reject_non_dco_commits(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reject_non_dco_commits", value)

    @property
    @pulumi.getter(name="rejectUnsignedCommits")
    def reject_unsigned_commits(self) -> Optional[pulumi.Input[bool]]:
        """
        Reject commit when it’s not signed.
        """
        return pulumi.get(self, "reject_unsigned_commits")

    @reject_unsigned_commits.setter
    def reject_unsigned_commits(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reject_unsigned_commits", value)


@pulumi.input_type
class _ProjectPushRulesState:
    def __init__(__self__, *,
                 author_email_regex: Optional[pulumi.Input[str]] = None,
                 branch_name_regex: Optional[pulumi.Input[str]] = None,
                 commit_committer_check: Optional[pulumi.Input[bool]] = None,
                 commit_committer_name_check: Optional[pulumi.Input[bool]] = None,
                 commit_message_negative_regex: Optional[pulumi.Input[str]] = None,
                 commit_message_regex: Optional[pulumi.Input[str]] = None,
                 deny_delete_tag: Optional[pulumi.Input[bool]] = None,
                 file_name_regex: Optional[pulumi.Input[str]] = None,
                 max_file_size: Optional[pulumi.Input[int]] = None,
                 member_check: Optional[pulumi.Input[bool]] = None,
                 prevent_secrets: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 reject_non_dco_commits: Optional[pulumi.Input[bool]] = None,
                 reject_unsigned_commits: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering ProjectPushRules resources.
        :param pulumi.Input[str] author_email_regex: All commit author emails must match this regex, e.g. `@my-company.com$`.
        :param pulumi.Input[str] branch_name_regex: All branch names must match this regex, e.g. `(feature|hotfix)\\/*`.
        :param pulumi.Input[bool] commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails.
        :param pulumi.Input[bool] commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.
        :param pulumi.Input[str] commit_message_negative_regex: No commit message is allowed to match this regex, e.g. `ssh\\:\\/\\/`.
        :param pulumi.Input[str] commit_message_regex: All commit messages must match this regex, e.g. `Fixed \\d+\\..*`.
        :param pulumi.Input[bool] deny_delete_tag: Deny deleting a tag.
        :param pulumi.Input[str] file_name_regex: All committed filenames must not match this regex, e.g. `(jar|exe)$`.
        :param pulumi.Input[int] max_file_size: Maximum file size (MB).
        :param pulumi.Input[bool] member_check: Restrict commits by author (email) to existing GitLab users.
        :param pulumi.Input[bool] prevent_secrets: GitLab will reject any files that are likely to contain secrets.
        :param pulumi.Input[str] project: The ID or URL-encoded path of the project.
        :param pulumi.Input[bool] reject_non_dco_commits: Reject commit when it’s not DCO certified.
        :param pulumi.Input[bool] reject_unsigned_commits: Reject commit when it’s not signed.
        """
        if author_email_regex is not None:
            pulumi.set(__self__, "author_email_regex", author_email_regex)
        if branch_name_regex is not None:
            pulumi.set(__self__, "branch_name_regex", branch_name_regex)
        if commit_committer_check is not None:
            pulumi.set(__self__, "commit_committer_check", commit_committer_check)
        if commit_committer_name_check is not None:
            pulumi.set(__self__, "commit_committer_name_check", commit_committer_name_check)
        if commit_message_negative_regex is not None:
            pulumi.set(__self__, "commit_message_negative_regex", commit_message_negative_regex)
        if commit_message_regex is not None:
            pulumi.set(__self__, "commit_message_regex", commit_message_regex)
        if deny_delete_tag is not None:
            pulumi.set(__self__, "deny_delete_tag", deny_delete_tag)
        if file_name_regex is not None:
            pulumi.set(__self__, "file_name_regex", file_name_regex)
        if max_file_size is not None:
            pulumi.set(__self__, "max_file_size", max_file_size)
        if member_check is not None:
            pulumi.set(__self__, "member_check", member_check)
        if prevent_secrets is not None:
            pulumi.set(__self__, "prevent_secrets", prevent_secrets)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if reject_non_dco_commits is not None:
            pulumi.set(__self__, "reject_non_dco_commits", reject_non_dco_commits)
        if reject_unsigned_commits is not None:
            pulumi.set(__self__, "reject_unsigned_commits", reject_unsigned_commits)

    @property
    @pulumi.getter(name="authorEmailRegex")
    def author_email_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All commit author emails must match this regex, e.g. `@my-company.com$`.
        """
        return pulumi.get(self, "author_email_regex")

    @author_email_regex.setter
    def author_email_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "author_email_regex", value)

    @property
    @pulumi.getter(name="branchNameRegex")
    def branch_name_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All branch names must match this regex, e.g. `(feature|hotfix)\\/*`.
        """
        return pulumi.get(self, "branch_name_regex")

    @branch_name_regex.setter
    def branch_name_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "branch_name_regex", value)

    @property
    @pulumi.getter(name="commitCommitterCheck")
    def commit_committer_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Users can only push commits to this repository that were committed with one of their own verified emails.
        """
        return pulumi.get(self, "commit_committer_check")

    @commit_committer_check.setter
    def commit_committer_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "commit_committer_check", value)

    @property
    @pulumi.getter(name="commitCommitterNameCheck")
    def commit_committer_name_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.
        """
        return pulumi.get(self, "commit_committer_name_check")

    @commit_committer_name_check.setter
    def commit_committer_name_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "commit_committer_name_check", value)

    @property
    @pulumi.getter(name="commitMessageNegativeRegex")
    def commit_message_negative_regex(self) -> Optional[pulumi.Input[str]]:
        """
        No commit message is allowed to match this regex, e.g. `ssh\\:\\/\\/`.
        """
        return pulumi.get(self, "commit_message_negative_regex")

    @commit_message_negative_regex.setter
    def commit_message_negative_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "commit_message_negative_regex", value)

    @property
    @pulumi.getter(name="commitMessageRegex")
    def commit_message_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All commit messages must match this regex, e.g. `Fixed \\d+\\..*`.
        """
        return pulumi.get(self, "commit_message_regex")

    @commit_message_regex.setter
    def commit_message_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "commit_message_regex", value)

    @property
    @pulumi.getter(name="denyDeleteTag")
    def deny_delete_tag(self) -> Optional[pulumi.Input[bool]]:
        """
        Deny deleting a tag.
        """
        return pulumi.get(self, "deny_delete_tag")

    @deny_delete_tag.setter
    def deny_delete_tag(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "deny_delete_tag", value)

    @property
    @pulumi.getter(name="fileNameRegex")
    def file_name_regex(self) -> Optional[pulumi.Input[str]]:
        """
        All committed filenames must not match this regex, e.g. `(jar|exe)$`.
        """
        return pulumi.get(self, "file_name_regex")

    @file_name_regex.setter
    def file_name_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_name_regex", value)

    @property
    @pulumi.getter(name="maxFileSize")
    def max_file_size(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum file size (MB).
        """
        return pulumi.get(self, "max_file_size")

    @max_file_size.setter
    def max_file_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_file_size", value)

    @property
    @pulumi.getter(name="memberCheck")
    def member_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Restrict commits by author (email) to existing GitLab users.
        """
        return pulumi.get(self, "member_check")

    @member_check.setter
    def member_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "member_check", value)

    @property
    @pulumi.getter(name="preventSecrets")
    def prevent_secrets(self) -> Optional[pulumi.Input[bool]]:
        """
        GitLab will reject any files that are likely to contain secrets.
        """
        return pulumi.get(self, "prevent_secrets")

    @prevent_secrets.setter
    def prevent_secrets(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "prevent_secrets", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID or URL-encoded path of the project.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="rejectNonDcoCommits")
    def reject_non_dco_commits(self) -> Optional[pulumi.Input[bool]]:
        """
        Reject commit when it’s not DCO certified.
        """
        return pulumi.get(self, "reject_non_dco_commits")

    @reject_non_dco_commits.setter
    def reject_non_dco_commits(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reject_non_dco_commits", value)

    @property
    @pulumi.getter(name="rejectUnsignedCommits")
    def reject_unsigned_commits(self) -> Optional[pulumi.Input[bool]]:
        """
        Reject commit when it’s not signed.
        """
        return pulumi.get(self, "reject_unsigned_commits")

    @reject_unsigned_commits.setter
    def reject_unsigned_commits(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reject_unsigned_commits", value)


class ProjectPushRules(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 author_email_regex: Optional[pulumi.Input[str]] = None,
                 branch_name_regex: Optional[pulumi.Input[str]] = None,
                 commit_committer_check: Optional[pulumi.Input[bool]] = None,
                 commit_committer_name_check: Optional[pulumi.Input[bool]] = None,
                 commit_message_negative_regex: Optional[pulumi.Input[str]] = None,
                 commit_message_regex: Optional[pulumi.Input[str]] = None,
                 deny_delete_tag: Optional[pulumi.Input[bool]] = None,
                 file_name_regex: Optional[pulumi.Input[str]] = None,
                 max_file_size: Optional[pulumi.Input[int]] = None,
                 member_check: Optional[pulumi.Input[bool]] = None,
                 prevent_secrets: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 reject_non_dco_commits: Optional[pulumi.Input[bool]] = None,
                 reject_unsigned_commits: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_gitlab as gitlab

        sample = gitlab.ProjectPushRules("sample",
            project="42",
            author_email_regex="@gitlab.com$",
            branch_name_regex="(feat|fix)\\\\/*",
            commit_committer_check=True,
            commit_committer_name_check=True,
            commit_message_negative_regex="ssh\\\\:\\\\/\\\\/",
            commit_message_regex="(feat|fix):.*",
            deny_delete_tag=False,
            file_name_regex="(jar|exe)$",
            max_file_size=4,
            member_check=True,
            prevent_secrets=True,
            reject_unsigned_commits=False)
        ```

        ## Import

        Starting in Terraform v1.5.0 you can use an import block to import `gitlab_project_push_rules`. For example:

        terraform

        import {

          to = gitlab_project_push_rules.example

          id = "see CLI command below for ID"

        }

        Import using the CLI is supported using the following syntax:

        Gitlab project push rules can be imported with a key composed of `<project_id>`, e.g.

        ```sh
        $ pulumi import gitlab:index/projectPushRules:ProjectPushRules sample "42"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] author_email_regex: All commit author emails must match this regex, e.g. `@my-company.com$`.
        :param pulumi.Input[str] branch_name_regex: All branch names must match this regex, e.g. `(feature|hotfix)\\/*`.
        :param pulumi.Input[bool] commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails.
        :param pulumi.Input[bool] commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.
        :param pulumi.Input[str] commit_message_negative_regex: No commit message is allowed to match this regex, e.g. `ssh\\:\\/\\/`.
        :param pulumi.Input[str] commit_message_regex: All commit messages must match this regex, e.g. `Fixed \\d+\\..*`.
        :param pulumi.Input[bool] deny_delete_tag: Deny deleting a tag.
        :param pulumi.Input[str] file_name_regex: All committed filenames must not match this regex, e.g. `(jar|exe)$`.
        :param pulumi.Input[int] max_file_size: Maximum file size (MB).
        :param pulumi.Input[bool] member_check: Restrict commits by author (email) to existing GitLab users.
        :param pulumi.Input[bool] prevent_secrets: GitLab will reject any files that are likely to contain secrets.
        :param pulumi.Input[str] project: The ID or URL-encoded path of the project.
        :param pulumi.Input[bool] reject_non_dco_commits: Reject commit when it’s not DCO certified.
        :param pulumi.Input[bool] reject_unsigned_commits: Reject commit when it’s not signed.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProjectPushRulesInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_gitlab as gitlab

        sample = gitlab.ProjectPushRules("sample",
            project="42",
            author_email_regex="@gitlab.com$",
            branch_name_regex="(feat|fix)\\\\/*",
            commit_committer_check=True,
            commit_committer_name_check=True,
            commit_message_negative_regex="ssh\\\\:\\\\/\\\\/",
            commit_message_regex="(feat|fix):.*",
            deny_delete_tag=False,
            file_name_regex="(jar|exe)$",
            max_file_size=4,
            member_check=True,
            prevent_secrets=True,
            reject_unsigned_commits=False)
        ```

        ## Import

        Starting in Terraform v1.5.0 you can use an import block to import `gitlab_project_push_rules`. For example:

        terraform

        import {

          to = gitlab_project_push_rules.example

          id = "see CLI command below for ID"

        }

        Import using the CLI is supported using the following syntax:

        Gitlab project push rules can be imported with a key composed of `<project_id>`, e.g.

        ```sh
        $ pulumi import gitlab:index/projectPushRules:ProjectPushRules sample "42"
        ```

        :param str resource_name: The name of the resource.
        :param ProjectPushRulesInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectPushRulesInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 author_email_regex: Optional[pulumi.Input[str]] = None,
                 branch_name_regex: Optional[pulumi.Input[str]] = None,
                 commit_committer_check: Optional[pulumi.Input[bool]] = None,
                 commit_committer_name_check: Optional[pulumi.Input[bool]] = None,
                 commit_message_negative_regex: Optional[pulumi.Input[str]] = None,
                 commit_message_regex: Optional[pulumi.Input[str]] = None,
                 deny_delete_tag: Optional[pulumi.Input[bool]] = None,
                 file_name_regex: Optional[pulumi.Input[str]] = None,
                 max_file_size: Optional[pulumi.Input[int]] = None,
                 member_check: Optional[pulumi.Input[bool]] = None,
                 prevent_secrets: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 reject_non_dco_commits: Optional[pulumi.Input[bool]] = None,
                 reject_unsigned_commits: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectPushRulesInitArgs.__new__(ProjectPushRulesInitArgs)

            __props__.__dict__["author_email_regex"] = author_email_regex
            __props__.__dict__["branch_name_regex"] = branch_name_regex
            __props__.__dict__["commit_committer_check"] = commit_committer_check
            __props__.__dict__["commit_committer_name_check"] = commit_committer_name_check
            __props__.__dict__["commit_message_negative_regex"] = commit_message_negative_regex
            __props__.__dict__["commit_message_regex"] = commit_message_regex
            __props__.__dict__["deny_delete_tag"] = deny_delete_tag
            __props__.__dict__["file_name_regex"] = file_name_regex
            __props__.__dict__["max_file_size"] = max_file_size
            __props__.__dict__["member_check"] = member_check
            __props__.__dict__["prevent_secrets"] = prevent_secrets
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["reject_non_dco_commits"] = reject_non_dco_commits
            __props__.__dict__["reject_unsigned_commits"] = reject_unsigned_commits
        super(ProjectPushRules, __self__).__init__(
            'gitlab:index/projectPushRules:ProjectPushRules',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            author_email_regex: Optional[pulumi.Input[str]] = None,
            branch_name_regex: Optional[pulumi.Input[str]] = None,
            commit_committer_check: Optional[pulumi.Input[bool]] = None,
            commit_committer_name_check: Optional[pulumi.Input[bool]] = None,
            commit_message_negative_regex: Optional[pulumi.Input[str]] = None,
            commit_message_regex: Optional[pulumi.Input[str]] = None,
            deny_delete_tag: Optional[pulumi.Input[bool]] = None,
            file_name_regex: Optional[pulumi.Input[str]] = None,
            max_file_size: Optional[pulumi.Input[int]] = None,
            member_check: Optional[pulumi.Input[bool]] = None,
            prevent_secrets: Optional[pulumi.Input[bool]] = None,
            project: Optional[pulumi.Input[str]] = None,
            reject_non_dco_commits: Optional[pulumi.Input[bool]] = None,
            reject_unsigned_commits: Optional[pulumi.Input[bool]] = None) -> 'ProjectPushRules':
        """
        Get an existing ProjectPushRules resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] author_email_regex: All commit author emails must match this regex, e.g. `@my-company.com$`.
        :param pulumi.Input[str] branch_name_regex: All branch names must match this regex, e.g. `(feature|hotfix)\\/*`.
        :param pulumi.Input[bool] commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails.
        :param pulumi.Input[bool] commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.
        :param pulumi.Input[str] commit_message_negative_regex: No commit message is allowed to match this regex, e.g. `ssh\\:\\/\\/`.
        :param pulumi.Input[str] commit_message_regex: All commit messages must match this regex, e.g. `Fixed \\d+\\..*`.
        :param pulumi.Input[bool] deny_delete_tag: Deny deleting a tag.
        :param pulumi.Input[str] file_name_regex: All committed filenames must not match this regex, e.g. `(jar|exe)$`.
        :param pulumi.Input[int] max_file_size: Maximum file size (MB).
        :param pulumi.Input[bool] member_check: Restrict commits by author (email) to existing GitLab users.
        :param pulumi.Input[bool] prevent_secrets: GitLab will reject any files that are likely to contain secrets.
        :param pulumi.Input[str] project: The ID or URL-encoded path of the project.
        :param pulumi.Input[bool] reject_non_dco_commits: Reject commit when it’s not DCO certified.
        :param pulumi.Input[bool] reject_unsigned_commits: Reject commit when it’s not signed.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectPushRulesState.__new__(_ProjectPushRulesState)

        __props__.__dict__["author_email_regex"] = author_email_regex
        __props__.__dict__["branch_name_regex"] = branch_name_regex
        __props__.__dict__["commit_committer_check"] = commit_committer_check
        __props__.__dict__["commit_committer_name_check"] = commit_committer_name_check
        __props__.__dict__["commit_message_negative_regex"] = commit_message_negative_regex
        __props__.__dict__["commit_message_regex"] = commit_message_regex
        __props__.__dict__["deny_delete_tag"] = deny_delete_tag
        __props__.__dict__["file_name_regex"] = file_name_regex
        __props__.__dict__["max_file_size"] = max_file_size
        __props__.__dict__["member_check"] = member_check
        __props__.__dict__["prevent_secrets"] = prevent_secrets
        __props__.__dict__["project"] = project
        __props__.__dict__["reject_non_dco_commits"] = reject_non_dco_commits
        __props__.__dict__["reject_unsigned_commits"] = reject_unsigned_commits
        return ProjectPushRules(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authorEmailRegex")
    def author_email_regex(self) -> pulumi.Output[str]:
        """
        All commit author emails must match this regex, e.g. `@my-company.com$`.
        """
        return pulumi.get(self, "author_email_regex")

    @property
    @pulumi.getter(name="branchNameRegex")
    def branch_name_regex(self) -> pulumi.Output[str]:
        """
        All branch names must match this regex, e.g. `(feature|hotfix)\\/*`.
        """
        return pulumi.get(self, "branch_name_regex")

    @property
    @pulumi.getter(name="commitCommitterCheck")
    def commit_committer_check(self) -> pulumi.Output[bool]:
        """
        Users can only push commits to this repository that were committed with one of their own verified emails.
        """
        return pulumi.get(self, "commit_committer_check")

    @property
    @pulumi.getter(name="commitCommitterNameCheck")
    def commit_committer_name_check(self) -> pulumi.Output[bool]:
        """
        Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.
        """
        return pulumi.get(self, "commit_committer_name_check")

    @property
    @pulumi.getter(name="commitMessageNegativeRegex")
    def commit_message_negative_regex(self) -> pulumi.Output[str]:
        """
        No commit message is allowed to match this regex, e.g. `ssh\\:\\/\\/`.
        """
        return pulumi.get(self, "commit_message_negative_regex")

    @property
    @pulumi.getter(name="commitMessageRegex")
    def commit_message_regex(self) -> pulumi.Output[str]:
        """
        All commit messages must match this regex, e.g. `Fixed \\d+\\..*`.
        """
        return pulumi.get(self, "commit_message_regex")

    @property
    @pulumi.getter(name="denyDeleteTag")
    def deny_delete_tag(self) -> pulumi.Output[bool]:
        """
        Deny deleting a tag.
        """
        return pulumi.get(self, "deny_delete_tag")

    @property
    @pulumi.getter(name="fileNameRegex")
    def file_name_regex(self) -> pulumi.Output[str]:
        """
        All committed filenames must not match this regex, e.g. `(jar|exe)$`.
        """
        return pulumi.get(self, "file_name_regex")

    @property
    @pulumi.getter(name="maxFileSize")
    def max_file_size(self) -> pulumi.Output[int]:
        """
        Maximum file size (MB).
        """
        return pulumi.get(self, "max_file_size")

    @property
    @pulumi.getter(name="memberCheck")
    def member_check(self) -> pulumi.Output[bool]:
        """
        Restrict commits by author (email) to existing GitLab users.
        """
        return pulumi.get(self, "member_check")

    @property
    @pulumi.getter(name="preventSecrets")
    def prevent_secrets(self) -> pulumi.Output[bool]:
        """
        GitLab will reject any files that are likely to contain secrets.
        """
        return pulumi.get(self, "prevent_secrets")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID or URL-encoded path of the project.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="rejectNonDcoCommits")
    def reject_non_dco_commits(self) -> pulumi.Output[bool]:
        """
        Reject commit when it’s not DCO certified.
        """
        return pulumi.get(self, "reject_non_dco_commits")

    @property
    @pulumi.getter(name="rejectUnsignedCommits")
    def reject_unsigned_commits(self) -> pulumi.Output[bool]:
        """
        Reject commit when it’s not signed.
        """
        return pulumi.get(self, "reject_unsigned_commits")

