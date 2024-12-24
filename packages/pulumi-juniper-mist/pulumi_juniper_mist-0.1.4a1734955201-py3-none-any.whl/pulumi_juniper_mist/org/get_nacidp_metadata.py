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
from .. import _utilities

__all__ = [
    'GetNacidpMetadataResult',
    'AwaitableGetNacidpMetadataResult',
    'get_nacidp_metadata',
    'get_nacidp_metadata_output',
]

@pulumi.output_type
class GetNacidpMetadataResult:
    """
    A collection of values returned by getNacidpMetadata.
    """
    def __init__(__self__, acs_url=None, entity_id=None, id=None, logout_url=None, metadata=None, nacidp_id=None, org_id=None):
        if acs_url and not isinstance(acs_url, str):
            raise TypeError("Expected argument 'acs_url' to be a str")
        pulumi.set(__self__, "acs_url", acs_url)
        if entity_id and not isinstance(entity_id, str):
            raise TypeError("Expected argument 'entity_id' to be a str")
        pulumi.set(__self__, "entity_id", entity_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if logout_url and not isinstance(logout_url, str):
            raise TypeError("Expected argument 'logout_url' to be a str")
        pulumi.set(__self__, "logout_url", logout_url)
        if metadata and not isinstance(metadata, str):
            raise TypeError("Expected argument 'metadata' to be a str")
        pulumi.set(__self__, "metadata", metadata)
        if nacidp_id and not isinstance(nacidp_id, str):
            raise TypeError("Expected argument 'nacidp_id' to be a str")
        pulumi.set(__self__, "nacidp_id", nacidp_id)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)

    @property
    @pulumi.getter(name="acsUrl")
    def acs_url(self) -> str:
        return pulumi.get(self, "acs_url")

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> str:
        return pulumi.get(self, "entity_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="logoutUrl")
    def logout_url(self) -> str:
        return pulumi.get(self, "logout_url")

    @property
    @pulumi.getter
    def metadata(self) -> str:
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter(name="nacidpId")
    def nacidp_id(self) -> str:
        return pulumi.get(self, "nacidp_id")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> str:
        return pulumi.get(self, "org_id")


class AwaitableGetNacidpMetadataResult(GetNacidpMetadataResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNacidpMetadataResult(
            acs_url=self.acs_url,
            entity_id=self.entity_id,
            id=self.id,
            logout_url=self.logout_url,
            metadata=self.metadata,
            nacidp_id=self.nacidp_id,
            org_id=self.org_id)


def get_nacidp_metadata(nacidp_id: Optional[str] = None,
                        org_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNacidpMetadataResult:
    """
    This data source provides the NAC IDP Metadata information.
    The provided information (`entity_id`, `acs_url`, `logout_url` and `metadata`) are the informationrequired to configure the IDP

    ## Example Usage

    ```python
    import pulumi
    import pulumi_junipermist as junipermist

    saml_idp = junipermist.org.get_nacidp_metadata(org_id=terraform_test["id"],
        nacidp_id=saml_idp_one["id"])
    ```
    """
    __args__ = dict()
    __args__['nacidpId'] = nacidp_id
    __args__['orgId'] = org_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('junipermist:org/getNacidpMetadata:getNacidpMetadata', __args__, opts=opts, typ=GetNacidpMetadataResult).value

    return AwaitableGetNacidpMetadataResult(
        acs_url=pulumi.get(__ret__, 'acs_url'),
        entity_id=pulumi.get(__ret__, 'entity_id'),
        id=pulumi.get(__ret__, 'id'),
        logout_url=pulumi.get(__ret__, 'logout_url'),
        metadata=pulumi.get(__ret__, 'metadata'),
        nacidp_id=pulumi.get(__ret__, 'nacidp_id'),
        org_id=pulumi.get(__ret__, 'org_id'))
def get_nacidp_metadata_output(nacidp_id: Optional[pulumi.Input[str]] = None,
                               org_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetNacidpMetadataResult]:
    """
    This data source provides the NAC IDP Metadata information.
    The provided information (`entity_id`, `acs_url`, `logout_url` and `metadata`) are the informationrequired to configure the IDP

    ## Example Usage

    ```python
    import pulumi
    import pulumi_junipermist as junipermist

    saml_idp = junipermist.org.get_nacidp_metadata(org_id=terraform_test["id"],
        nacidp_id=saml_idp_one["id"])
    ```
    """
    __args__ = dict()
    __args__['nacidpId'] = nacidp_id
    __args__['orgId'] = org_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('junipermist:org/getNacidpMetadata:getNacidpMetadata', __args__, opts=opts, typ=GetNacidpMetadataResult)
    return __ret__.apply(lambda __response__: GetNacidpMetadataResult(
        acs_url=pulumi.get(__response__, 'acs_url'),
        entity_id=pulumi.get(__response__, 'entity_id'),
        id=pulumi.get(__response__, 'id'),
        logout_url=pulumi.get(__response__, 'logout_url'),
        metadata=pulumi.get(__response__, 'metadata'),
        nacidp_id=pulumi.get(__response__, 'nacidp_id'),
        org_id=pulumi.get(__response__, 'org_id')))
