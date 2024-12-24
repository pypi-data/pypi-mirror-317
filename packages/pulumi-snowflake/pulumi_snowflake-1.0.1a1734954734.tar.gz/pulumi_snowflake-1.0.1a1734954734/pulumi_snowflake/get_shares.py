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
    'GetSharesResult',
    'AwaitableGetSharesResult',
    'get_shares',
    'get_shares_output',
]

@pulumi.output_type
class GetSharesResult:
    """
    A collection of values returned by getShares.
    """
    def __init__(__self__, id=None, pattern=None, shares=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if pattern and not isinstance(pattern, str):
            raise TypeError("Expected argument 'pattern' to be a str")
        pulumi.set(__self__, "pattern", pattern)
        if shares and not isinstance(shares, list):
            raise TypeError("Expected argument 'shares' to be a list")
        pulumi.set(__self__, "shares", shares)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def pattern(self) -> Optional[str]:
        """
        Filters the command output by object name.
        """
        return pulumi.get(self, "pattern")

    @property
    @pulumi.getter
    def shares(self) -> Sequence['outputs.GetSharesShareResult']:
        """
        List of all the shares available in the system.
        """
        return pulumi.get(self, "shares")


class AwaitableGetSharesResult(GetSharesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharesResult(
            id=self.id,
            pattern=self.pattern,
            shares=self.shares)


def get_shares(pattern: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSharesResult:
    """
    !> **Caution: Preview Feature** This feature is considered a preview feature in the provider, regardless of the state of the resource in Snowflake. We do not guarantee its stability. It will be reworked and marked as a stable feature in future releases. Breaking changes are expected, even without bumping the major version. To use this feature, add the relevant feature name to `preview_features_enabled field` in the provider configuration. Please always refer to the Getting Help section in our Github repo to best determine how to get help for your questions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    this = snowflake.get_shares()
    ad = snowflake.get_shares(pattern="usage")
    ```


    :param str pattern: Filters the command output by object name.
    """
    __args__ = dict()
    __args__['pattern'] = pattern
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getShares:getShares', __args__, opts=opts, typ=GetSharesResult).value

    return AwaitableGetSharesResult(
        id=pulumi.get(__ret__, 'id'),
        pattern=pulumi.get(__ret__, 'pattern'),
        shares=pulumi.get(__ret__, 'shares'))
def get_shares_output(pattern: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSharesResult]:
    """
    !> **Caution: Preview Feature** This feature is considered a preview feature in the provider, regardless of the state of the resource in Snowflake. We do not guarantee its stability. It will be reworked and marked as a stable feature in future releases. Breaking changes are expected, even without bumping the major version. To use this feature, add the relevant feature name to `preview_features_enabled field` in the provider configuration. Please always refer to the Getting Help section in our Github repo to best determine how to get help for your questions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    this = snowflake.get_shares()
    ad = snowflake.get_shares(pattern="usage")
    ```


    :param str pattern: Filters the command output by object name.
    """
    __args__ = dict()
    __args__['pattern'] = pattern
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('snowflake:index/getShares:getShares', __args__, opts=opts, typ=GetSharesResult)
    return __ret__.apply(lambda __response__: GetSharesResult(
        id=pulumi.get(__response__, 'id'),
        pattern=pulumi.get(__response__, 'pattern'),
        shares=pulumi.get(__response__, 'shares')))
