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

__all__ = ['WxruleArgs', 'Wxrule']

@pulumi.input_type
class WxruleArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 order: pulumi.Input[int],
                 site_id: pulumi.Input[str],
                 apply_tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 blocked_apps: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_allow_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_deny_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 src_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Wxrule resource.
        :param pulumi.Input[str] action: type of action, allow / block. enum: `allow`, `block`
        :param pulumi.Input[int] order: the order how rules would be looked up, > 0 and bigger order got matched first, -1 means LAST, uniqueness not checked
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_apps: blocked apps (always blocking, ignoring action), the key of Get Application List
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_allow_wxtags: List of WxTag UUID to indicate these tags are allowed access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_deny_wxtags: List of WxTag UUID to indicate these tags are blocked access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_wxtags: List of WxTag UUID
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_wxtags: List of WxTag UUID to determine if this rule would match
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "order", order)
        pulumi.set(__self__, "site_id", site_id)
        if apply_tags is not None:
            pulumi.set(__self__, "apply_tags", apply_tags)
        if blocked_apps is not None:
            pulumi.set(__self__, "blocked_apps", blocked_apps)
        if dst_allow_wxtags is not None:
            pulumi.set(__self__, "dst_allow_wxtags", dst_allow_wxtags)
        if dst_deny_wxtags is not None:
            pulumi.set(__self__, "dst_deny_wxtags", dst_deny_wxtags)
        if dst_wxtags is not None:
            pulumi.set(__self__, "dst_wxtags", dst_wxtags)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if src_wxtags is not None:
            pulumi.set(__self__, "src_wxtags", src_wxtags)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        type of action, allow / block. enum: `allow`, `block`
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def order(self) -> pulumi.Input[int]:
        """
        the order how rules would be looked up, > 0 and bigger order got matched first, -1 means LAST, uniqueness not checked
        """
        return pulumi.get(self, "order")

    @order.setter
    def order(self, value: pulumi.Input[int]):
        pulumi.set(self, "order", value)

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "site_id")

    @site_id.setter
    def site_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "site_id", value)

    @property
    @pulumi.getter(name="applyTags")
    def apply_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "apply_tags")

    @apply_tags.setter
    def apply_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "apply_tags", value)

    @property
    @pulumi.getter(name="blockedApps")
    def blocked_apps(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        blocked apps (always blocking, ignoring action), the key of Get Application List
        """
        return pulumi.get(self, "blocked_apps")

    @blocked_apps.setter
    def blocked_apps(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "blocked_apps", value)

    @property
    @pulumi.getter(name="dstAllowWxtags")
    def dst_allow_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID to indicate these tags are allowed access
        """
        return pulumi.get(self, "dst_allow_wxtags")

    @dst_allow_wxtags.setter
    def dst_allow_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dst_allow_wxtags", value)

    @property
    @pulumi.getter(name="dstDenyWxtags")
    def dst_deny_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID to indicate these tags are blocked access
        """
        return pulumi.get(self, "dst_deny_wxtags")

    @dst_deny_wxtags.setter
    def dst_deny_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dst_deny_wxtags", value)

    @property
    @pulumi.getter(name="dstWxtags")
    def dst_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID
        """
        return pulumi.get(self, "dst_wxtags")

    @dst_wxtags.setter
    def dst_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dst_wxtags", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="srcWxtags")
    def src_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID to determine if this rule would match
        """
        return pulumi.get(self, "src_wxtags")

    @src_wxtags.setter
    def src_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "src_wxtags", value)


@pulumi.input_type
class _WxruleState:
    def __init__(__self__, *,
                 action: Optional[pulumi.Input[str]] = None,
                 apply_tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 blocked_apps: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_allow_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_deny_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 order: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 src_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Wxrule resources.
        :param pulumi.Input[str] action: type of action, allow / block. enum: `allow`, `block`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_apps: blocked apps (always blocking, ignoring action), the key of Get Application List
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_allow_wxtags: List of WxTag UUID to indicate these tags are allowed access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_deny_wxtags: List of WxTag UUID to indicate these tags are blocked access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_wxtags: List of WxTag UUID
        :param pulumi.Input[int] order: the order how rules would be looked up, > 0 and bigger order got matched first, -1 means LAST, uniqueness not checked
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_wxtags: List of WxTag UUID to determine if this rule would match
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if apply_tags is not None:
            pulumi.set(__self__, "apply_tags", apply_tags)
        if blocked_apps is not None:
            pulumi.set(__self__, "blocked_apps", blocked_apps)
        if dst_allow_wxtags is not None:
            pulumi.set(__self__, "dst_allow_wxtags", dst_allow_wxtags)
        if dst_deny_wxtags is not None:
            pulumi.set(__self__, "dst_deny_wxtags", dst_deny_wxtags)
        if dst_wxtags is not None:
            pulumi.set(__self__, "dst_wxtags", dst_wxtags)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if order is not None:
            pulumi.set(__self__, "order", order)
        if site_id is not None:
            pulumi.set(__self__, "site_id", site_id)
        if src_wxtags is not None:
            pulumi.set(__self__, "src_wxtags", src_wxtags)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[str]]:
        """
        type of action, allow / block. enum: `allow`, `block`
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="applyTags")
    def apply_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "apply_tags")

    @apply_tags.setter
    def apply_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "apply_tags", value)

    @property
    @pulumi.getter(name="blockedApps")
    def blocked_apps(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        blocked apps (always blocking, ignoring action), the key of Get Application List
        """
        return pulumi.get(self, "blocked_apps")

    @blocked_apps.setter
    def blocked_apps(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "blocked_apps", value)

    @property
    @pulumi.getter(name="dstAllowWxtags")
    def dst_allow_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID to indicate these tags are allowed access
        """
        return pulumi.get(self, "dst_allow_wxtags")

    @dst_allow_wxtags.setter
    def dst_allow_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dst_allow_wxtags", value)

    @property
    @pulumi.getter(name="dstDenyWxtags")
    def dst_deny_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID to indicate these tags are blocked access
        """
        return pulumi.get(self, "dst_deny_wxtags")

    @dst_deny_wxtags.setter
    def dst_deny_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dst_deny_wxtags", value)

    @property
    @pulumi.getter(name="dstWxtags")
    def dst_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID
        """
        return pulumi.get(self, "dst_wxtags")

    @dst_wxtags.setter
    def dst_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dst_wxtags", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def order(self) -> Optional[pulumi.Input[int]]:
        """
        the order how rules would be looked up, > 0 and bigger order got matched first, -1 means LAST, uniqueness not checked
        """
        return pulumi.get(self, "order")

    @order.setter
    def order(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "order", value)

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "site_id")

    @site_id.setter
    def site_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "site_id", value)

    @property
    @pulumi.getter(name="srcWxtags")
    def src_wxtags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of WxTag UUID to determine if this rule would match
        """
        return pulumi.get(self, "src_wxtags")

    @src_wxtags.setter
    def src_wxtags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "src_wxtags", value)


class Wxrule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 apply_tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 blocked_apps: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_allow_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_deny_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 order: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 src_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        This resource manages the Site WxRules (WLAN policies).
        A WxLAN policy is a set of rules and settings that can be applied to devices in a network to determine how they are treated. it provides support for access policies, network segmentation, role-based policies, micro-segmentation, and least privilege. WxLAN policies are used to allow or deny specific users from accessing specific resources in a wireless network.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_juniper_mist as junipermist

        wxrule_one = junipermist.site.Wxrule("wxrule_one",
            site_id=terraform_test["id"],
            src_wxtags=[wxtag_one["id"]],
            enabled=True,
            action="allow",
            dst_deny_wxtags=[wxtag_two["id"]],
            order=1)
        ```

        ## Import

        Using `pulumi import`, import `mist_site_wxrule` with:

        Site WxRule can be imported by specifying the site_id and the wxrule_id

        ```sh
        $ pulumi import junipermist:site/wxrule:Wxrule wxrule_one 17b46405-3a6d-4715-8bb4-6bb6d06f316a.d3c42998-9012-4859-9743-6b9bee475309
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: type of action, allow / block. enum: `allow`, `block`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_apps: blocked apps (always blocking, ignoring action), the key of Get Application List
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_allow_wxtags: List of WxTag UUID to indicate these tags are allowed access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_deny_wxtags: List of WxTag UUID to indicate these tags are blocked access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_wxtags: List of WxTag UUID
        :param pulumi.Input[int] order: the order how rules would be looked up, > 0 and bigger order got matched first, -1 means LAST, uniqueness not checked
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_wxtags: List of WxTag UUID to determine if this rule would match
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WxruleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource manages the Site WxRules (WLAN policies).
        A WxLAN policy is a set of rules and settings that can be applied to devices in a network to determine how they are treated. it provides support for access policies, network segmentation, role-based policies, micro-segmentation, and least privilege. WxLAN policies are used to allow or deny specific users from accessing specific resources in a wireless network.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_juniper_mist as junipermist

        wxrule_one = junipermist.site.Wxrule("wxrule_one",
            site_id=terraform_test["id"],
            src_wxtags=[wxtag_one["id"]],
            enabled=True,
            action="allow",
            dst_deny_wxtags=[wxtag_two["id"]],
            order=1)
        ```

        ## Import

        Using `pulumi import`, import `mist_site_wxrule` with:

        Site WxRule can be imported by specifying the site_id and the wxrule_id

        ```sh
        $ pulumi import junipermist:site/wxrule:Wxrule wxrule_one 17b46405-3a6d-4715-8bb4-6bb6d06f316a.d3c42998-9012-4859-9743-6b9bee475309
        ```

        :param str resource_name: The name of the resource.
        :param WxruleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WxruleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 apply_tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 blocked_apps: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_allow_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_deny_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dst_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 order: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 src_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WxruleArgs.__new__(WxruleArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["apply_tags"] = apply_tags
            __props__.__dict__["blocked_apps"] = blocked_apps
            __props__.__dict__["dst_allow_wxtags"] = dst_allow_wxtags
            __props__.__dict__["dst_deny_wxtags"] = dst_deny_wxtags
            __props__.__dict__["dst_wxtags"] = dst_wxtags
            __props__.__dict__["enabled"] = enabled
            if order is None and not opts.urn:
                raise TypeError("Missing required property 'order'")
            __props__.__dict__["order"] = order
            if site_id is None and not opts.urn:
                raise TypeError("Missing required property 'site_id'")
            __props__.__dict__["site_id"] = site_id
            __props__.__dict__["src_wxtags"] = src_wxtags
        super(Wxrule, __self__).__init__(
            'junipermist:site/wxrule:Wxrule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[str]] = None,
            apply_tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            blocked_apps: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            dst_allow_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            dst_deny_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            dst_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            order: Optional[pulumi.Input[int]] = None,
            site_id: Optional[pulumi.Input[str]] = None,
            src_wxtags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Wxrule':
        """
        Get an existing Wxrule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: type of action, allow / block. enum: `allow`, `block`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_apps: blocked apps (always blocking, ignoring action), the key of Get Application List
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_allow_wxtags: List of WxTag UUID to indicate these tags are allowed access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_deny_wxtags: List of WxTag UUID to indicate these tags are blocked access
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dst_wxtags: List of WxTag UUID
        :param pulumi.Input[int] order: the order how rules would be looked up, > 0 and bigger order got matched first, -1 means LAST, uniqueness not checked
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_wxtags: List of WxTag UUID to determine if this rule would match
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _WxruleState.__new__(_WxruleState)

        __props__.__dict__["action"] = action
        __props__.__dict__["apply_tags"] = apply_tags
        __props__.__dict__["blocked_apps"] = blocked_apps
        __props__.__dict__["dst_allow_wxtags"] = dst_allow_wxtags
        __props__.__dict__["dst_deny_wxtags"] = dst_deny_wxtags
        __props__.__dict__["dst_wxtags"] = dst_wxtags
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["order"] = order
        __props__.__dict__["site_id"] = site_id
        __props__.__dict__["src_wxtags"] = src_wxtags
        return Wxrule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        type of action, allow / block. enum: `allow`, `block`
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="applyTags")
    def apply_tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "apply_tags")

    @property
    @pulumi.getter(name="blockedApps")
    def blocked_apps(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        blocked apps (always blocking, ignoring action), the key of Get Application List
        """
        return pulumi.get(self, "blocked_apps")

    @property
    @pulumi.getter(name="dstAllowWxtags")
    def dst_allow_wxtags(self) -> pulumi.Output[Sequence[str]]:
        """
        List of WxTag UUID to indicate these tags are allowed access
        """
        return pulumi.get(self, "dst_allow_wxtags")

    @property
    @pulumi.getter(name="dstDenyWxtags")
    def dst_deny_wxtags(self) -> pulumi.Output[Sequence[str]]:
        """
        List of WxTag UUID to indicate these tags are blocked access
        """
        return pulumi.get(self, "dst_deny_wxtags")

    @property
    @pulumi.getter(name="dstWxtags")
    def dst_wxtags(self) -> pulumi.Output[Sequence[str]]:
        """
        List of WxTag UUID
        """
        return pulumi.get(self, "dst_wxtags")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def order(self) -> pulumi.Output[int]:
        """
        the order how rules would be looked up, > 0 and bigger order got matched first, -1 means LAST, uniqueness not checked
        """
        return pulumi.get(self, "order")

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "site_id")

    @property
    @pulumi.getter(name="srcWxtags")
    def src_wxtags(self) -> pulumi.Output[Sequence[str]]:
        """
        List of WxTag UUID to determine if this rule would match
        """
        return pulumi.get(self, "src_wxtags")

