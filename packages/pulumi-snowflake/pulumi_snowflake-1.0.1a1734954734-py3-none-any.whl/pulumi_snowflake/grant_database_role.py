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

__all__ = ['GrantDatabaseRoleArgs', 'GrantDatabaseRole']

@pulumi.input_type
class GrantDatabaseRoleArgs:
    def __init__(__self__, *,
                 database_role_name: pulumi.Input[str],
                 parent_database_role_name: Optional[pulumi.Input[str]] = None,
                 parent_role_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a GrantDatabaseRole resource.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role which will be granted to share or parent role. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_database_role_name: The fully qualified name of the parent database role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_role_name: The fully qualified name of the parent account role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] share_name: The fully qualified name of the share on which privileges will be granted. For more information about this resource, see docs.
        """
        pulumi.set(__self__, "database_role_name", database_role_name)
        if parent_database_role_name is not None:
            pulumi.set(__self__, "parent_database_role_name", parent_database_role_name)
        if parent_role_name is not None:
            pulumi.set(__self__, "parent_role_name", parent_role_name)
        if share_name is not None:
            pulumi.set(__self__, "share_name", share_name)

    @property
    @pulumi.getter(name="databaseRoleName")
    def database_role_name(self) -> pulumi.Input[str]:
        """
        The fully qualified name of the database role which will be granted to share or parent role. For more information about this resource, see docs.
        """
        return pulumi.get(self, "database_role_name")

    @database_role_name.setter
    def database_role_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_role_name", value)

    @property
    @pulumi.getter(name="parentDatabaseRoleName")
    def parent_database_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the parent database role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        """
        return pulumi.get(self, "parent_database_role_name")

    @parent_database_role_name.setter
    def parent_database_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_database_role_name", value)

    @property
    @pulumi.getter(name="parentRoleName")
    def parent_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the parent account role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        """
        return pulumi.get(self, "parent_role_name")

    @parent_role_name.setter
    def parent_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_role_name", value)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the share on which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "share_name", value)


@pulumi.input_type
class _GrantDatabaseRoleState:
    def __init__(__self__, *,
                 database_role_name: Optional[pulumi.Input[str]] = None,
                 parent_database_role_name: Optional[pulumi.Input[str]] = None,
                 parent_role_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering GrantDatabaseRole resources.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role which will be granted to share or parent role. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_database_role_name: The fully qualified name of the parent database role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_role_name: The fully qualified name of the parent account role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] share_name: The fully qualified name of the share on which privileges will be granted. For more information about this resource, see docs.
        """
        if database_role_name is not None:
            pulumi.set(__self__, "database_role_name", database_role_name)
        if parent_database_role_name is not None:
            pulumi.set(__self__, "parent_database_role_name", parent_database_role_name)
        if parent_role_name is not None:
            pulumi.set(__self__, "parent_role_name", parent_role_name)
        if share_name is not None:
            pulumi.set(__self__, "share_name", share_name)

    @property
    @pulumi.getter(name="databaseRoleName")
    def database_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the database role which will be granted to share or parent role. For more information about this resource, see docs.
        """
        return pulumi.get(self, "database_role_name")

    @database_role_name.setter
    def database_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_role_name", value)

    @property
    @pulumi.getter(name="parentDatabaseRoleName")
    def parent_database_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the parent database role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        """
        return pulumi.get(self, "parent_database_role_name")

    @parent_database_role_name.setter
    def parent_database_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_database_role_name", value)

    @property
    @pulumi.getter(name="parentRoleName")
    def parent_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the parent account role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        """
        return pulumi.get(self, "parent_role_name")

    @parent_role_name.setter
    def parent_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_role_name", value)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the share on which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "share_name", value)


class GrantDatabaseRole(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_role_name: Optional[pulumi.Input[str]] = None,
                 parent_database_role_name: Optional[pulumi.Input[str]] = None,
                 parent_role_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        format is database_role_name (string) | object_type (ROLE|DATABASE ROLE|SHARE) | grantee_name (string)

        ```sh
        $ pulumi import snowflake:index/grantDatabaseRole:GrantDatabaseRole example '"ABC"."test_db_role"|ROLE|"test_parent_role"'
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role which will be granted to share or parent role. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_database_role_name: The fully qualified name of the parent database role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_role_name: The fully qualified name of the parent account role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] share_name: The fully qualified name of the share on which privileges will be granted. For more information about this resource, see docs.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GrantDatabaseRoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        format is database_role_name (string) | object_type (ROLE|DATABASE ROLE|SHARE) | grantee_name (string)

        ```sh
        $ pulumi import snowflake:index/grantDatabaseRole:GrantDatabaseRole example '"ABC"."test_db_role"|ROLE|"test_parent_role"'
        ```

        :param str resource_name: The name of the resource.
        :param GrantDatabaseRoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GrantDatabaseRoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_role_name: Optional[pulumi.Input[str]] = None,
                 parent_database_role_name: Optional[pulumi.Input[str]] = None,
                 parent_role_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GrantDatabaseRoleArgs.__new__(GrantDatabaseRoleArgs)

            if database_role_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_role_name'")
            __props__.__dict__["database_role_name"] = database_role_name
            __props__.__dict__["parent_database_role_name"] = parent_database_role_name
            __props__.__dict__["parent_role_name"] = parent_role_name
            __props__.__dict__["share_name"] = share_name
        super(GrantDatabaseRole, __self__).__init__(
            'snowflake:index/grantDatabaseRole:GrantDatabaseRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            database_role_name: Optional[pulumi.Input[str]] = None,
            parent_database_role_name: Optional[pulumi.Input[str]] = None,
            parent_role_name: Optional[pulumi.Input[str]] = None,
            share_name: Optional[pulumi.Input[str]] = None) -> 'GrantDatabaseRole':
        """
        Get an existing GrantDatabaseRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role which will be granted to share or parent role. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_database_role_name: The fully qualified name of the parent database role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] parent_role_name: The fully qualified name of the parent account role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        :param pulumi.Input[str] share_name: The fully qualified name of the share on which privileges will be granted. For more information about this resource, see docs.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GrantDatabaseRoleState.__new__(_GrantDatabaseRoleState)

        __props__.__dict__["database_role_name"] = database_role_name
        __props__.__dict__["parent_database_role_name"] = parent_database_role_name
        __props__.__dict__["parent_role_name"] = parent_role_name
        __props__.__dict__["share_name"] = share_name
        return GrantDatabaseRole(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="databaseRoleName")
    def database_role_name(self) -> pulumi.Output[str]:
        """
        The fully qualified name of the database role which will be granted to share or parent role. For more information about this resource, see docs.
        """
        return pulumi.get(self, "database_role_name")

    @property
    @pulumi.getter(name="parentDatabaseRoleName")
    def parent_database_role_name(self) -> pulumi.Output[Optional[str]]:
        """
        The fully qualified name of the parent database role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        """
        return pulumi.get(self, "parent_database_role_name")

    @property
    @pulumi.getter(name="parentRoleName")
    def parent_role_name(self) -> pulumi.Output[Optional[str]]:
        """
        The fully qualified name of the parent account role which will create a parent-child relationship between the roles. For more information about this resource, see docs.
        """
        return pulumi.get(self, "parent_role_name")

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> pulumi.Output[Optional[str]]:
        """
        The fully qualified name of the share on which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "share_name")

