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

__all__ = ['AccountAuthenticationPolicyAttachmentArgs', 'AccountAuthenticationPolicyAttachment']

@pulumi.input_type
class AccountAuthenticationPolicyAttachmentArgs:
    def __init__(__self__, *,
                 authentication_policy: pulumi.Input[str]):
        """
        The set of arguments for constructing a AccountAuthenticationPolicyAttachment resource.
        :param pulumi.Input[str] authentication_policy: Qualified name (`"db"."schema"."policy_name"`) of the authentication policy to apply to the current account.
        """
        pulumi.set(__self__, "authentication_policy", authentication_policy)

    @property
    @pulumi.getter(name="authenticationPolicy")
    def authentication_policy(self) -> pulumi.Input[str]:
        """
        Qualified name (`"db"."schema"."policy_name"`) of the authentication policy to apply to the current account.
        """
        return pulumi.get(self, "authentication_policy")

    @authentication_policy.setter
    def authentication_policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "authentication_policy", value)


@pulumi.input_type
class _AccountAuthenticationPolicyAttachmentState:
    def __init__(__self__, *,
                 authentication_policy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccountAuthenticationPolicyAttachment resources.
        :param pulumi.Input[str] authentication_policy: Qualified name (`"db"."schema"."policy_name"`) of the authentication policy to apply to the current account.
        """
        if authentication_policy is not None:
            pulumi.set(__self__, "authentication_policy", authentication_policy)

    @property
    @pulumi.getter(name="authenticationPolicy")
    def authentication_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Qualified name (`"db"."schema"."policy_name"`) of the authentication policy to apply to the current account.
        """
        return pulumi.get(self, "authentication_policy")

    @authentication_policy.setter
    def authentication_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication_policy", value)


class AccountAuthenticationPolicyAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a AccountAuthenticationPolicyAttachment resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_policy: Qualified name (`"db"."schema"."policy_name"`) of the authentication policy to apply to the current account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountAuthenticationPolicyAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a AccountAuthenticationPolicyAttachment resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param AccountAuthenticationPolicyAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountAuthenticationPolicyAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountAuthenticationPolicyAttachmentArgs.__new__(AccountAuthenticationPolicyAttachmentArgs)

            if authentication_policy is None and not opts.urn:
                raise TypeError("Missing required property 'authentication_policy'")
            __props__.__dict__["authentication_policy"] = authentication_policy
        super(AccountAuthenticationPolicyAttachment, __self__).__init__(
            'snowflake:index/accountAuthenticationPolicyAttachment:AccountAuthenticationPolicyAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            authentication_policy: Optional[pulumi.Input[str]] = None) -> 'AccountAuthenticationPolicyAttachment':
        """
        Get an existing AccountAuthenticationPolicyAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_policy: Qualified name (`"db"."schema"."policy_name"`) of the authentication policy to apply to the current account.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountAuthenticationPolicyAttachmentState.__new__(_AccountAuthenticationPolicyAttachmentState)

        __props__.__dict__["authentication_policy"] = authentication_policy
        return AccountAuthenticationPolicyAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authenticationPolicy")
    def authentication_policy(self) -> pulumi.Output[str]:
        """
        Qualified name (`"db"."schema"."policy_name"`) of the authentication policy to apply to the current account.
        """
        return pulumi.get(self, "authentication_policy")

