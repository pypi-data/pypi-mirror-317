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

__all__ = ['NotificationArgs', 'Notification']

@pulumi.input_type
class NotificationArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[int],
                 type: pulumi.Input[str],
                 value: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 responders: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]]] = None):
        """
        The set of arguments for constructing a Notification resource.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        :param pulumi.Input[str] type: Type of responder. [`team`, `user`, `escalation`, `schedule`]
        :param pulumi.Input[str] value: Integration/API key or endpoint to send the notification.
        :param pulumi.Input[str] name: Name of the responder
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: Options argument (e.g. `rk` used for VictorOps routing key).
        :param pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]] responders: An array of reponders (only for OpsGenie). Each `responders` block
               consists of the field documented below.
               
               ___
               
               The `responders` block consists of:
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if options is not None:
            pulumi.set(__self__, "options", options)
        if responders is not None:
            pulumi.set(__self__, "responders", responders)

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

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of responder. [`team`, `user`, `escalation`, `schedule`]
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Integration/API key or endpoint to send the notification.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the responder
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Options argument (e.g. `rk` used for VictorOps routing key).
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def responders(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]]]:
        """
        An array of reponders (only for OpsGenie). Each `responders` block
        consists of the field documented below.

        ___

        The `responders` block consists of:
        """
        return pulumi.get(self, "responders")

    @responders.setter
    def responders(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]]]):
        pulumi.set(self, "responders", value)


@pulumi.input_type
class _NotificationState:
    def __init__(__self__, *,
                 instance_id: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 responders: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Notification resources.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        :param pulumi.Input[str] name: Name of the responder
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: Options argument (e.g. `rk` used for VictorOps routing key).
        :param pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]] responders: An array of reponders (only for OpsGenie). Each `responders` block
               consists of the field documented below.
               
               ___
               
               The `responders` block consists of:
        :param pulumi.Input[str] type: Type of responder. [`team`, `user`, `escalation`, `schedule`]
        :param pulumi.Input[str] value: Integration/API key or endpoint to send the notification.
        """
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if options is not None:
            pulumi.set(__self__, "options", options)
        if responders is not None:
            pulumi.set(__self__, "responders", responders)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if value is not None:
            pulumi.set(__self__, "value", value)

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

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the responder
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Options argument (e.g. `rk` used for VictorOps routing key).
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def responders(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]]]:
        """
        An array of reponders (only for OpsGenie). Each `responders` block
        consists of the field documented below.

        ___

        The `responders` block consists of:
        """
        return pulumi.get(self, "responders")

    @responders.setter
    def responders(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationResponderArgs']]]]):
        pulumi.set(self, "responders", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of responder. [`team`, `user`, `escalation`, `schedule`]
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Integration/API key or endpoint to send the notification.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


class Notification(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 responders: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NotificationResponderArgs', 'NotificationResponderArgsDict']]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource allows you to create and manage recipients to receive alarm notifications. There will
        always be a default recipient created upon instance creation. This recipient will use team email and
        receive notifications from default alarms.

        Available for all subscription plans.

        ## Example Usage

        <details>
          <summary>
            <b>Email recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        email_recipient = cloudamqp.Notification("email_recipient",
            instance_id=instance["id"],
            type="email",
            value="alarm@example.com",
            name="alarm")
        ```

        </details>

        <details>
          <summary>
            <b>OpsGenie recipient with optional responders</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        opsgenie_recipient = cloudamqp.Notification("opsgenie_recipient",
            instance_id=instance["id"],
            type="opsgenie",
            value="<api-key>",
            name="OpsGenie",
            responders=[
                {
                    "type": "team",
                    "id": "<team-uuid>",
                },
                {
                    "type": "user",
                    "username": "<username>",
                },
            ])
        ```

        </details>

        <details>
          <summary>
            <b>Pagerduty recipient with optional dedup key</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        pagerduty_recipient = cloudamqp.Notification("pagerduty_recipient",
            instance_id=instance["id"],
            type="pagerduty",
            value="<integration-key>",
            name="PagerDuty",
            options={
                "dedupkey": "DEDUPKEY",
            })
        ```

        </details>

        <details>
          <summary>
            <b>Signl4 recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        signl4_recipient = cloudamqp.Notification("signl4_recipient",
            instance_id=instance["id"],
            type="signl4",
            value="<team-secret>",
            name="Signl4")
        ```

        </details>

        <details>
          <summary>
            <b>Teams recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        teams_recipient = cloudamqp.Notification("teams_recipient",
            instance_id=instance["id"],
            type="teams",
            value="<teams-webhook-url>",
            name="Teams")
        ```

        </details>

        <details>
          <summary>
            <b>Victorops recipient with optional routing key (rk)</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        victorops_recipient = cloudamqp.Notification("victorops_recipient",
            instance_id=instance["id"],
            type="victorops",
            value="<integration-key>",
            name="Victorops",
            options={
                "rk": "ROUTINGKEY",
            })
        ```

        </details>

        <details>
          <summary>
            <b>Slack recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        slack_recipient = cloudamqp.Notification("slack_recipient",
            instance_id=instance["id"],
            type="slack",
            value="<slack-webhook-url>",
            name="Slack webhook recipient")
        ```

        </details>

        <details>
          <summary>
            <b>Webhook recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        webhook_recipient = cloudamqp.Notification("webhook_recipient",
            instance_id=instance["id"],
            type="webhook",
            value="<webhook-url>",
            name="Webhook")
        ```

        </details>

        ## Notification Type reference

        Valid options for notification type.

        * email
        * opsgenie
        * opsgenie-eu
        * pagerduty
        * signl4
        * slack
        * teams
        * victorops
        * webhook

        ## Options parameter

        | Type      | Options  | Description | Note |
        |---|---|---|---|
        | Victorops | rk       | Routing key to route alarm notification | - |
        | PagerDuty | dedupkey | Default the dedup key for PagerDuty is generated depending on what alarm has triggered, but here you can set what `dedup` key to use so even if the same alarm is triggered for different resources you only get one notification. Leave blank to use the generated dedup key. | If multiple alarms are triggered using this recipient, since they all share `dedup` key only the first alarm will be shown in PagerDuty |

        ## Dependency

        This resource depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.

        ## Import

        `cloudamqp_notification` can be imported using CloudAMQP internal identifier of a recipient together

        (CSV separated) with the instance identifier. To retrieve the identifier of a recipient, use

        [CloudAMQP API](https://docs.cloudamqp.com/cloudamqp_api.html#list-recipients).

        ```sh
        $ pulumi import cloudamqp:index/notification:Notification recipient <id>,<instance_id>`
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        :param pulumi.Input[str] name: Name of the responder
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: Options argument (e.g. `rk` used for VictorOps routing key).
        :param pulumi.Input[Sequence[pulumi.Input[Union['NotificationResponderArgs', 'NotificationResponderArgsDict']]]] responders: An array of reponders (only for OpsGenie). Each `responders` block
               consists of the field documented below.
               
               ___
               
               The `responders` block consists of:
        :param pulumi.Input[str] type: Type of responder. [`team`, `user`, `escalation`, `schedule`]
        :param pulumi.Input[str] value: Integration/API key or endpoint to send the notification.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NotificationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows you to create and manage recipients to receive alarm notifications. There will
        always be a default recipient created upon instance creation. This recipient will use team email and
        receive notifications from default alarms.

        Available for all subscription plans.

        ## Example Usage

        <details>
          <summary>
            <b>Email recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        email_recipient = cloudamqp.Notification("email_recipient",
            instance_id=instance["id"],
            type="email",
            value="alarm@example.com",
            name="alarm")
        ```

        </details>

        <details>
          <summary>
            <b>OpsGenie recipient with optional responders</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        opsgenie_recipient = cloudamqp.Notification("opsgenie_recipient",
            instance_id=instance["id"],
            type="opsgenie",
            value="<api-key>",
            name="OpsGenie",
            responders=[
                {
                    "type": "team",
                    "id": "<team-uuid>",
                },
                {
                    "type": "user",
                    "username": "<username>",
                },
            ])
        ```

        </details>

        <details>
          <summary>
            <b>Pagerduty recipient with optional dedup key</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        pagerduty_recipient = cloudamqp.Notification("pagerduty_recipient",
            instance_id=instance["id"],
            type="pagerduty",
            value="<integration-key>",
            name="PagerDuty",
            options={
                "dedupkey": "DEDUPKEY",
            })
        ```

        </details>

        <details>
          <summary>
            <b>Signl4 recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        signl4_recipient = cloudamqp.Notification("signl4_recipient",
            instance_id=instance["id"],
            type="signl4",
            value="<team-secret>",
            name="Signl4")
        ```

        </details>

        <details>
          <summary>
            <b>Teams recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        teams_recipient = cloudamqp.Notification("teams_recipient",
            instance_id=instance["id"],
            type="teams",
            value="<teams-webhook-url>",
            name="Teams")
        ```

        </details>

        <details>
          <summary>
            <b>Victorops recipient with optional routing key (rk)</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        victorops_recipient = cloudamqp.Notification("victorops_recipient",
            instance_id=instance["id"],
            type="victorops",
            value="<integration-key>",
            name="Victorops",
            options={
                "rk": "ROUTINGKEY",
            })
        ```

        </details>

        <details>
          <summary>
            <b>Slack recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        slack_recipient = cloudamqp.Notification("slack_recipient",
            instance_id=instance["id"],
            type="slack",
            value="<slack-webhook-url>",
            name="Slack webhook recipient")
        ```

        </details>

        <details>
          <summary>
            <b>Webhook recipient</b>
          </summary>

        ```python
        import pulumi
        import pulumi_cloudamqp as cloudamqp

        webhook_recipient = cloudamqp.Notification("webhook_recipient",
            instance_id=instance["id"],
            type="webhook",
            value="<webhook-url>",
            name="Webhook")
        ```

        </details>

        ## Notification Type reference

        Valid options for notification type.

        * email
        * opsgenie
        * opsgenie-eu
        * pagerduty
        * signl4
        * slack
        * teams
        * victorops
        * webhook

        ## Options parameter

        | Type      | Options  | Description | Note |
        |---|---|---|---|
        | Victorops | rk       | Routing key to route alarm notification | - |
        | PagerDuty | dedupkey | Default the dedup key for PagerDuty is generated depending on what alarm has triggered, but here you can set what `dedup` key to use so even if the same alarm is triggered for different resources you only get one notification. Leave blank to use the generated dedup key. | If multiple alarms are triggered using this recipient, since they all share `dedup` key only the first alarm will be shown in PagerDuty |

        ## Dependency

        This resource depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.

        ## Import

        `cloudamqp_notification` can be imported using CloudAMQP internal identifier of a recipient together

        (CSV separated) with the instance identifier. To retrieve the identifier of a recipient, use

        [CloudAMQP API](https://docs.cloudamqp.com/cloudamqp_api.html#list-recipients).

        ```sh
        $ pulumi import cloudamqp:index/notification:Notification recipient <id>,<instance_id>`
        ```

        :param str resource_name: The name of the resource.
        :param NotificationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NotificationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 responders: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NotificationResponderArgs', 'NotificationResponderArgsDict']]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NotificationArgs.__new__(NotificationArgs)

            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["name"] = name
            __props__.__dict__["options"] = options
            __props__.__dict__["responders"] = responders
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            if value is None and not opts.urn:
                raise TypeError("Missing required property 'value'")
            __props__.__dict__["value"] = value
        super(Notification, __self__).__init__(
            'cloudamqp:index/notification:Notification',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_id: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            responders: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NotificationResponderArgs', 'NotificationResponderArgsDict']]]]] = None,
            type: Optional[pulumi.Input[str]] = None,
            value: Optional[pulumi.Input[str]] = None) -> 'Notification':
        """
        Get an existing Notification resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] instance_id: The CloudAMQP instance ID.
        :param pulumi.Input[str] name: Name of the responder
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: Options argument (e.g. `rk` used for VictorOps routing key).
        :param pulumi.Input[Sequence[pulumi.Input[Union['NotificationResponderArgs', 'NotificationResponderArgsDict']]]] responders: An array of reponders (only for OpsGenie). Each `responders` block
               consists of the field documented below.
               
               ___
               
               The `responders` block consists of:
        :param pulumi.Input[str] type: Type of responder. [`team`, `user`, `escalation`, `schedule`]
        :param pulumi.Input[str] value: Integration/API key or endpoint to send the notification.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NotificationState.__new__(_NotificationState)

        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["name"] = name
        __props__.__dict__["options"] = options
        __props__.__dict__["responders"] = responders
        __props__.__dict__["type"] = type
        __props__.__dict__["value"] = value
        return Notification(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[int]:
        """
        The CloudAMQP instance ID.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the responder
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Options argument (e.g. `rk` used for VictorOps routing key).
        """
        return pulumi.get(self, "options")

    @property
    @pulumi.getter
    def responders(self) -> pulumi.Output[Optional[Sequence['outputs.NotificationResponder']]]:
        """
        An array of reponders (only for OpsGenie). Each `responders` block
        consists of the field documented below.

        ___

        The `responders` block consists of:
        """
        return pulumi.get(self, "responders")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of responder. [`team`, `user`, `escalation`, `schedule`]
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[str]:
        """
        Integration/API key or endpoint to send the notification.
        """
        return pulumi.get(self, "value")

