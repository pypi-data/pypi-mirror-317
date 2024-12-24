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
    'GetNacrulesResult',
    'AwaitableGetNacrulesResult',
    'get_nacrules',
    'get_nacrules_output',
]

@pulumi.output_type
class GetNacrulesResult:
    """
    A collection of values returned by getNacrules.
    """
    def __init__(__self__, id=None, org_id=None, org_nacrules=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if org_nacrules and not isinstance(org_nacrules, list):
            raise TypeError("Expected argument 'org_nacrules' to be a list")
        pulumi.set(__self__, "org_nacrules", org_nacrules)

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
    @pulumi.getter(name="orgNacrules")
    def org_nacrules(self) -> Sequence['outputs.GetNacrulesOrgNacruleResult']:
        return pulumi.get(self, "org_nacrules")


class AwaitableGetNacrulesResult(GetNacrulesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNacrulesResult(
            id=self.id,
            org_id=self.org_id,
            org_nacrules=self.org_nacrules)


def get_nacrules(org_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNacrulesResult:
    """
    This data source provides the list of NAC Rules (Auth Policies).
    A NAC Rule defines a list of critera (NAC Tag) the network client must match to execute the Rule, an action (Allow/Deny)and a list of RADIUS Attributes (NAC Tags) to return

    ## Example Usage

    ```python
    import pulumi
    import pulumi_junipermist as junipermist

    nacrules = junipermist.org.get_nacrules(org_id="15fca2ac-b1a6-47cc-9953-cc6906281550")
    ```
    """
    __args__ = dict()
    __args__['orgId'] = org_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('junipermist:org/getNacrules:getNacrules', __args__, opts=opts, typ=GetNacrulesResult).value

    return AwaitableGetNacrulesResult(
        id=pulumi.get(__ret__, 'id'),
        org_id=pulumi.get(__ret__, 'org_id'),
        org_nacrules=pulumi.get(__ret__, 'org_nacrules'))
def get_nacrules_output(org_id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetNacrulesResult]:
    """
    This data source provides the list of NAC Rules (Auth Policies).
    A NAC Rule defines a list of critera (NAC Tag) the network client must match to execute the Rule, an action (Allow/Deny)and a list of RADIUS Attributes (NAC Tags) to return

    ## Example Usage

    ```python
    import pulumi
    import pulumi_junipermist as junipermist

    nacrules = junipermist.org.get_nacrules(org_id="15fca2ac-b1a6-47cc-9953-cc6906281550")
    ```
    """
    __args__ = dict()
    __args__['orgId'] = org_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('junipermist:org/getNacrules:getNacrules', __args__, opts=opts, typ=GetNacrulesResult)
    return __ret__.apply(lambda __response__: GetNacrulesResult(
        id=pulumi.get(__response__, 'id'),
        org_id=pulumi.get(__response__, 'org_id'),
        org_nacrules=pulumi.get(__response__, 'org_nacrules')))
