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

__all__ = ['PskArgs', 'Psk']

@pulumi.input_type
class PskArgs:
    def __init__(__self__, *,
                 passphrase: pulumi.Input[str],
                 site_id: pulumi.Input[str],
                 ssid: pulumi.Input[str],
                 email: Optional[pulumi.Input[str]] = None,
                 expire_time: Optional[pulumi.Input[int]] = None,
                 expiry_notification_time: Optional[pulumi.Input[int]] = None,
                 mac: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 notify_expiry: Optional[pulumi.Input[bool]] = None,
                 notify_on_create_or_edit: Optional[pulumi.Input[bool]] = None,
                 old_passphrase: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None,
                 vlan_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Psk resource.
        :param pulumi.Input[str] passphrase: passphrase of the PSK (8-63 character or 64 in hex)
        :param pulumi.Input[str] ssid: SSID this PSK should be applicable to
        :param pulumi.Input[str] email: email to send psk expiring notifications to
        :param pulumi.Input[int] expire_time: Expire time for this PSK key (epoch time in seconds). Default `null` (as no expiration)
        :param pulumi.Input[int] expiry_notification_time: Number of days before psk is expired. Used as to when to start sending reminder notification when the psk is about to expire
        :param pulumi.Input[str] mac: if `usage`==`single`, the mac that this PSK ties to, empty if `auto-binding`
        :param pulumi.Input[bool] notify_expiry: If set to true, reminder notification will be sent when psk is about to expire
        :param pulumi.Input[bool] notify_on_create_or_edit: If set to true, notification will be sent when psk is created or edited
        :param pulumi.Input[str] old_passphrase: previous passphrase of the PSK if it has been rotated
        :param pulumi.Input[str] usage: enum: `multi`, `single`
        """
        pulumi.set(__self__, "passphrase", passphrase)
        pulumi.set(__self__, "site_id", site_id)
        pulumi.set(__self__, "ssid", ssid)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if expire_time is not None:
            pulumi.set(__self__, "expire_time", expire_time)
        if expiry_notification_time is not None:
            pulumi.set(__self__, "expiry_notification_time", expiry_notification_time)
        if mac is not None:
            pulumi.set(__self__, "mac", mac)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if note is not None:
            pulumi.set(__self__, "note", note)
        if notify_expiry is not None:
            pulumi.set(__self__, "notify_expiry", notify_expiry)
        if notify_on_create_or_edit is not None:
            pulumi.set(__self__, "notify_on_create_or_edit", notify_on_create_or_edit)
        if old_passphrase is not None:
            pulumi.set(__self__, "old_passphrase", old_passphrase)
        if role is not None:
            pulumi.set(__self__, "role", role)
        if usage is not None:
            pulumi.set(__self__, "usage", usage)
        if vlan_id is not None:
            pulumi.set(__self__, "vlan_id", vlan_id)

    @property
    @pulumi.getter
    def passphrase(self) -> pulumi.Input[str]:
        """
        passphrase of the PSK (8-63 character or 64 in hex)
        """
        return pulumi.get(self, "passphrase")

    @passphrase.setter
    def passphrase(self, value: pulumi.Input[str]):
        pulumi.set(self, "passphrase", value)

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "site_id")

    @site_id.setter
    def site_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "site_id", value)

    @property
    @pulumi.getter
    def ssid(self) -> pulumi.Input[str]:
        """
        SSID this PSK should be applicable to
        """
        return pulumi.get(self, "ssid")

    @ssid.setter
    def ssid(self, value: pulumi.Input[str]):
        pulumi.set(self, "ssid", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        email to send psk expiring notifications to
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[pulumi.Input[int]]:
        """
        Expire time for this PSK key (epoch time in seconds). Default `null` (as no expiration)
        """
        return pulumi.get(self, "expire_time")

    @expire_time.setter
    def expire_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expire_time", value)

    @property
    @pulumi.getter(name="expiryNotificationTime")
    def expiry_notification_time(self) -> Optional[pulumi.Input[int]]:
        """
        Number of days before psk is expired. Used as to when to start sending reminder notification when the psk is about to expire
        """
        return pulumi.get(self, "expiry_notification_time")

    @expiry_notification_time.setter
    def expiry_notification_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expiry_notification_time", value)

    @property
    @pulumi.getter
    def mac(self) -> Optional[pulumi.Input[str]]:
        """
        if `usage`==`single`, the mac that this PSK ties to, empty if `auto-binding`
        """
        return pulumi.get(self, "mac")

    @mac.setter
    def mac(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mac", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def note(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "note")

    @note.setter
    def note(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "note", value)

    @property
    @pulumi.getter(name="notifyExpiry")
    def notify_expiry(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, reminder notification will be sent when psk is about to expire
        """
        return pulumi.get(self, "notify_expiry")

    @notify_expiry.setter
    def notify_expiry(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "notify_expiry", value)

    @property
    @pulumi.getter(name="notifyOnCreateOrEdit")
    def notify_on_create_or_edit(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, notification will be sent when psk is created or edited
        """
        return pulumi.get(self, "notify_on_create_or_edit")

    @notify_on_create_or_edit.setter
    def notify_on_create_or_edit(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "notify_on_create_or_edit", value)

    @property
    @pulumi.getter(name="oldPassphrase")
    def old_passphrase(self) -> Optional[pulumi.Input[str]]:
        """
        previous passphrase of the PSK if it has been rotated
        """
        return pulumi.get(self, "old_passphrase")

    @old_passphrase.setter
    def old_passphrase(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "old_passphrase", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def usage(self) -> Optional[pulumi.Input[str]]:
        """
        enum: `multi`, `single`
        """
        return pulumi.get(self, "usage")

    @usage.setter
    def usage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage", value)

    @property
    @pulumi.getter(name="vlanId")
    def vlan_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "vlan_id")

    @vlan_id.setter
    def vlan_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vlan_id", value)


@pulumi.input_type
class _PskState:
    def __init__(__self__, *,
                 email: Optional[pulumi.Input[str]] = None,
                 expire_time: Optional[pulumi.Input[int]] = None,
                 expiry_notification_time: Optional[pulumi.Input[int]] = None,
                 mac: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 notify_expiry: Optional[pulumi.Input[bool]] = None,
                 notify_on_create_or_edit: Optional[pulumi.Input[bool]] = None,
                 old_passphrase: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 passphrase: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 ssid: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None,
                 vlan_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Psk resources.
        :param pulumi.Input[str] email: email to send psk expiring notifications to
        :param pulumi.Input[int] expire_time: Expire time for this PSK key (epoch time in seconds). Default `null` (as no expiration)
        :param pulumi.Input[int] expiry_notification_time: Number of days before psk is expired. Used as to when to start sending reminder notification when the psk is about to expire
        :param pulumi.Input[str] mac: if `usage`==`single`, the mac that this PSK ties to, empty if `auto-binding`
        :param pulumi.Input[bool] notify_expiry: If set to true, reminder notification will be sent when psk is about to expire
        :param pulumi.Input[bool] notify_on_create_or_edit: If set to true, notification will be sent when psk is created or edited
        :param pulumi.Input[str] old_passphrase: previous passphrase of the PSK if it has been rotated
        :param pulumi.Input[str] passphrase: passphrase of the PSK (8-63 character or 64 in hex)
        :param pulumi.Input[str] ssid: SSID this PSK should be applicable to
        :param pulumi.Input[str] usage: enum: `multi`, `single`
        """
        if email is not None:
            pulumi.set(__self__, "email", email)
        if expire_time is not None:
            pulumi.set(__self__, "expire_time", expire_time)
        if expiry_notification_time is not None:
            pulumi.set(__self__, "expiry_notification_time", expiry_notification_time)
        if mac is not None:
            pulumi.set(__self__, "mac", mac)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if note is not None:
            pulumi.set(__self__, "note", note)
        if notify_expiry is not None:
            pulumi.set(__self__, "notify_expiry", notify_expiry)
        if notify_on_create_or_edit is not None:
            pulumi.set(__self__, "notify_on_create_or_edit", notify_on_create_or_edit)
        if old_passphrase is not None:
            pulumi.set(__self__, "old_passphrase", old_passphrase)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if passphrase is not None:
            pulumi.set(__self__, "passphrase", passphrase)
        if role is not None:
            pulumi.set(__self__, "role", role)
        if site_id is not None:
            pulumi.set(__self__, "site_id", site_id)
        if ssid is not None:
            pulumi.set(__self__, "ssid", ssid)
        if usage is not None:
            pulumi.set(__self__, "usage", usage)
        if vlan_id is not None:
            pulumi.set(__self__, "vlan_id", vlan_id)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        email to send psk expiring notifications to
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[pulumi.Input[int]]:
        """
        Expire time for this PSK key (epoch time in seconds). Default `null` (as no expiration)
        """
        return pulumi.get(self, "expire_time")

    @expire_time.setter
    def expire_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expire_time", value)

    @property
    @pulumi.getter(name="expiryNotificationTime")
    def expiry_notification_time(self) -> Optional[pulumi.Input[int]]:
        """
        Number of days before psk is expired. Used as to when to start sending reminder notification when the psk is about to expire
        """
        return pulumi.get(self, "expiry_notification_time")

    @expiry_notification_time.setter
    def expiry_notification_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expiry_notification_time", value)

    @property
    @pulumi.getter
    def mac(self) -> Optional[pulumi.Input[str]]:
        """
        if `usage`==`single`, the mac that this PSK ties to, empty if `auto-binding`
        """
        return pulumi.get(self, "mac")

    @mac.setter
    def mac(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mac", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def note(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "note")

    @note.setter
    def note(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "note", value)

    @property
    @pulumi.getter(name="notifyExpiry")
    def notify_expiry(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, reminder notification will be sent when psk is about to expire
        """
        return pulumi.get(self, "notify_expiry")

    @notify_expiry.setter
    def notify_expiry(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "notify_expiry", value)

    @property
    @pulumi.getter(name="notifyOnCreateOrEdit")
    def notify_on_create_or_edit(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, notification will be sent when psk is created or edited
        """
        return pulumi.get(self, "notify_on_create_or_edit")

    @notify_on_create_or_edit.setter
    def notify_on_create_or_edit(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "notify_on_create_or_edit", value)

    @property
    @pulumi.getter(name="oldPassphrase")
    def old_passphrase(self) -> Optional[pulumi.Input[str]]:
        """
        previous passphrase of the PSK if it has been rotated
        """
        return pulumi.get(self, "old_passphrase")

    @old_passphrase.setter
    def old_passphrase(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "old_passphrase", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def passphrase(self) -> Optional[pulumi.Input[str]]:
        """
        passphrase of the PSK (8-63 character or 64 in hex)
        """
        return pulumi.get(self, "passphrase")

    @passphrase.setter
    def passphrase(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "passphrase", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "site_id")

    @site_id.setter
    def site_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "site_id", value)

    @property
    @pulumi.getter
    def ssid(self) -> Optional[pulumi.Input[str]]:
        """
        SSID this PSK should be applicable to
        """
        return pulumi.get(self, "ssid")

    @ssid.setter
    def ssid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ssid", value)

    @property
    @pulumi.getter
    def usage(self) -> Optional[pulumi.Input[str]]:
        """
        enum: `multi`, `single`
        """
        return pulumi.get(self, "usage")

    @usage.setter
    def usage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage", value)

    @property
    @pulumi.getter(name="vlanId")
    def vlan_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "vlan_id")

    @vlan_id.setter
    def vlan_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vlan_id", value)


class Psk(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 expire_time: Optional[pulumi.Input[int]] = None,
                 expiry_notification_time: Optional[pulumi.Input[int]] = None,
                 mac: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 notify_expiry: Optional[pulumi.Input[bool]] = None,
                 notify_on_create_or_edit: Optional[pulumi.Input[bool]] = None,
                 old_passphrase: Optional[pulumi.Input[str]] = None,
                 passphrase: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 ssid: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None,
                 vlan_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This data source provides the list of Site PSKs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_juniper_mist as junipermist

        psk_one = junipermist.site.Psk("psk_one",
            site_id=terraform_site["id"],
            name="JNP-FR-PAR",
            passphrase="secretone",
            ssid=wlan_one["ssid"],
            usage="multi")
        ```

        ## Import

        Using `pulumi import`, import `mist_site_psk` with:

        Site PSK can be imported by specifying the site_id and the psk_id

        ```sh
        $ pulumi import junipermist:site/psk:Psk psk_one 17b46405-3a6d-4715-8bb4-6bb6d06f316a.d3c42998-9012-4859-9743-6b9bee475309
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] email: email to send psk expiring notifications to
        :param pulumi.Input[int] expire_time: Expire time for this PSK key (epoch time in seconds). Default `null` (as no expiration)
        :param pulumi.Input[int] expiry_notification_time: Number of days before psk is expired. Used as to when to start sending reminder notification when the psk is about to expire
        :param pulumi.Input[str] mac: if `usage`==`single`, the mac that this PSK ties to, empty if `auto-binding`
        :param pulumi.Input[bool] notify_expiry: If set to true, reminder notification will be sent when psk is about to expire
        :param pulumi.Input[bool] notify_on_create_or_edit: If set to true, notification will be sent when psk is created or edited
        :param pulumi.Input[str] old_passphrase: previous passphrase of the PSK if it has been rotated
        :param pulumi.Input[str] passphrase: passphrase of the PSK (8-63 character or 64 in hex)
        :param pulumi.Input[str] ssid: SSID this PSK should be applicable to
        :param pulumi.Input[str] usage: enum: `multi`, `single`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PskArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This data source provides the list of Site PSKs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_juniper_mist as junipermist

        psk_one = junipermist.site.Psk("psk_one",
            site_id=terraform_site["id"],
            name="JNP-FR-PAR",
            passphrase="secretone",
            ssid=wlan_one["ssid"],
            usage="multi")
        ```

        ## Import

        Using `pulumi import`, import `mist_site_psk` with:

        Site PSK can be imported by specifying the site_id and the psk_id

        ```sh
        $ pulumi import junipermist:site/psk:Psk psk_one 17b46405-3a6d-4715-8bb4-6bb6d06f316a.d3c42998-9012-4859-9743-6b9bee475309
        ```

        :param str resource_name: The name of the resource.
        :param PskArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PskArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 expire_time: Optional[pulumi.Input[int]] = None,
                 expiry_notification_time: Optional[pulumi.Input[int]] = None,
                 mac: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 notify_expiry: Optional[pulumi.Input[bool]] = None,
                 notify_on_create_or_edit: Optional[pulumi.Input[bool]] = None,
                 old_passphrase: Optional[pulumi.Input[str]] = None,
                 passphrase: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 ssid: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None,
                 vlan_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PskArgs.__new__(PskArgs)

            __props__.__dict__["email"] = email
            __props__.__dict__["expire_time"] = expire_time
            __props__.__dict__["expiry_notification_time"] = expiry_notification_time
            __props__.__dict__["mac"] = mac
            __props__.__dict__["name"] = name
            __props__.__dict__["note"] = note
            __props__.__dict__["notify_expiry"] = notify_expiry
            __props__.__dict__["notify_on_create_or_edit"] = notify_on_create_or_edit
            __props__.__dict__["old_passphrase"] = None if old_passphrase is None else pulumi.Output.secret(old_passphrase)
            if passphrase is None and not opts.urn:
                raise TypeError("Missing required property 'passphrase'")
            __props__.__dict__["passphrase"] = None if passphrase is None else pulumi.Output.secret(passphrase)
            __props__.__dict__["role"] = role
            if site_id is None and not opts.urn:
                raise TypeError("Missing required property 'site_id'")
            __props__.__dict__["site_id"] = site_id
            if ssid is None and not opts.urn:
                raise TypeError("Missing required property 'ssid'")
            __props__.__dict__["ssid"] = ssid
            __props__.__dict__["usage"] = usage
            __props__.__dict__["vlan_id"] = vlan_id
            __props__.__dict__["org_id"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["oldPassphrase", "passphrase"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Psk, __self__).__init__(
            'junipermist:site/psk:Psk',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            email: Optional[pulumi.Input[str]] = None,
            expire_time: Optional[pulumi.Input[int]] = None,
            expiry_notification_time: Optional[pulumi.Input[int]] = None,
            mac: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            note: Optional[pulumi.Input[str]] = None,
            notify_expiry: Optional[pulumi.Input[bool]] = None,
            notify_on_create_or_edit: Optional[pulumi.Input[bool]] = None,
            old_passphrase: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            passphrase: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None,
            site_id: Optional[pulumi.Input[str]] = None,
            ssid: Optional[pulumi.Input[str]] = None,
            usage: Optional[pulumi.Input[str]] = None,
            vlan_id: Optional[pulumi.Input[str]] = None) -> 'Psk':
        """
        Get an existing Psk resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] email: email to send psk expiring notifications to
        :param pulumi.Input[int] expire_time: Expire time for this PSK key (epoch time in seconds). Default `null` (as no expiration)
        :param pulumi.Input[int] expiry_notification_time: Number of days before psk is expired. Used as to when to start sending reminder notification when the psk is about to expire
        :param pulumi.Input[str] mac: if `usage`==`single`, the mac that this PSK ties to, empty if `auto-binding`
        :param pulumi.Input[bool] notify_expiry: If set to true, reminder notification will be sent when psk is about to expire
        :param pulumi.Input[bool] notify_on_create_or_edit: If set to true, notification will be sent when psk is created or edited
        :param pulumi.Input[str] old_passphrase: previous passphrase of the PSK if it has been rotated
        :param pulumi.Input[str] passphrase: passphrase of the PSK (8-63 character or 64 in hex)
        :param pulumi.Input[str] ssid: SSID this PSK should be applicable to
        :param pulumi.Input[str] usage: enum: `multi`, `single`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PskState.__new__(_PskState)

        __props__.__dict__["email"] = email
        __props__.__dict__["expire_time"] = expire_time
        __props__.__dict__["expiry_notification_time"] = expiry_notification_time
        __props__.__dict__["mac"] = mac
        __props__.__dict__["name"] = name
        __props__.__dict__["note"] = note
        __props__.__dict__["notify_expiry"] = notify_expiry
        __props__.__dict__["notify_on_create_or_edit"] = notify_on_create_or_edit
        __props__.__dict__["old_passphrase"] = old_passphrase
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["passphrase"] = passphrase
        __props__.__dict__["role"] = role
        __props__.__dict__["site_id"] = site_id
        __props__.__dict__["ssid"] = ssid
        __props__.__dict__["usage"] = usage
        __props__.__dict__["vlan_id"] = vlan_id
        return Psk(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[Optional[str]]:
        """
        email to send psk expiring notifications to
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> pulumi.Output[int]:
        """
        Expire time for this PSK key (epoch time in seconds). Default `null` (as no expiration)
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter(name="expiryNotificationTime")
    def expiry_notification_time(self) -> pulumi.Output[Optional[int]]:
        """
        Number of days before psk is expired. Used as to when to start sending reminder notification when the psk is about to expire
        """
        return pulumi.get(self, "expiry_notification_time")

    @property
    @pulumi.getter
    def mac(self) -> pulumi.Output[Optional[str]]:
        """
        if `usage`==`single`, the mac that this PSK ties to, empty if `auto-binding`
        """
        return pulumi.get(self, "mac")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def note(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "note")

    @property
    @pulumi.getter(name="notifyExpiry")
    def notify_expiry(self) -> pulumi.Output[bool]:
        """
        If set to true, reminder notification will be sent when psk is about to expire
        """
        return pulumi.get(self, "notify_expiry")

    @property
    @pulumi.getter(name="notifyOnCreateOrEdit")
    def notify_on_create_or_edit(self) -> pulumi.Output[Optional[bool]]:
        """
        If set to true, notification will be sent when psk is created or edited
        """
        return pulumi.get(self, "notify_on_create_or_edit")

    @property
    @pulumi.getter(name="oldPassphrase")
    def old_passphrase(self) -> pulumi.Output[Optional[str]]:
        """
        previous passphrase of the PSK if it has been rotated
        """
        return pulumi.get(self, "old_passphrase")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter
    def passphrase(self) -> pulumi.Output[str]:
        """
        passphrase of the PSK (8-63 character or 64 in hex)
        """
        return pulumi.get(self, "passphrase")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "role")

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "site_id")

    @property
    @pulumi.getter
    def ssid(self) -> pulumi.Output[str]:
        """
        SSID this PSK should be applicable to
        """
        return pulumi.get(self, "ssid")

    @property
    @pulumi.getter
    def usage(self) -> pulumi.Output[str]:
        """
        enum: `multi`, `single`
        """
        return pulumi.get(self, "usage")

    @property
    @pulumi.getter(name="vlanId")
    def vlan_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "vlan_id")

