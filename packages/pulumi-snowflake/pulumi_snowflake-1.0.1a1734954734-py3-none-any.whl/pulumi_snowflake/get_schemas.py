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
    'GetSchemasResult',
    'AwaitableGetSchemasResult',
    'get_schemas',
    'get_schemas_output',
]

@pulumi.output_type
class GetSchemasResult:
    """
    A collection of values returned by getSchemas.
    """
    def __init__(__self__, id=None, in_=None, like=None, limit=None, schemas=None, starts_with=None, with_describe=None, with_parameters=None):
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
        if schemas and not isinstance(schemas, list):
            raise TypeError("Expected argument 'schemas' to be a list")
        pulumi.set(__self__, "schemas", schemas)
        if starts_with and not isinstance(starts_with, str):
            raise TypeError("Expected argument 'starts_with' to be a str")
        pulumi.set(__self__, "starts_with", starts_with)
        if with_describe and not isinstance(with_describe, bool):
            raise TypeError("Expected argument 'with_describe' to be a bool")
        pulumi.set(__self__, "with_describe", with_describe)
        if with_parameters and not isinstance(with_parameters, bool):
            raise TypeError("Expected argument 'with_parameters' to be a bool")
        pulumi.set(__self__, "with_parameters", with_parameters)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="in")
    def in_(self) -> Optional['outputs.GetSchemasInResult']:
        """
        IN clause to filter the list of streamlits
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
    def limit(self) -> Optional['outputs.GetSchemasLimitResult']:
        """
        Limits the number of rows returned. If the `limit.from` is set, then the limit wll start from the first element matched by the expression. The expression is only used to match with the first element, later on the elements are not matched by the prefix, but you can enforce a certain pattern with `starts_with` or `like`.
        """
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def schemas(self) -> Sequence['outputs.GetSchemasSchemaResult']:
        """
        Holds the aggregated output of all SCHEMA details queries.
        """
        return pulumi.get(self, "schemas")

    @property
    @pulumi.getter(name="startsWith")
    def starts_with(self) -> Optional[str]:
        """
        Filters the output with **case-sensitive** characters indicating the beginning of the object name.
        """
        return pulumi.get(self, "starts_with")

    @property
    @pulumi.getter(name="withDescribe")
    def with_describe(self) -> Optional[bool]:
        """
        Runs DESC SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the description field. By default this value is set to true.
        """
        return pulumi.get(self, "with_describe")

    @property
    @pulumi.getter(name="withParameters")
    def with_parameters(self) -> Optional[bool]:
        """
        Runs SHOW PARAMETERS FOR SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the parameters field as a map. By default this value is set to true.
        """
        return pulumi.get(self, "with_parameters")


class AwaitableGetSchemasResult(GetSchemasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSchemasResult(
            id=self.id,
            in_=self.in_,
            like=self.like,
            limit=self.limit,
            schemas=self.schemas,
            starts_with=self.starts_with,
            with_describe=self.with_describe,
            with_parameters=self.with_parameters)


def get_schemas(in_: Optional[Union['GetSchemasInArgs', 'GetSchemasInArgsDict']] = None,
                like: Optional[str] = None,
                limit: Optional[Union['GetSchemasLimitArgs', 'GetSchemasLimitArgsDict']] = None,
                starts_with: Optional[str] = None,
                with_describe: Optional[bool] = None,
                with_parameters: Optional[bool] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSchemasResult:
    """
    <!-- TODO(SNOW-1844996): Remove this note.-->
    > **Note** Field `WITH PRIVILEGES` is currently missing. It will be added in the future.

    Data source used to get details of filtered schemas. Filtering is aligned with the current possibilities for [SHOW SCHEMAS](https://docs.snowflake.com/en/sql-reference/sql/show-schemas) query. The results of SHOW, DESCRIBE, and SHOW PARAMETERS IN are encapsulated in one output collection.


    :param Union['GetSchemasInArgs', 'GetSchemasInArgsDict'] in_: IN clause to filter the list of streamlits
    :param str like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (`%` and `_`).
    :param Union['GetSchemasLimitArgs', 'GetSchemasLimitArgsDict'] limit: Limits the number of rows returned. If the `limit.from` is set, then the limit wll start from the first element matched by the expression. The expression is only used to match with the first element, later on the elements are not matched by the prefix, but you can enforce a certain pattern with `starts_with` or `like`.
    :param str starts_with: Filters the output with **case-sensitive** characters indicating the beginning of the object name.
    :param bool with_describe: Runs DESC SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the description field. By default this value is set to true.
    :param bool with_parameters: Runs SHOW PARAMETERS FOR SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the parameters field as a map. By default this value is set to true.
    """
    __args__ = dict()
    __args__['in'] = in_
    __args__['like'] = like
    __args__['limit'] = limit
    __args__['startsWith'] = starts_with
    __args__['withDescribe'] = with_describe
    __args__['withParameters'] = with_parameters
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getSchemas:getSchemas', __args__, opts=opts, typ=GetSchemasResult).value

    return AwaitableGetSchemasResult(
        id=pulumi.get(__ret__, 'id'),
        in_=pulumi.get(__ret__, 'in_'),
        like=pulumi.get(__ret__, 'like'),
        limit=pulumi.get(__ret__, 'limit'),
        schemas=pulumi.get(__ret__, 'schemas'),
        starts_with=pulumi.get(__ret__, 'starts_with'),
        with_describe=pulumi.get(__ret__, 'with_describe'),
        with_parameters=pulumi.get(__ret__, 'with_parameters'))
def get_schemas_output(in_: Optional[pulumi.Input[Optional[Union['GetSchemasInArgs', 'GetSchemasInArgsDict']]]] = None,
                       like: Optional[pulumi.Input[Optional[str]]] = None,
                       limit: Optional[pulumi.Input[Optional[Union['GetSchemasLimitArgs', 'GetSchemasLimitArgsDict']]]] = None,
                       starts_with: Optional[pulumi.Input[Optional[str]]] = None,
                       with_describe: Optional[pulumi.Input[Optional[bool]]] = None,
                       with_parameters: Optional[pulumi.Input[Optional[bool]]] = None,
                       opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSchemasResult]:
    """
    <!-- TODO(SNOW-1844996): Remove this note.-->
    > **Note** Field `WITH PRIVILEGES` is currently missing. It will be added in the future.

    Data source used to get details of filtered schemas. Filtering is aligned with the current possibilities for [SHOW SCHEMAS](https://docs.snowflake.com/en/sql-reference/sql/show-schemas) query. The results of SHOW, DESCRIBE, and SHOW PARAMETERS IN are encapsulated in one output collection.


    :param Union['GetSchemasInArgs', 'GetSchemasInArgsDict'] in_: IN clause to filter the list of streamlits
    :param str like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (`%` and `_`).
    :param Union['GetSchemasLimitArgs', 'GetSchemasLimitArgsDict'] limit: Limits the number of rows returned. If the `limit.from` is set, then the limit wll start from the first element matched by the expression. The expression is only used to match with the first element, later on the elements are not matched by the prefix, but you can enforce a certain pattern with `starts_with` or `like`.
    :param str starts_with: Filters the output with **case-sensitive** characters indicating the beginning of the object name.
    :param bool with_describe: Runs DESC SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the description field. By default this value is set to true.
    :param bool with_parameters: Runs SHOW PARAMETERS FOR SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the parameters field as a map. By default this value is set to true.
    """
    __args__ = dict()
    __args__['in'] = in_
    __args__['like'] = like
    __args__['limit'] = limit
    __args__['startsWith'] = starts_with
    __args__['withDescribe'] = with_describe
    __args__['withParameters'] = with_parameters
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('snowflake:index/getSchemas:getSchemas', __args__, opts=opts, typ=GetSchemasResult)
    return __ret__.apply(lambda __response__: GetSchemasResult(
        id=pulumi.get(__response__, 'id'),
        in_=pulumi.get(__response__, 'in_'),
        like=pulumi.get(__response__, 'like'),
        limit=pulumi.get(__response__, 'limit'),
        schemas=pulumi.get(__response__, 'schemas'),
        starts_with=pulumi.get(__response__, 'starts_with'),
        with_describe=pulumi.get(__response__, 'with_describe'),
        with_parameters=pulumi.get(__response__, 'with_parameters')))
