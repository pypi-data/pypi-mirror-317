# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***


import asyncio
import functools
import importlib.metadata
import importlib.util
import inspect
import json
import os
import sys
import typing
import warnings
import base64

import pulumi
import pulumi.runtime
from pulumi.runtime.sync_await import _sync_await
from pulumi.runtime.proto import resource_pb2

from semver import VersionInfo as SemverVersion
from parver import Version as PEP440Version

C = typing.TypeVar("C", bound=typing.Callable)


def get_env(*args):
    for v in args:
        value = os.getenv(v)
        if value is not None:
            return value
    return None


def get_env_bool(*args):
    str = get_env(*args)
    if str is not None:
        # NOTE: these values are taken from https://golang.org/src/strconv/atob.go?s=351:391#L1, which is what
        # Terraform uses internally when parsing boolean values.
        if str in ["1", "t", "T", "true", "TRUE", "True"]:
            return True
        if str in ["0", "f", "F", "false", "FALSE", "False"]:
            return False
    return None


def get_env_int(*args):
    str = get_env(*args)
    if str is not None:
        try:
            return int(str)
        except:
            return None
    return None


def get_env_float(*args):
    str = get_env(*args)
    if str is not None:
        try:
            return float(str)
        except:
            return None
    return None


def _get_semver_version():
    # __name__ is set to the fully-qualified name of the current module, In our case, it will be
    # <some module>._utilities. <some module> is the module we want to query the version for.
    root_package, *rest = __name__.split('.')

    # pkg_resources uses setuptools to inspect the set of installed packages. We use it here to ask
    # for the currently installed version of the root package (i.e. us) and get its version.

    # Unfortunately, PEP440 and semver differ slightly in incompatible ways. The Pulumi engine expects
    # to receive a valid semver string when receiving requests from the language host, so it's our
    # responsibility as the library to convert our own PEP440 version into a valid semver string.

    pep440_version_string = importlib.metadata.version(root_package)
    pep440_version = PEP440Version.parse(pep440_version_string)
    (major, minor, patch) = pep440_version.release
    prerelease = None
    if pep440_version.pre_tag == 'a':
        prerelease = f"alpha.{pep440_version.pre}"
    elif pep440_version.pre_tag == 'b':
        prerelease = f"beta.{pep440_version.pre}"
    elif pep440_version.pre_tag == 'rc':
        prerelease = f"rc.{pep440_version.pre}"
    elif pep440_version.dev is not None:
        prerelease = f"dev.{pep440_version.dev}"

    # The only significant difference between PEP440 and semver as it pertains to us is that PEP440 has explicit support
    # for dev builds, while semver encodes them as "prerelease" versions. In order to bridge between the two, we convert
    # our dev build version into a prerelease tag. This matches what all of our other packages do when constructing
    # their own semver string.
    return SemverVersion(major=major, minor=minor, patch=patch, prerelease=prerelease)


# Determine the version once and cache the value, which measurably improves program performance.
_version = _get_semver_version()
_version_str = str(_version)

def get_resource_opts_defaults() -> pulumi.ResourceOptions:
    return pulumi.ResourceOptions(
        version=get_version(),
        plugin_download_url=get_plugin_download_url(),
    )

def get_invoke_opts_defaults() -> pulumi.InvokeOptions:
    return pulumi.InvokeOptions(
        version=get_version(),
        plugin_download_url=get_plugin_download_url(),
    )

def get_resource_args_opts(resource_args_type, resource_options_type, *args, **kwargs):
    """
    Return the resource args and options given the *args and **kwargs of a resource's
    __init__ method.
    """

    resource_args, opts = None, None

    # If the first item is the resource args type, save it and remove it from the args list.
    if args and isinstance(args[0], resource_args_type):
        resource_args, args = args[0], args[1:]

    # Now look at the first item in the args list again.
    # If the first item is the resource options class, save it.
    if args and isinstance(args[0], resource_options_type):
        opts = args[0]

    # If resource_args is None, see if "args" is in kwargs, and, if so, if it's typed as the
    # the resource args type.
    if resource_args is None:
        a = kwargs.get("args")
        if isinstance(a, resource_args_type):
            resource_args = a

    # If opts is None, look it up in kwargs.
    if opts is None:
        opts = kwargs.get("opts")

    return resource_args, opts


# Temporary: just use pulumi._utils.lazy_import once everyone upgrades.
def lazy_import(fullname):

    import pulumi._utils as u
    f = getattr(u, 'lazy_import', None)
    if f is None:
        f = _lazy_import_temp

    return f(fullname)


