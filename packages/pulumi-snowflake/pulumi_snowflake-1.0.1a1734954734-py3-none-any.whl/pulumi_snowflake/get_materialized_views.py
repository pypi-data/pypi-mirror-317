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
    'GetMaterializedViewsResult',
    'AwaitableGetMaterializedViewsResult',
    'get_materialized_views',
    'get_materialized_views_output',
]

@pulumi.output_type
class GetMaterializedViewsResult:
    """
    A collection of values returned by getMaterializedViews.
    """
    def __init__(__self__, database=None, id=None, materialized_views=None, schema=None):
        if database and not isinstance(database, str):
            raise TypeError("Expected argument 'database' to be a str")
        pulumi.set(__self__, "database", database)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if materialized_views and not isinstance(materialized_views, list):
            raise TypeError("Expected argument 'materialized_views' to be a list")
        pulumi.set(__self__, "materialized_views", materialized_views)
        if schema and not isinstance(schema, str):
            raise TypeError("Expected argument 'schema' to be a str")
        pulumi.set(__self__, "schema", schema)

    @property
    @pulumi.getter
    def database(self) -> str:
        """
        The database from which to return the schemas from.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="materializedViews")
    def materialized_views(self) -> Sequence['outputs.GetMaterializedViewsMaterializedViewResult']:
        """
        The views in the schema
        """
        return pulumi.get(self, "materialized_views")

    @property
    @pulumi.getter
    def schema(self) -> str:
        """
        The schema from which to return the views from.
        """
        return pulumi.get(self, "schema")


class AwaitableGetMaterializedViewsResult(GetMaterializedViewsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMaterializedViewsResult(
            database=self.database,
            id=self.id,
            materialized_views=self.materialized_views,
            schema=self.schema)


def get_materialized_views(database: Optional[str] = None,
                           schema: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMaterializedViewsResult:
    """
    !> **Caution: Preview Feature** This feature is considered a preview feature in the provider, regardless of the state of the resource in Snowflake. We do not guarantee its stability. It will be reworked and marked as a stable feature in future releases. Breaking changes are expected, even without bumping the major version. To use this feature, add the relevant feature name to `preview_features_enabled field` in the provider configuration. Please always refer to the Getting Help section in our Github repo to best determine how to get help for your questions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_materialized_views(database="MYDB",
        schema="MYSCHEMA")
    ```


    :param str database: The database from which to return the schemas from.
    :param str schema: The schema from which to return the views from.
    """
    __args__ = dict()
    __args__['database'] = database
    __args__['schema'] = schema
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getMaterializedViews:getMaterializedViews', __args__, opts=opts, typ=GetMaterializedViewsResult).value

    return AwaitableGetMaterializedViewsResult(
        database=pulumi.get(__ret__, 'database'),
        id=pulumi.get(__ret__, 'id'),
        materialized_views=pulumi.get(__ret__, 'materialized_views'),
        schema=pulumi.get(__ret__, 'schema'))
def get_materialized_views_output(database: Optional[pulumi.Input[str]] = None,
                                  schema: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetMaterializedViewsResult]:
    """
    !> **Caution: Preview Feature** This feature is considered a preview feature in the provider, regardless of the state of the resource in Snowflake. We do not guarantee its stability. It will be reworked and marked as a stable feature in future releases. Breaking changes are expected, even without bumping the major version. To use this feature, add the relevant feature name to `preview_features_enabled field` in the provider configuration. Please always refer to the Getting Help section in our Github repo to best determine how to get help for your questions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_materialized_views(database="MYDB",
        schema="MYSCHEMA")
    ```


    :param str database: The database from which to return the schemas from.
    :param str schema: The schema from which to return the views from.
    """
    __args__ = dict()
    __args__['database'] = database
    __args__['schema'] = schema
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('snowflake:index/getMaterializedViews:getMaterializedViews', __args__, opts=opts, typ=GetMaterializedViewsResult)
    return __ret__.apply(lambda __response__: GetMaterializedViewsResult(
        database=pulumi.get(__response__, 'database'),
        id=pulumi.get(__response__, 'id'),
        materialized_views=pulumi.get(__response__, 'materialized_views'),
        schema=pulumi.get(__response__, 'schema')))
