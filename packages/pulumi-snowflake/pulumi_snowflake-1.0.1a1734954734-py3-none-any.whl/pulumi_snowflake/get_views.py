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

__all__ = [
    'GetViewsResult',
    'AwaitableGetViewsResult',
    'get_views',
    'get_views_output',
]

@pulumi.output_type
class GetViewsResult:
    """
    A collection of values returned by getViews.
    """
    def __init__(__self__, id=None, in_=None, like=None, limit=None, starts_with=None, views=None, with_describe=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if in_ and not isinstance(in_, dict):
            raise TypeError("Expected argument 'in_' to be a dict")
        pulumi.set(__self__, "in_", in_)
        if like and not isinstance(like, str):
            raise TypeError("Expected argument 'like' to be a str")
        pulumi.set(__self__, "like", like)
        if limit and not isinstance(limit, dict):
            raise TypeError("Expected argument 'limit' to be a dict")
        pulumi.set(__self__, "limit", limit)
        if starts_with and not isinstance(starts_with, str):
            raise TypeError("Expected argument 'starts_with' to be a str")
        pulumi.set(__self__, "starts_with", starts_with)
        if views and not isinstance(views, list):
            raise TypeError("Expected argument 'views' to be a list")
        pulumi.set(__self__, "views", views)
        if with_describe and not isinstance(with_describe, bool):
            raise TypeError("Expected argument 'with_describe' to be a bool")
        pulumi.set(__self__, "with_describe", with_describe)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="in")
    def in_(self) -> Optional['outputs.GetViewsInResult']:
        """
        IN clause to filter the list of views
        """
        return pulumi.get(self, "in_")

    @property
    @pulumi.getter
    def like(self) -> Optional[str]:
        """
        Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (`%` and `_`).
        """
        return pulumi.get(self, "like")

    @property
    @pulumi.getter
    def limit(self) -> Optional['outputs.GetViewsLimitResult']:
        """
        Limits the number of rows returned. If the `limit.from` is set, then the limit wll start from the first element matched by the expression. The expression is only used to match with the first element, later on the elements are not matched by the prefix, but you can enforce a certain pattern with `starts_with` or `like`.
        """
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter(name="startsWith")
    def starts_with(self) -> Optional[str]:
        """
        Filters the output with **case-sensitive** characters indicating the beginning of the object name.
        """
        return pulumi.get(self, "starts_with")

    @property
    @pulumi.getter
    def views(self) -> Sequence['outputs.GetViewsViewResult']:
        """
        Holds the aggregated output of all views details queries.
        """
        return pulumi.get(self, "views")

    @property
    @pulumi.getter(name="withDescribe")
    def with_describe(self) -> Optional[bool]:
        """
        Runs DESC VIEW for each view returned by SHOW VIEWS. The output of describe is saved to the description field. By default this value is set to true.
        """
        return pulumi.get(self, "with_describe")


class AwaitableGetViewsResult(GetViewsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetViewsResult(
            id=self.id,
            in_=self.in_,
            like=self.like,
            limit=self.limit,
            starts_with=self.starts_with,
            views=self.views,
            with_describe=self.with_describe)


def get_views(in_: Optional[Union['GetViewsInArgs', 'GetViewsInArgsDict']] = None,
              like: Optional[str] = None,
              limit: Optional[Union['GetViewsLimitArgs', 'GetViewsLimitArgsDict']] = None,
              starts_with: Optional[str] = None,
              with_describe: Optional[bool] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetViewsResult:
    """
    Data source used to get details of filtered views. Filtering is aligned with the current possibilities for [SHOW VIEWS](https://docs.snowflake.com/en/sql-reference/sql/show-views) query (only `like` is supported). The results of SHOW and DESCRIBE are encapsulated in one output collection `views`.


    :param Union['GetViewsInArgs', 'GetViewsInArgsDict'] in_: IN clause to filter the list of views
    :param str like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (`%` and `_`).
    :param Union['GetViewsLimitArgs', 'GetViewsLimitArgsDict'] limit: Limits the number of rows returned. If the `limit.from` is set, then the limit wll start from the first element matched by the expression. The expression is only used to match with the first element, later on the elements are not matched by the prefix, but you can enforce a certain pattern with `starts_with` or `like`.
    :param str starts_with: Filters the output with **case-sensitive** characters indicating the beginning of the object name.
    :param bool with_describe: Runs DESC VIEW for each view returned by SHOW VIEWS. The output of describe is saved to the description field. By default this value is set to true.
    """
    __args__ = dict()
    __args__['in'] = in_
    __args__['like'] = like
    __args__['limit'] = limit
    __args__['startsWith'] = starts_with
    __args__['withDescribe'] = with_describe
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getViews:getViews', __args__, opts=opts, typ=GetViewsResult).value

    return AwaitableGetViewsResult(
        id=pulumi.get(__ret__, 'id'),
        in_=pulumi.get(__ret__, 'in_'),
        like=pulumi.get(__ret__, 'like'),
        limit=pulumi.get(__ret__, 'limit'),
        starts_with=pulumi.get(__ret__, 'starts_with'),
        views=pulumi.get(__ret__, 'views'),
        with_describe=pulumi.get(__ret__, 'with_describe'))
def get_views_output(in_: Optional[pulumi.Input[Optional[Union['GetViewsInArgs', 'GetViewsInArgsDict']]]] = None,
                     like: Optional[pulumi.Input[Optional[str]]] = None,
                     limit: Optional[pulumi.Input[Optional[Union['GetViewsLimitArgs', 'GetViewsLimitArgsDict']]]] = None,
                     starts_with: Optional[pulumi.Input[Optional[str]]] = None,
                     with_describe: Optional[pulumi.Input[Optional[bool]]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetViewsResult]:
    """
    Data source used to get details of filtered views. Filtering is aligned with the current possibilities for [SHOW VIEWS](https://docs.snowflake.com/en/sql-reference/sql/show-views) query (only `like` is supported). The results of SHOW and DESCRIBE are encapsulated in one output collection `views`.


    :param Union['GetViewsInArgs', 'GetViewsInArgsDict'] in_: IN clause to filter the list of views
    :param str like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (`%` and `_`).
    :param Union['GetViewsLimitArgs', 'GetViewsLimitArgsDict'] limit: Limits the number of rows returned. If the `limit.from` is set, then the limit wll start from the first element matched by the expression. The expression is only used to match with the first element, later on the elements are not matched by the prefix, but you can enforce a certain pattern with `starts_with` or `like`.
    :param str starts_with: Filters the output with **case-sensitive** characters indicating the beginning of the object name.
    :param bool with_describe: Runs DESC VIEW for each view returned by SHOW VIEWS. The output of describe is saved to the description field. By default this value is set to true.
    """
    __args__ = dict()
    __args__['in'] = in_
    __args__['like'] = like
    __args__['limit'] = limit
    __args__['startsWith'] = starts_with
    __args__['withDescribe'] = with_describe
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('snowflake:index/getViews:getViews', __args__, opts=opts, typ=GetViewsResult)
    return __ret__.apply(lambda __response__: GetViewsResult(
        id=pulumi.get(__response__, 'id'),
        in_=pulumi.get(__response__, 'in_'),
        like=pulumi.get(__response__, 'like'),
        limit=pulumi.get(__response__, 'limit'),
        starts_with=pulumi.get(__response__, 'starts_with'),
        views=pulumi.get(__response__, 'views'),
        with_describe=pulumi.get(__response__, 'with_describe')))
