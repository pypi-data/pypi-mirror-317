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

__all__ = ['GrantOwnershipArgs', 'GrantOwnership']

@pulumi.input_type
class GrantOwnershipArgs:
    def __init__(__self__, *,
                 on: pulumi.Input['GrantOwnershipOnArgs'],
                 account_role_name: Optional[pulumi.Input[str]] = None,
                 database_role_name: Optional[pulumi.Input[str]] = None,
                 outbound_privileges: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a GrantOwnership resource.
        :param pulumi.Input['GrantOwnershipOnArgs'] on: Configures which object(s) should transfer their ownership to the specified role.
        :param pulumi.Input[str] account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input[str] outbound_privileges: Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters).
        """
        pulumi.set(__self__, "on", on)
        if account_role_name is not None:
            pulumi.set(__self__, "account_role_name", account_role_name)
        if database_role_name is not None:
            pulumi.set(__self__, "database_role_name", database_role_name)
        if outbound_privileges is not None:
            pulumi.set(__self__, "outbound_privileges", outbound_privileges)

    @property
    @pulumi.getter
    def on(self) -> pulumi.Input['GrantOwnershipOnArgs']:
        """
        Configures which object(s) should transfer their ownership to the specified role.
        """
        return pulumi.get(self, "on")

    @on.setter
    def on(self, value: pulumi.Input['GrantOwnershipOnArgs']):
        pulumi.set(self, "on", value)

    @property
    @pulumi.getter(name="accountRoleName")
    def account_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "account_role_name")

    @account_role_name.setter
    def account_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_role_name", value)

    @property
    @pulumi.getter(name="databaseRoleName")
    def database_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "database_role_name")

    @database_role_name.setter
    def database_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_role_name", value)

    @property
    @pulumi.getter(name="outboundPrivileges")
    def outbound_privileges(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters).
        """
        return pulumi.get(self, "outbound_privileges")

    @outbound_privileges.setter
    def outbound_privileges(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "outbound_privileges", value)


@pulumi.input_type
class _GrantOwnershipState:
    def __init__(__self__, *,
                 account_role_name: Optional[pulumi.Input[str]] = None,
                 database_role_name: Optional[pulumi.Input[str]] = None,
                 on: Optional[pulumi.Input['GrantOwnershipOnArgs']] = None,
                 outbound_privileges: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering GrantOwnership resources.
        :param pulumi.Input[str] account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input['GrantOwnershipOnArgs'] on: Configures which object(s) should transfer their ownership to the specified role.
        :param pulumi.Input[str] outbound_privileges: Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters).
        """
        if account_role_name is not None:
            pulumi.set(__self__, "account_role_name", account_role_name)
        if database_role_name is not None:
            pulumi.set(__self__, "database_role_name", database_role_name)
        if on is not None:
            pulumi.set(__self__, "on", on)
        if outbound_privileges is not None:
            pulumi.set(__self__, "outbound_privileges", outbound_privileges)

    @property
    @pulumi.getter(name="accountRoleName")
    def account_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "account_role_name")

    @account_role_name.setter
    def account_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_role_name", value)

    @property
    @pulumi.getter(name="databaseRoleName")
    def database_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "database_role_name")

    @database_role_name.setter
    def database_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_role_name", value)

    @property
    @pulumi.getter
    def on(self) -> Optional[pulumi.Input['GrantOwnershipOnArgs']]:
        """
        Configures which object(s) should transfer their ownership to the specified role.
        """
        return pulumi.get(self, "on")

    @on.setter
    def on(self, value: Optional[pulumi.Input['GrantOwnershipOnArgs']]):
        pulumi.set(self, "on", value)

    @property
    @pulumi.getter(name="outboundPrivileges")
    def outbound_privileges(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters).
        """
        return pulumi.get(self, "outbound_privileges")

    @outbound_privileges.setter
    def outbound_privileges(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "outbound_privileges", value)