# Copied from pulumi._utils.lazy_import, see comments there.
def _lazy_import_temp(fullname):
    m = sys.modules.get(fullname, None)
    if m is not None:
        return m

    spec = importlib.util.find_spec(fullname)

    m = sys.modules.get(fullname, None)
    if m is not None:
        return m

    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)

    m = sys.modules.get(fullname, None)
    if m is not None:
        return m

    sys.modules[fullname] = module
    loader.exec_module(module)
    return module


class Package(pulumi.runtime.ResourcePackage):
    def __init__(self, pkg_info):
        super().__init__()
        self.pkg_info = pkg_info

    def version(self):
        return _version

    def construct_provider(self, name: str, typ: str, urn: str) -> pulumi.ProviderResource:
        if typ != self.pkg_info['token']:
            raise Exception(f"unknown provider type {typ}")
        Provider = getattr(lazy_import(self.pkg_info['fqn']), self.pkg_info['class'])
        return Provider(name, pulumi.ResourceOptions(urn=urn))


class Module(pulumi.runtime.ResourceModule):
    def __init__(self, mod_info):
        super().__init__()
        self.mod_info = mod_info

    def version(self):
        return _version

    def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
        class_name = self.mod_info['classes'].get(typ, None)

        if class_name is None:
            raise Exception(f"unknown resource type {typ}")

        TheClass = getattr(lazy_import(self.mod_info['fqn']), class_name)
        return TheClass(name, pulumi.ResourceOptions(urn=urn))


def register(resource_modules, resource_packages):
    resource_modules = json.loads(resource_modules)
    resource_packages = json.loads(resource_packages)

    for pkg_info in resource_packages:
        pulumi.runtime.register_resource_package(pkg_info['pkg'], Package(pkg_info))

    for mod_info in resource_modules:
        pulumi.runtime.register_resource_module(
            mod_info['pkg'],
            mod_info['mod'],
            Module(mod_info))


_F = typing.TypeVar('_F', bound=typing.Callable[..., typing.Any])


def lift_output_func(func: typing.Any) -> typing.Callable[[_F], _F]:
    """Decorator internally used on {fn}_output lifted function versions
    to implement them automatically from the un-lifted function."""

    func_sig = inspect.signature(func)

    def lifted_func(*args, opts=None, **kwargs):
        bound_args = func_sig.bind(*args, **kwargs)
        # Convert tuple to list, see pulumi/pulumi#8172
        args_list = list(bound_args.args)
        return pulumi.Output.from_input({
            'args': args_list,
            'kwargs': bound_args.kwargs
        }).apply(lambda resolved_args: func(*resolved_args['args'],
                                            opts=opts,
                                            **resolved_args['kwargs']))

    return (lambda _: lifted_func)


def call_plain(
    tok: str,
    props: pulumi.Inputs,
    res: typing.Optional[pulumi.Resource] = None,
    typ: typing.Optional[type] = None,
) -> typing.Any:
    """
    Wraps pulumi.runtime.plain to force the output and return it plainly.
    """

    output = pulumi.runtime.call(tok, props, res, typ)

    # Ingoring deps silently. They are typically non-empty, r.f() calls include r as a dependency.
    result, known, secret, _ = _sync_await(asyncio.create_task(_await_output(output)))

    problem = None
    if not known:
        problem = ' an unknown value'
    elif secret:
        problem = ' a secret value'

    if problem:
        raise AssertionError(
            f"Plain resource method '{tok}' incorrectly returned {problem}. "
            + "This is an error in the provider, please report this to the provider developer."
        )

    return result


async def _await_output(o: pulumi.Output[typing.Any]) -> typing.Tuple[object, bool, bool, set]:
    return (
        await o._future,
        await o._is_known,
        await o._is_secret,
        await o._resources,
    )


# This is included to provide an upgrade path for users who are using a version
# of the Pulumi SDK (<3.121.0) that does not include the `deprecated` decorator.
def deprecated(message: str) -> typing.Callable[[C], C]:
    """
    Decorator to indicate a function is deprecated.

    As well as inserting appropriate statements to indicate that the function is
    deprecated, this decorator also tags the function with a special attribute
    so that Pulumi code can detect that it is deprecated and react appropriately
    in certain situations.

    message is the deprecation message that should be printed if the function is called.
    """

    def decorator(fn: C) -> C:
        if not callable(fn):
            raise TypeError("Expected fn to be callable")

        @functools.wraps(fn)
        def deprecated_fn(*args, **kwargs):
            warnings.warn(message)
            pulumi.warn(f"{fn.__name__} is deprecated: {message}")

            return fn(*args, **kwargs)

        deprecated_fn.__dict__["_pulumi_deprecated_callable"] = fn
        return typing.cast(C, deprecated_fn)

    return decorator

def get_plugin_download_url():
	return "github://api.github.com/pulumi/pulumi-junipermist"

def get_version():
     return _version_str
