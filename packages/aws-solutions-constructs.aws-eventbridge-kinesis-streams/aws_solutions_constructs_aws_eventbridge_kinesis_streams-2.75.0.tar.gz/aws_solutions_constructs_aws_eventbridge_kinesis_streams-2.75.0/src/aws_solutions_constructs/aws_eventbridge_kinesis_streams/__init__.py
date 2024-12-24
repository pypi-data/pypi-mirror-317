r'''
# aws-eventbridge-kinesisstreams module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_eventbridge_kinesisstreams`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-eventbridge-kinesisstreams`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.eventbridgekinesisstreams`|

## Overview

This AWS Solutions Construct implements an Amazon EventBridge rule to send data to an Amazon Kinesis Data Stream

Here is a minimal deployable pattern definition:

Typescript

```python
import { Construct } from 'constructs';
import { Stack, StackProps, Duration } from 'aws-cdk-lib';
import { EventbridgeToKinesisStreams, EventbridgeToKinesisStreamsProps } from "@aws-solutions-constructs/aws-eventbridge-kinesisstreams";
import * as events from 'aws-cdk-lib/aws-events';

const constructProps: EventbridgeToKinesisStreamsProps = {
  eventRuleProps: {
    schedule: events.Schedule.rate(Duration.minutes(5)),
  }
};

new EventbridgeToKinesisStreams(this, 'test-eventbridge-kinesis-streams', constructProps);
```

Python

```Python
from aws_solutions_constructs.aws_eventbridge_kinesis_streams import EventbridgeToKinesisStreams, EventbridgeToKinesisStreamsProps
from aws_cdk import (
    aws_events as events,
    Duration,
    Stack
)
from constructs import Construct

EventbridgeToKinesisStreams(self, 'test-eventbridge-kinesis-streams',
    event_rule_props=events.RuleProps(
        schedule=events.Schedule.rate(Duration.minutes(5)),
    ))
```

Java

```java
import software.constructs.Construct;

import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;
import software.amazon.awscdk.Duration;
import software.amazon.awscdk.services.events.*;
import software.amazon.awsconstructs.services.eventbridgekinesisstreams.*;

new EventbridgeToKinesisStreams(this, "test-eventbridge-kinesis-streams",
        new EventbridgeToKinesisStreamsProps.Builder()
                .eventRuleProps(new RuleProps.Builder()
                        .schedule(Schedule.rate(Duration.minutes(5)))
                        .build())
                .build());
```

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingEventBusInterface?|[`events.IEventBus`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.IEventBus.html)| Optional user-provided custom EventBus for construct to use. Providing both this and `eventBusProps` results an error.|
|eventBusProps?|[`events.EventBusProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.EventBusProps.html)|Optional user-provided properties to override the default properties when creating a custom EventBus. Setting this value to `{}` will create a custom EventBus using all default properties. If neither this nor `existingEventBusInterface` is provided the construct will use the `default` EventBus. Providing both this and `existingEventBusInterface` results an error.|
|eventRuleProps|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.RuleProps.html)|User provided eventRuleProps to override the defaults. |
|existingStreamObj?|[`kinesis.Stream`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kinesis.Stream.html)|Existing instance of Kinesis Stream, providing both this and `kinesisStreamProps` will cause an error.|
|kinesisStreamProps?|[`kinesis.StreamProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kinesis.StreamProps.html)|Optional user-provided props to override the default props for the Kinesis stream. |
|createCloudWatchAlarms|`boolean`|Whether to create recommended CloudWatch alarms. |

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventBus?|[`events.IEventBus`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.IEventBus.html)|Returns the instance of events.IEventBus used by the construct|
|eventsRule|[`events.Rule`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.Rule.html)|Returns an instance of events.Rule created by the construct.|
|kinesisStream|[`kinesis.Stream`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_kinesis.Stream.html)|Returns an instance of the Kinesis stream created by the pattern.|
|eventsRole?|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_iam.Role.html)|Returns an instance of the iam.Role created by the construct for events rule.|
|cloudwatchAlarms?|[`cloudwatch.Alarm[]`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cloudwatch.Alarm.html)|Returns an instance of the cloudwatch.Alarm[] created by the construct.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon EventBridge Rule

* Configure least privilege access IAM role for EventBridge Rule to publish to the Kinesis Data Stream.

### Amazon Kinesis Stream

* Enable server-side encryption for Kinesis Data Stream using AWS Managed KMS Key.

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import constructs as _constructs_77d1e7e8


class EventbridgeToKinesisStreams(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-eventbridge-kinesisstreams.EventbridgeToKinesisStreams",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
        create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
        event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
        existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        existing_stream_obj: typing.Optional[_aws_cdk_aws_kinesis_ceddda9d.Stream] = None,
        kinesis_stream_props: typing.Any = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param create_cloud_watch_alarms: Whether to create recommended CloudWatch alarms. Default: - Alarms are created
        :param event_bus_props: A new custom EventBus is created with provided props. Default: - None
        :param existing_event_bus_interface: Existing instance of a custom EventBus. Default: - None
        :param existing_stream_obj: Existing instance of Kinesis Stream object, providing both this and KinesisStreamProps will cause an error. Default: - Default props are used
        :param kinesis_stream_props: User provided props to override the default props for the Kinesis Stream. Default: - Default props are used

        :access: public
        :summary: Constructs a new instance of the EventbridgeToKinesisStreams class.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719e99574903097d001c8ae01c96eb2157eb855f1e3d20372365554dab7c2443)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EventbridgeToKinesisStreamsProps(
            event_rule_props=event_rule_props,
            create_cloud_watch_alarms=create_cloud_watch_alarms,
            event_bus_props=event_bus_props,
            existing_event_bus_interface=existing_event_bus_interface,
            existing_stream_obj=existing_stream_obj,
            kinesis_stream_props=kinesis_stream_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="eventsRole")
    def events_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "eventsRole"))

    @builtins.property
    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> _aws_cdk_aws_events_ceddda9d.Rule:
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.get(self, "eventsRule"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(self) -> _aws_cdk_aws_kinesis_ceddda9d.Stream:
        return typing.cast(_aws_cdk_aws_kinesis_ceddda9d.Stream, jsii.get(self, "kinesisStream"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarms")
    def cloudwatch_alarms(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]], jsii.get(self, "cloudwatchAlarms"))

    @builtins.property
    @jsii.member(jsii_name="eventBus")
    def event_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], jsii.get(self, "eventBus"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-eventbridge-kinesisstreams.EventbridgeToKinesisStreamsProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_rule_props": "eventRuleProps",
        "create_cloud_watch_alarms": "createCloudWatchAlarms",
        "event_bus_props": "eventBusProps",
        "existing_event_bus_interface": "existingEventBusInterface",
        "existing_stream_obj": "existingStreamObj",
        "kinesis_stream_props": "kinesisStreamProps",
    },
)
class EventbridgeToKinesisStreamsProps:
    def __init__(
        self,
        *,
        event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
        create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
        event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
        existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        existing_stream_obj: typing.Optional[_aws_cdk_aws_kinesis_ceddda9d.Stream] = None,
        kinesis_stream_props: typing.Any = None,
    ) -> None:
        '''
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param create_cloud_watch_alarms: Whether to create recommended CloudWatch alarms. Default: - Alarms are created
        :param event_bus_props: A new custom EventBus is created with provided props. Default: - None
        :param existing_event_bus_interface: Existing instance of a custom EventBus. Default: - None
        :param existing_stream_obj: Existing instance of Kinesis Stream object, providing both this and KinesisStreamProps will cause an error. Default: - Default props are used
        :param kinesis_stream_props: User provided props to override the default props for the Kinesis Stream. Default: - Default props are used

        :summary: The properties for the EventbridgeToKinesisStreams Construct
        '''
        if isinstance(event_rule_props, dict):
            event_rule_props = _aws_cdk_aws_events_ceddda9d.RuleProps(**event_rule_props)
        if isinstance(event_bus_props, dict):
            event_bus_props = _aws_cdk_aws_events_ceddda9d.EventBusProps(**event_bus_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876f8fae3e114c62d79eb38d286a96e5ab914b3fe558103d414a47be65004e1b)
            check_type(argname="argument event_rule_props", value=event_rule_props, expected_type=type_hints["event_rule_props"])
            check_type(argname="argument create_cloud_watch_alarms", value=create_cloud_watch_alarms, expected_type=type_hints["create_cloud_watch_alarms"])
            check_type(argname="argument event_bus_props", value=event_bus_props, expected_type=type_hints["event_bus_props"])
            check_type(argname="argument existing_event_bus_interface", value=existing_event_bus_interface, expected_type=type_hints["existing_event_bus_interface"])
            check_type(argname="argument existing_stream_obj", value=existing_stream_obj, expected_type=type_hints["existing_stream_obj"])
            check_type(argname="argument kinesis_stream_props", value=kinesis_stream_props, expected_type=type_hints["kinesis_stream_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_rule_props": event_rule_props,
        }
        if create_cloud_watch_alarms is not None:
            self._values["create_cloud_watch_alarms"] = create_cloud_watch_alarms
        if event_bus_props is not None:
            self._values["event_bus_props"] = event_bus_props
        if existing_event_bus_interface is not None:
            self._values["existing_event_bus_interface"] = existing_event_bus_interface
        if existing_stream_obj is not None:
            self._values["existing_stream_obj"] = existing_stream_obj
        if kinesis_stream_props is not None:
            self._values["kinesis_stream_props"] = kinesis_stream_props

    @builtins.property
    def event_rule_props(self) -> _aws_cdk_aws_events_ceddda9d.RuleProps:
        '''User provided eventRuleProps to override the defaults.

        :default: - None
        '''
        result = self._values.get("event_rule_props")
        assert result is not None, "Required property 'event_rule_props' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.RuleProps, result)

    @builtins.property
    def create_cloud_watch_alarms(self) -> typing.Optional[builtins.bool]:
        '''Whether to create recommended CloudWatch alarms.

        :default: - Alarms are created
        '''
        result = self._values.get("create_cloud_watch_alarms")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bus_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.EventBusProps]:
        '''A new custom EventBus is created with provided props.

        :default: - None
        '''
        result = self._values.get("event_bus_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.EventBusProps], result)

    @builtins.property
    def existing_event_bus_interface(
        self,
    ) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        '''Existing instance of a custom EventBus.

        :default: - None
        '''
        result = self._values.get("existing_event_bus_interface")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], result)

    @builtins.property
    def existing_stream_obj(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesis_ceddda9d.Stream]:
        '''Existing instance of Kinesis Stream object, providing both this and KinesisStreamProps will cause an error.

        :default: - Default props are used
        '''
        result = self._values.get("existing_stream_obj")
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesis_ceddda9d.Stream], result)

    @builtins.property
    def kinesis_stream_props(self) -> typing.Any:
        '''User provided props to override the default props for the Kinesis Stream.

        :default: - Default props are used
        '''
        result = self._values.get("kinesis_stream_props")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventbridgeToKinesisStreamsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EventbridgeToKinesisStreams",
    "EventbridgeToKinesisStreamsProps",
]

publication.publish()

def _typecheckingstub__719e99574903097d001c8ae01c96eb2157eb855f1e3d20372365554dab7c2443(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
    create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
    event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
    existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    existing_stream_obj: typing.Optional[_aws_cdk_aws_kinesis_ceddda9d.Stream] = None,
    kinesis_stream_props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876f8fae3e114c62d79eb38d286a96e5ab914b3fe558103d414a47be65004e1b(
    *,
    event_rule_props: typing.Union[_aws_cdk_aws_events_ceddda9d.RuleProps, typing.Dict[builtins.str, typing.Any]],
    create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
    event_bus_props: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventBusProps, typing.Dict[builtins.str, typing.Any]]] = None,
    existing_event_bus_interface: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    existing_stream_obj: typing.Optional[_aws_cdk_aws_kinesis_ceddda9d.Stream] = None,
    kinesis_stream_props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