class GrantOwnership(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_role_name: Optional[pulumi.Input[str]] = None,
                 database_role_name: Optional[pulumi.Input[str]] = None,
                 on: Optional[pulumi.Input[Union['GrantOwnershipOnArgs', 'GrantOwnershipOnArgsDict']]] = None,
                 outbound_privileges: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        ### Import examples

        #### OnObject on Schema ToAccountRole

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|COPY|OnObject|SCHEMA|"database_name"."schema_name"'`
        ```

        #### OnObject on Schema ToDatabaseRole

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToDatabaseRole|"database_name"."database_role_name"|COPY|OnObject|SCHEMA|"database_name"."schema_name"'`
        ```

        #### OnObject on Table

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|COPY|OnObject|TABLE|"database_name"."schema_name"."table_name"'`
        ```

        #### OnAll InDatabase

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|REVOKE|OnAll|TABLES|InDatabase|"database_name"'`
        ```

        #### OnAll InSchema

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"||OnAll|TABLES|InSchema|"database_name"."schema_name"'`
        ```

        #### OnFuture InDatabase

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"||OnFuture|TABLES|InDatabase|"database_name"'`
        ```

        #### OnFuture InSchema

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|COPY|OnFuture|TABLES|InSchema|"database_name"."schema_name"'`
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input[Union['GrantOwnershipOnArgs', 'GrantOwnershipOnArgsDict']] on: Configures which object(s) should transfer their ownership to the specified role.
        :param pulumi.Input[str] outbound_privileges: Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GrantOwnershipArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        ### Import examples

        #### OnObject on Schema ToAccountRole

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|COPY|OnObject|SCHEMA|"database_name"."schema_name"'`
        ```

        #### OnObject on Schema ToDatabaseRole

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToDatabaseRole|"database_name"."database_role_name"|COPY|OnObject|SCHEMA|"database_name"."schema_name"'`
        ```

        #### OnObject on Table

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|COPY|OnObject|TABLE|"database_name"."schema_name"."table_name"'`
        ```

        #### OnAll InDatabase

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|REVOKE|OnAll|TABLES|InDatabase|"database_name"'`
        ```

        #### OnAll InSchema

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"||OnAll|TABLES|InSchema|"database_name"."schema_name"'`
        ```

        #### OnFuture InDatabase

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"||OnFuture|TABLES|InDatabase|"database_name"'`
        ```

        #### OnFuture InSchema

        ```sh
        $ pulumi import snowflake:index/grantOwnership:GrantOwnership example 'ToAccountRole|"account_role"|COPY|OnFuture|TABLES|InSchema|"database_name"."schema_name"'`
        ```

        :param str resource_name: The name of the resource.
        :param GrantOwnershipArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GrantOwnershipArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_role_name: Optional[pulumi.Input[str]] = None,
                 database_role_name: Optional[pulumi.Input[str]] = None,
                 on: Optional[pulumi.Input[Union['GrantOwnershipOnArgs', 'GrantOwnershipOnArgsDict']]] = None,
                 outbound_privileges: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GrantOwnershipArgs.__new__(GrantOwnershipArgs)

            __props__.__dict__["account_role_name"] = account_role_name
            __props__.__dict__["database_role_name"] = database_role_name
            if on is None and not opts.urn:
                raise TypeError("Missing required property 'on'")
            __props__.__dict__["on"] = on
            __props__.__dict__["outbound_privileges"] = outbound_privileges
        super(GrantOwnership, __self__).__init__(
            'snowflake:index/grantOwnership:GrantOwnership',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_role_name: Optional[pulumi.Input[str]] = None,
            database_role_name: Optional[pulumi.Input[str]] = None,
            on: Optional[pulumi.Input[Union['GrantOwnershipOnArgs', 'GrantOwnershipOnArgsDict']]] = None,
            outbound_privileges: Optional[pulumi.Input[str]] = None) -> 'GrantOwnership':
        """
        Get an existing GrantOwnership resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_role_name: The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input[str] database_role_name: The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see docs.
        :param pulumi.Input[Union['GrantOwnershipOnArgs', 'GrantOwnershipOnArgsDict']] on: Configures which object(s) should transfer their ownership to the specified role.
        :param pulumi.Input[str] outbound_privileges: Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GrantOwnershipState.__new__(_GrantOwnershipState)

        __props__.__dict__["account_role_name"] = account_role_name
        __props__.__dict__["database_role_name"] = database_role_name
        __props__.__dict__["on"] = on
        __props__.__dict__["outbound_privileges"] = outbound_privileges
        return GrantOwnership(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountRoleName")
    def account_role_name(self) -> pulumi.Output[Optional[str]]:
        """
        The fully qualified name of the account role to which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "account_role_name")

    @property
    @pulumi.getter(name="databaseRoleName")
    def database_role_name(self) -> pulumi.Output[Optional[str]]:
        """
        The fully qualified name of the database role to which privileges will be granted. For more information about this resource, see docs.
        """
        return pulumi.get(self, "database_role_name")

    @property
    @pulumi.getter
    def on(self) -> pulumi.Output['outputs.GrantOwnershipOn']:
        """
        Configures which object(s) should transfer their ownership to the specified role.
        """
        return pulumi.get(self, "on")

    @property
    @pulumi.getter(name="outboundPrivileges")
    def outbound_privileges(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role. Available options are: REVOKE for removing existing privileges and COPY to transfer them with ownership. For more information head over to [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/grant-ownership#optional-parameters).
        """
        return pulumi.get(self, "outbound_privileges")

