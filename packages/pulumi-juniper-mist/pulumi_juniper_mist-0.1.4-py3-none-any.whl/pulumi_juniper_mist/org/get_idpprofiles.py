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
from . import outputs

__all__ = [
    'GetIdpprofilesResult',
    'AwaitableGetIdpprofilesResult',
    'get_idpprofiles',
    'get_idpprofiles_output',
]

@pulumi.output_type
class GetIdpprofilesResult:
    """
    A collection of values returned by getIdpprofiles.
    """
    def __init__(__self__, id=None, org_id=None, org_idpprofiles=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if org_idpprofiles and not isinstance(org_idpprofiles, list):
            raise TypeError("Expected argument 'org_idpprofiles' to be a list")
        pulumi.set(__self__, "org_idpprofiles", org_idpprofiles)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> str:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="orgIdpprofiles")
    def org_idpprofiles(self) -> Sequence['outputs.GetIdpprofilesOrgIdpprofileResult']:
        return pulumi.get(self, "org_idpprofiles")


class AwaitableGetIdpprofilesResult(GetIdpprofilesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIdpprofilesResult(
            id=self.id,
            org_id=self.org_id,
            org_idpprofiles=self.org_idpprofiles)


def get_idpprofiles(org_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIdpprofilesResult:
    """
    This data source provides the list of WAN Assurance IDP Profiles.
    An IDP Profile is a configuration setting that defines the behavior and actions of an intrusion detection and prevention (IDP) system.It specifies how the idp system should detect and respond to potential security threats or attacks on a network.The profile includes rules and policies that determine which types of traffic or attacks should be monitored,what actions should be taken when a threat is detected, and any exceptions or exclusions for specific destinations or attack types.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_junipermist as junipermist

    idpprofiles = junipermist.org.get_idpprofiles(org_id="15fca2ac-b1a6-47cc-9953-cc6906281550")
    ```
    """
    __args__ = dict()
    __args__['orgId'] = org_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('junipermist:org/getIdpprofiles:getIdpprofiles', __args__, opts=opts, typ=GetIdpprofilesResult).value

    return AwaitableGetIdpprofilesResult(
        id=pulumi.get(__ret__, 'id'),
        org_id=pulumi.get(__ret__, 'org_id'),
        org_idpprofiles=pulumi.get(__ret__, 'org_idpprofiles'))
def get_idpprofiles_output(org_id: Optional[pulumi.Input[str]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetIdpprofilesResult]:
    """
    This data source provides the list of WAN Assurance IDP Profiles.
    An IDP Profile is a configuration setting that defines the behavior and actions of an intrusion detection and prevention (IDP) system.It specifies how the idp system should detect and respond to potential security threats or attacks on a network.The profile includes rules and policies that determine which types of traffic or attacks should be monitored,what actions should be taken when a threat is detected, and any exceptions or exclusions for specific destinations or attack types.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_junipermist as junipermist

    idpprofiles = junipermist.org.get_idpprofiles(org_id="15fca2ac-b1a6-47cc-9953-cc6906281550")
    ```
    """
    __args__ = dict()
    __args__['orgId'] = org_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('junipermist:org/getIdpprofiles:getIdpprofiles', __args__, opts=opts, typ=GetIdpprofilesResult)
    return __ret__.apply(lambda __response__: GetIdpprofilesResult(
        id=pulumi.get(__response__, 'id'),
        org_id=pulumi.get(__response__, 'org_id'),
        org_idpprofiles=pulumi.get(__response__, 'org_idpprofiles')))
