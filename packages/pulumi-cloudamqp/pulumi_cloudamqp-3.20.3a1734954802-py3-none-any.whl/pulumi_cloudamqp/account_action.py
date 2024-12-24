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

__all__ = ['AccountActionArgs', 'AccountAction']

@pulumi.input_type
class AccountActionArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 instance_id: pulumi.Input[int]):
        """
        The set of arguments for constructing a AccountAction resource.
        :param pulumi.Input[str] action: The action to be invoked. Allowed actions `rotate-password`, `rotate-apikey`.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "instance_id", instance_id)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        The action to be invoked. Allowed actions `rotate-password`, `rotate-apikey`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[int]:
        """
        The CloudAMQP instance ID.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "instance_id", value)


@pulumi.input_type
class _AccountActionState:
    def __init__(__self__, *,
                 action: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering AccountAction resources.
        :param pulumi.Input[str] action: The action to be invoked. Allowed actions `rotate-password`, `rotate-apikey`.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[str]]:
        """
        The action to be invoked. Allowed actions `rotate-password`, `rotate-apikey`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[int]]:
        """
        The CloudAMQP instance ID.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "instance_id", value)


class AccountAction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## Import

        Not possible to import this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The action to be invoked. Allowed actions `rotate-password`, `rotate-apikey`.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountActionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        Not possible to import this resource.

        :param str resource_name: The name of the resource.
        :param AccountActionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountActionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountActionArgs.__new__(AccountActionArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
        super(AccountAction, __self__).__init__(
            'cloudamqp:index/accountAction:AccountAction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[int]] = None) -> 'AccountAction':
        """
        Get an existing AccountAction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The action to be invoked. Allowed actions `rotate-password`, `rotate-apikey`.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountActionState.__new__(_AccountActionState)

        __props__.__dict__["action"] = action
        __props__.__dict__["instance_id"] = instance_id
        return AccountAction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        The action to be invoked. Allowed actions `rotate-password`, `rotate-apikey`.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[int]:
        """
        The CloudAMQP instance ID.
        """
        return pulumi.get(self, "instance_id")

