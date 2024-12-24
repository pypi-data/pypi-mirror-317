r'''
# aws-constructs-factories module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_constructs_factories`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-constructs-factories`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.constructsfactories`|

## Overview

This AWS Solutions Construct exposes the same code used to create our underlying resources as factories, so clients can create individual resources that are well-architected.
There are factories to create:

[Amazon S3 buckets](https://docs.aws.amazon.com/solutions/latest/constructs/aws-constructs-factories.html#s3-buckets) - Create a well architected S3 bucket (e.g. - includes an access logging bucket)
[AWS Step Functions state machines](https://docs.aws.amazon.com/solutions/latest/constructs/aws-constructs-factories.html#step-functions-state-machines) - Create a well architected Step Functions state machine and log group (e.g. log group has /aws/vendedlogs/ name prefix to avoid resource policy issues)

## S3 Buckets

Create fully well-architected S3 buckets with as little as one function call. Here is a minimal deployable pattern definition:

Typescript

```python
import { Construct } from 'constructs';
import { Stack, StackProps } from 'aws-cdk-lib';
import { ConstructsFactories } from '@aws-solutions-constructs/aws-constructs-factories';

const factories = new ConstructsFactories(this, 'MyFactories');

factories.s3BucketFactory('GoodBucket', {});
```

Python

```python
from aws_cdk import (
    Stack,
)
from constructs import Construct

from aws_solutions_constructs import (
    aws_constructs_factories as cf
)

factories = cf.ConstructsFactories(self, 'MyFactories')
factories.s3_bucket_factory('GoodBucket')
```

Java

```java
import software.constructs.Construct;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awsconstructs.services.constructsfactories.ConstructsFactories;
import software.amazon.awsconstructs.services.constructsfactories.S3BucketFactoryProps;

final ConstructsFactories factories = new ConstructsFactories(this, "MyFactories");
factories.s3BucketFactory("GoodBucket",
  new S3BucketFactoryProps.Builder().build());
```

# S3BucketFactory Function Signature

```python
s3BucketFactory(id: string, props: S3BucketFactoryProps): S3BucketFactoryResponse
```

# S3BucketFactoryProps

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.BucketProps.html)|Optional user provided props to override the default props for the S3 Bucket.|
|logS3AccessLogs?|`boolean`|Whether to turn on Access Logging for the S3 bucket. Creates an S3 bucket with associated storage costs for the logs. Enabling Access Logging is a best practice. default - true|
|loggingBucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.BucketProps.html)|Optional user provided props to override the default props for the S3 Logging Bucket.|

# S3BucketFactoryResponse

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|s3Bucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html)|The s3.Bucket created by the factory. |
|s3LoggingBucket?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html)|The s3.Bucket created by the construct as the logging bucket for the primary bucket. If the logS3AccessLogs property is false, this value will be undefined.|

# Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

* An S3 Content Bucket

  * AWS managed Server Side Encryption (AES256)
  * Lifecycle rule to transition objects to Glacier storage class in 90 days
  * Access Logging enabled
  * All Public access blocked
  * Versioning enabled
  * UpdateReplacePolicy is delete
  * Deletion policy is delete
  * Bucket policy requiring SecureTransport
* An S3 Bucket for Access Logs

  * AWS managed Server Side Encryption (AES256)
  * All public access blocked
  * Versioning enabled
  * UpdateReplacePolicy is delete
  * Deletion policy is delete
  * Bucket policy requiring SecureTransport
  * Bucket policy granting PutObject privileges to the S3 logging service, from the content bucket in the content bucket account.
  * cfn_nag suppression of access logging finding (not logging access to the access log bucket)

# Architecture

![Architecture Diagram](architecture.png)

## Step Functions State Machines

Create fully well-architected Step Functions state machine with log group. The log group name includes the vendedlogs prefix. Here
but is unique to the stack, avoiding naming collions between instances. is a minimal deployable pattern definition:

Typescript

```python
import { App, Stack } from "aws-cdk-lib";
import { ConstructsFactories } from "../../lib";
import { generateIntegStackName, CreateTestStateMachineDefinitionBody } from '@aws-solutions-constructs/core';
import { IntegTest } from '@aws-cdk/integ-tests-alpha';

const placeholderTask = new sftasks.EvaluateExpression(this, 'placeholder', {
  expression: '$.argOne + $.argTwo'
});

const factories = new ConstructsFactories(this, 'minimalImplementation');

factories.stateMachineFactory('testsm', {
  stateMachineProps: {
    definitionBody: sfn.DefinitionBody.fromChainable(placeholderTask)
  }
});
```

Python

```python

# Pending

```

Java

```java

// Pending

```

# stateMachineFactory Function Signature

```python
stateMachineFactory(id: string, props: StateMachineFactoryProps): StateMachineFactoryResponse
```

# StateMachineFactoryProps

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|stateMachineProps|[`sfn.StateMachineProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions.StateMachineProps.html)|The CDK properties that define the state machine. This property is required and must include a definitionBody or definition (definition is deprecated)|
|logGroup?|[]`logs.LogGroup`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_logs.LogGroup.html)|An existing LogGroup to which the new state machine will write log entries. Default: none, the construct will create a new log group.|
|createCloudWatchAlarms?|boolean|Whether to create recommended CloudWatch alarms for the State Machine. Default: the alarms are created|
|cloudWatchAlarmsPrefix?|string|Creating multiple State Machines with one Factories construct will result in name collisions as the cloudwatch alarms originally had fixed resource ids. This value was added to avoid collisions while not making changes that would be destructive for existing stacks. Unless you are creating multiple State Machines using factories you can ignore it|

# StateMachineFactoryResponse

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|stateMachineProps|[`sfn.StateMachineProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions.StateMachineProps.html)||
|logGroup|[]`logs.LogGroupProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_logs.LogGroupProps.html)||
|cloudwatchAlarms?|[`cloudwatch.Alarm[]`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cloudwatch.Alarm.html)|The alarms created by the factory (ExecutionFailed, ExecutionThrottled, ExecutionAborted)|

# Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

* An AWS Step Functions State Machine

  * Configured to log to the new log group at LogLevel.ERROR
* Amazon CloudWatch Logs Log Group

  * Log name is prefaced with /aws/vendedlogs/ to avoid resource policy [issues](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html#cloudwatch-iam-policy). The Log Group name is still created to be unique to the stack to avoid name collisions.
* CloudWatch alarms for:

  * 1 or more failed executions
  * 1 or more executions being throttled
  * 1 or more executions being aborted

# Architecture

![Architecture Diagram](sf-architecture.png)

## SQS Queues

Create SQS queues complete with DLQs and KMS CMKs with one function call. Here is a minimal deployable pattern definition:

Typescript

```python
import { Construct } from 'constructs';
import { Stack, StackProps } from 'aws-cdk-lib';
import { ConstructsFactories } from '@aws-solutions-constructs/aws-constructs-factories';

const factories = new ConstructsFactories(this, 'MyFactories');

factories.sqsQueueFacgory('GoodQueue', {});
```

Python

```python
Pending
```

Java

```java
Pendiong
```

# SqsQueueFactory Function Signature

```python
SqsQueueFactory(id: string, props: SqsQueueFactoryProps): SqsQueueFactoryResponse
```

# SqsQueueFactoryProps

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|queueProps?|sqs.QueueProps|Optional user provided props to override the default props for the primary queue.|
|enableEncryptionWithCustomerManagedKey?|boolean|If no key is provided, this flag determines whether the queue is encrypted with a new CMK or an AWS managed key. This flag is ignored if any of the following are defined: queueProps.encryptionMasterKey, encryptionKey or encryptionKeyProps. default - False if queueProps.encryptionMasterKey, encryptionKey, and encryptionKeyProps are all undefined.|
|encryptionKey?|kms.Key|An optional, imported encryption key to encrypt the SQS Queue with. Default - none|
|encryptionKeyProps?|kms.KeyProps|Optional user provided properties to override the default properties for the KMS encryption key used to encrypt the SQS Queue with. @default - None|
|deployDeadLetterQueue?|boolean|Whether to deploy a secondary queue to be used as a dead letter queue.|
|deadLetterQueueProps?|sqs.QueueProps|Optional user provided properties for the dead letter queue|
|maxReceiveCount?|number|The number of times a message can be unsuccessfully dequeued before being moved to the dead letter queue. default - [code](https://github.com/awslabs/aws-solutions-constructs/blob/8b30791902e09db2f7c49410a03d5d95ccc2ef51/source/patterns/%40aws-solutions-constructs/core/lib/sqs-defaults.ts#L32)|

# SqsQueueFactoryResponse

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|queue|sqs.Queue|The queue created by the factory.|
|key|kms.IKey|The key used to encrypt the queue, if the queue was configured to use a CMK|
|deadLetterQueue?|sqs.DeadLetterQueue|The dead letter queue associated with the queue created by the factory|

# Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

* An SQS queue

  * Encrypted by default with KMS managed key by default, can be KMS CMK if flag is set
  * Only queue owner can perform operations by default (your IAM policies can override)
  * Enforced encryption for data in transit
  * DLQ configured
* An SQS dead letter queue

  * Receives messages not processable in maxReceiveCount attempts
  * Encrypted with KMS managed key
  * Enforced encryption for data in transit

# Architecture

![Architecture Diagram](sqs-architecture.png)

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
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


class ConstructsFactories(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.ConstructsFactories",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605983066d245d838df0751ca3d83223b93e3dac7281a9b7677ff8c39ccd96d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="s3BucketFactory")
    def s3_bucket_factory(
        self,
        id: builtins.str,
        *,
        bucket_props: typing.Any = None,
        logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        log_s3_access_logs: typing.Optional[builtins.bool] = None,
    ) -> "S3BucketFactoryResponse":
        '''
        :param id: -
        :param bucket_props: -
        :param logging_bucket_props: -
        :param log_s3_access_logs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b90bfb94c5304484be85483634a7064b119ae1b0c5ed7cfc594e3e7bbf37f0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3BucketFactoryProps(
            bucket_props=bucket_props,
            logging_bucket_props=logging_bucket_props,
            log_s3_access_logs=log_s3_access_logs,
        )

        return typing.cast("S3BucketFactoryResponse", jsii.invoke(self, "s3BucketFactory", [id, props]))

    @jsii.member(jsii_name="sqsQueueFactory")
    def sqs_queue_factory(
        self,
        id: builtins.str,
        *,
        dead_letter_queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        encryption_key_props: typing.Optional[typing.Union[_aws_cdk_aws_kms_ceddda9d.KeyProps, typing.Dict[builtins.str, typing.Any]]] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "SqsQueueFactoryResponse":
        '''
        :param id: -
        :param dead_letter_queue_props: Optional user provided properties for the dead letter queue. Default: - Default props are used
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true
        :param enable_encryption_with_customer_managed_key: If no key is provided, this flag determines whether the queue is encrypted with a new CMK or an AWS managed key. This flag is ignored if any of the following are defined: queueProps.encryptionMasterKey, encryptionKey or encryptionKeyProps. Default: - False if queueProps.encryptionMasterKey, encryptionKey, and encryptionKeyProps are all undefined.
        :param encryption_key: An optional, imported encryption key to encrypt the SQS Queue with. Default: - None
        :param encryption_key_props: Optional user provided properties to override the default properties for the KMS encryption key used to encrypt the SQS Queue with. Default: - None
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead letter queue. Default: - Default props are used
        :param queue_props: Optional user provided props to override the default props for the primary queue. Default: - Default props are used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf99c1a76dccb709a8410aeed535e4d0c6fd49506e1e3bb9bd4e95a2dd4648d5)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SqsQueueFactoryProps(
            dead_letter_queue_props=dead_letter_queue_props,
            deploy_dead_letter_queue=deploy_dead_letter_queue,
            enable_encryption_with_customer_managed_key=enable_encryption_with_customer_managed_key,
            encryption_key=encryption_key,
            encryption_key_props=encryption_key_props,
            max_receive_count=max_receive_count,
            queue_props=queue_props,
        )

        return typing.cast("SqsQueueFactoryResponse", jsii.invoke(self, "sqsQueueFactory", [id, props]))

    @jsii.member(jsii_name="stateMachineFactory")
    def state_machine_factory(
        self,
        id: builtins.str,
        *,
        state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
        cloud_watch_alarms_prefix: typing.Optional[builtins.str] = None,
        create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "StateMachineFactoryResponse":
        '''
        :param id: -
        :param state_machine_props: The CDK properties that define the state machine. This property is required and must include a definitionBody or definition (definition is deprecated)
        :param cloud_watch_alarms_prefix: Creating multiple State Machines in 1 stack with constructs will result in name collisions as the cloudwatch alarms originally had fixed resource ids. This value was added to avoid collisions while not making changes that would be destructive for existing stacks. Unless you are creating multiple State Machines using constructs you can ignore it. Default: - undefined
        :param create_cloud_watch_alarms: Whether to create recommended CloudWatch alarms. Default: - Alarms are created
        :param log_group_props: An existing LogGroup to which the new state machine will write log entries. Default: none, the construct will create a new log group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8ce2d58c9a66b894497fcb91691d41649f06370c9e15b72ef1373fbe0d05c6)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StateMachineFactoryProps(
            state_machine_props=state_machine_props,
            cloud_watch_alarms_prefix=cloud_watch_alarms_prefix,
            create_cloud_watch_alarms=create_cloud_watch_alarms,
            log_group_props=log_group_props,
        )

        return typing.cast("StateMachineFactoryResponse", jsii.invoke(self, "stateMachineFactory", [id, props]))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.S3BucketFactoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_props": "bucketProps",
        "logging_bucket_props": "loggingBucketProps",
        "log_s3_access_logs": "logS3AccessLogs",
    },
)
class S3BucketFactoryProps:
    def __init__(
        self,
        *,
        bucket_props: typing.Any = None,
        logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        log_s3_access_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bucket_props: -
        :param logging_bucket_props: -
        :param log_s3_access_logs: -
        '''
        if isinstance(logging_bucket_props, dict):
            logging_bucket_props = _aws_cdk_aws_s3_ceddda9d.BucketProps(**logging_bucket_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a251aca0d0848bcaeaed9669ce040e9bd9f304c875a3796313bd27abcdacc3)
            check_type(argname="argument bucket_props", value=bucket_props, expected_type=type_hints["bucket_props"])
            check_type(argname="argument logging_bucket_props", value=logging_bucket_props, expected_type=type_hints["logging_bucket_props"])
            check_type(argname="argument log_s3_access_logs", value=log_s3_access_logs, expected_type=type_hints["log_s3_access_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_props is not None:
            self._values["bucket_props"] = bucket_props
        if logging_bucket_props is not None:
            self._values["logging_bucket_props"] = logging_bucket_props
        if log_s3_access_logs is not None:
            self._values["log_s3_access_logs"] = log_s3_access_logs

    @builtins.property
    def bucket_props(self) -> typing.Any:
        result = self._values.get("bucket_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def logging_bucket_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps]:
        result = self._values.get("logging_bucket_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps], result)

    @builtins.property
    def log_s3_access_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("log_s3_access_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketFactoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.S3BucketFactoryResponse",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket": "s3Bucket", "s3_logging_bucket": "s3LoggingBucket"},
)
class S3BucketFactoryResponse:
    def __init__(
        self,
        *,
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
        s3_logging_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
    ) -> None:
        '''
        :param s3_bucket: -
        :param s3_logging_bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e83545e4e90253a16e42d104a9338e2ce2020b20c95b614ea013e7c4918073)
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_logging_bucket", value=s3_logging_bucket, expected_type=type_hints["s3_logging_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket": s3_bucket,
        }
        if s3_logging_bucket is not None:
            self._values["s3_logging_bucket"] = s3_logging_bucket

    @builtins.property
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, result)

    @builtins.property
    def s3_logging_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        result = self._values.get("s3_logging_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketFactoryResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.SqsQueueFactoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue_props": "deadLetterQueueProps",
        "deploy_dead_letter_queue": "deployDeadLetterQueue",
        "enable_encryption_with_customer_managed_key": "enableEncryptionWithCustomerManagedKey",
        "encryption_key": "encryptionKey",
        "encryption_key_props": "encryptionKeyProps",
        "max_receive_count": "maxReceiveCount",
        "queue_props": "queueProps",
    },
)
class SqsQueueFactoryProps:
    def __init__(
        self,
        *,
        dead_letter_queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        encryption_key_props: typing.Optional[typing.Union[_aws_cdk_aws_kms_ceddda9d.KeyProps, typing.Dict[builtins.str, typing.Any]]] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dead_letter_queue_props: Optional user provided properties for the dead letter queue. Default: - Default props are used
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true
        :param enable_encryption_with_customer_managed_key: If no key is provided, this flag determines whether the queue is encrypted with a new CMK or an AWS managed key. This flag is ignored if any of the following are defined: queueProps.encryptionMasterKey, encryptionKey or encryptionKeyProps. Default: - False if queueProps.encryptionMasterKey, encryptionKey, and encryptionKeyProps are all undefined.
        :param encryption_key: An optional, imported encryption key to encrypt the SQS Queue with. Default: - None
        :param encryption_key_props: Optional user provided properties to override the default properties for the KMS encryption key used to encrypt the SQS Queue with. Default: - None
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead letter queue. Default: - Default props are used
        :param queue_props: Optional user provided props to override the default props for the primary queue. Default: - Default props are used.
        '''
        if isinstance(dead_letter_queue_props, dict):
            dead_letter_queue_props = _aws_cdk_aws_sqs_ceddda9d.QueueProps(**dead_letter_queue_props)
        if isinstance(encryption_key_props, dict):
            encryption_key_props = _aws_cdk_aws_kms_ceddda9d.KeyProps(**encryption_key_props)
        if isinstance(queue_props, dict):
            queue_props = _aws_cdk_aws_sqs_ceddda9d.QueueProps(**queue_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357772658c56c210047c7fbddf97a03753fe395062f8ccafa942fbf9b229b6fb)
            check_type(argname="argument dead_letter_queue_props", value=dead_letter_queue_props, expected_type=type_hints["dead_letter_queue_props"])
            check_type(argname="argument deploy_dead_letter_queue", value=deploy_dead_letter_queue, expected_type=type_hints["deploy_dead_letter_queue"])
            check_type(argname="argument enable_encryption_with_customer_managed_key", value=enable_encryption_with_customer_managed_key, expected_type=type_hints["enable_encryption_with_customer_managed_key"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument encryption_key_props", value=encryption_key_props, expected_type=type_hints["encryption_key_props"])
            check_type(argname="argument max_receive_count", value=max_receive_count, expected_type=type_hints["max_receive_count"])
            check_type(argname="argument queue_props", value=queue_props, expected_type=type_hints["queue_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue_props is not None:
            self._values["dead_letter_queue_props"] = dead_letter_queue_props
        if deploy_dead_letter_queue is not None:
            self._values["deploy_dead_letter_queue"] = deploy_dead_letter_queue
        if enable_encryption_with_customer_managed_key is not None:
            self._values["enable_encryption_with_customer_managed_key"] = enable_encryption_with_customer_managed_key
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if encryption_key_props is not None:
            self._values["encryption_key_props"] = encryption_key_props
        if max_receive_count is not None:
            self._values["max_receive_count"] = max_receive_count
        if queue_props is not None:
            self._values["queue_props"] = queue_props

    @builtins.property
    def dead_letter_queue_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.QueueProps]:
        '''Optional user provided properties for the dead letter queue.

        :default: - Default props are used
        '''
        result = self._values.get("dead_letter_queue_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.QueueProps], result)

    @builtins.property
    def deploy_dead_letter_queue(self) -> typing.Optional[builtins.bool]:
        '''Whether to deploy a secondary queue to be used as a dead letter queue.

        :default: - true
        '''
        result = self._values.get("deploy_dead_letter_queue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_encryption_with_customer_managed_key(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''If no key is provided, this flag determines whether the queue is encrypted with a new CMK or an AWS managed key.

        This flag is ignored if any of the following are defined: queueProps.encryptionMasterKey, encryptionKey or encryptionKeyProps.

        :default: - False if queueProps.encryptionMasterKey, encryptionKey, and encryptionKeyProps are all undefined.
        '''
        result = self._values.get("enable_encryption_with_customer_managed_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        '''An optional, imported encryption key to encrypt the SQS Queue with.

        :default: - None
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], result)

    @builtins.property
    def encryption_key_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.KeyProps]:
        '''Optional user provided properties to override the default properties for the KMS encryption key used to encrypt the SQS Queue with.

        :default: - None
        '''
        result = self._values.get("encryption_key_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.KeyProps], result)

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        '''The number of times a message can be unsuccessfully dequeued before being moved to the dead letter queue.

        :default: - Default props are used
        '''
        result = self._values.get("max_receive_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_props(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.QueueProps]:
        '''Optional user provided props to override the default props for the primary queue.

        :default: - Default props are used.
        '''
        result = self._values.get("queue_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.QueueProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueFactoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.SqsQueueFactoryResponse",
    jsii_struct_bases=[],
    name_mapping={
        "queue": "queue",
        "dead_letter_queue": "deadLetterQueue",
        "key": "key",
    },
)
class SqsQueueFactoryResponse:
    def __init__(
        self,
        *,
        queue: _aws_cdk_aws_sqs_ceddda9d.Queue,
        dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
        key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''
        :param queue: -
        :param dead_letter_queue: -
        :param key: -
        '''
        if isinstance(dead_letter_queue, dict):
            dead_letter_queue = _aws_cdk_aws_sqs_ceddda9d.DeadLetterQueue(**dead_letter_queue)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd81db84d5c3594de6e2da5168709e73ddb24db1d425ea510f2e8891bc71e32)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue": queue,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def queue(self) -> _aws_cdk_aws_sqs_ceddda9d.Queue:
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast(_aws_cdk_aws_sqs_ceddda9d.Queue, result)

    @builtins.property
    def dead_letter_queue(
        self,
    ) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.DeadLetterQueue]:
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.DeadLetterQueue], result)

    @builtins.property
    def key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        result = self._values.get("key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueFactoryResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.StateMachineFactoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "state_machine_props": "stateMachineProps",
        "cloud_watch_alarms_prefix": "cloudWatchAlarmsPrefix",
        "create_cloud_watch_alarms": "createCloudWatchAlarms",
        "log_group_props": "logGroupProps",
    },
)
class StateMachineFactoryProps:
    def __init__(
        self,
        *,
        state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
        cloud_watch_alarms_prefix: typing.Optional[builtins.str] = None,
        create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param state_machine_props: The CDK properties that define the state machine. This property is required and must include a definitionBody or definition (definition is deprecated)
        :param cloud_watch_alarms_prefix: Creating multiple State Machines in 1 stack with constructs will result in name collisions as the cloudwatch alarms originally had fixed resource ids. This value was added to avoid collisions while not making changes that would be destructive for existing stacks. Unless you are creating multiple State Machines using constructs you can ignore it. Default: - undefined
        :param create_cloud_watch_alarms: Whether to create recommended CloudWatch alarms. Default: - Alarms are created
        :param log_group_props: An existing LogGroup to which the new state machine will write log entries. Default: none, the construct will create a new log group.
        '''
        if isinstance(state_machine_props, dict):
            state_machine_props = _aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps(**state_machine_props)
        if isinstance(log_group_props, dict):
            log_group_props = _aws_cdk_aws_logs_ceddda9d.LogGroupProps(**log_group_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ef38c5b8793990636642f918f311333d9be77dfc62aec7517d2993d778bdb1)
            check_type(argname="argument state_machine_props", value=state_machine_props, expected_type=type_hints["state_machine_props"])
            check_type(argname="argument cloud_watch_alarms_prefix", value=cloud_watch_alarms_prefix, expected_type=type_hints["cloud_watch_alarms_prefix"])
            check_type(argname="argument create_cloud_watch_alarms", value=create_cloud_watch_alarms, expected_type=type_hints["create_cloud_watch_alarms"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "state_machine_props": state_machine_props,
        }
        if cloud_watch_alarms_prefix is not None:
            self._values["cloud_watch_alarms_prefix"] = cloud_watch_alarms_prefix
        if create_cloud_watch_alarms is not None:
            self._values["create_cloud_watch_alarms"] = create_cloud_watch_alarms
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props

    @builtins.property
    def state_machine_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps:
        '''The CDK properties that define the state machine.

        This property is required and
        must include a definitionBody or definition (definition is deprecated)
        '''
        result = self._values.get("state_machine_props")
        assert result is not None, "Required property 'state_machine_props' is missing"
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, result)

    @builtins.property
    def cloud_watch_alarms_prefix(self) -> typing.Optional[builtins.str]:
        '''Creating multiple State Machines in 1 stack with constructs will result in name collisions as the cloudwatch alarms originally had fixed resource ids.

        This value was added to avoid collisions while not making changes that would be
        destructive for existing stacks. Unless you are creating multiple State Machines using constructs
        you can ignore it.

        :default: - undefined
        '''
        result = self._values.get("cloud_watch_alarms_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_cloud_watch_alarms(self) -> typing.Optional[builtins.bool]:
        '''Whether to create recommended CloudWatch alarms.

        :default: - Alarms are created
        '''
        result = self._values.get("create_cloud_watch_alarms")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_group_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps]:
        '''An existing LogGroup to which the new state machine will write log entries.

        Default: none, the construct will create a new log group.
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineFactoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.StateMachineFactoryResponse",
    jsii_struct_bases=[],
    name_mapping={
        "log_group": "logGroup",
        "state_machine": "stateMachine",
        "cloudwatch_alarms": "cloudwatchAlarms",
    },
)
class StateMachineFactoryResponse:
    def __init__(
        self,
        *,
        log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
        cloudwatch_alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]] = None,
    ) -> None:
        '''
        :param log_group: The log group that will receive log messages from the state maching.
        :param state_machine: The state machine created by the factory (the state machine role is available as a property on this resource).
        :param cloudwatch_alarms: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161202dcfa7b7271dad8c07356c59eacd279fc41c1b984608b687fc4baf227f5)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
            check_type(argname="argument cloudwatch_alarms", value=cloudwatch_alarms, expected_type=type_hints["cloudwatch_alarms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group": log_group,
            "state_machine": state_machine,
        }
        if cloudwatch_alarms is not None:
            self._values["cloudwatch_alarms"] = cloudwatch_alarms

    @builtins.property
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group that will receive log messages from the state maching.'''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, result)

    @builtins.property
    def state_machine(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine:
        '''The state machine created by the factory (the state machine role is available as a property on this resource).'''
        result = self._values.get("state_machine")
        assert result is not None, "Required property 'state_machine' is missing"
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine, result)

    @builtins.property
    def cloudwatch_alarms(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]]:
        result = self._values.get("cloudwatch_alarms")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineFactoryResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ConstructsFactories",
    "S3BucketFactoryProps",
    "S3BucketFactoryResponse",
    "SqsQueueFactoryProps",
    "SqsQueueFactoryResponse",
    "StateMachineFactoryProps",
    "StateMachineFactoryResponse",
]

publication.publish()

def _typecheckingstub__605983066d245d838df0751ca3d83223b93e3dac7281a9b7677ff8c39ccd96d4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b90bfb94c5304484be85483634a7064b119ae1b0c5ed7cfc594e3e7bbf37f0(
    id: builtins.str,
    *,
    bucket_props: typing.Any = None,
    logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    log_s3_access_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf99c1a76dccb709a8410aeed535e4d0c6fd49506e1e3bb9bd4e95a2dd4648d5(
    id: builtins.str,
    *,
    dead_letter_queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
    enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    encryption_key_props: typing.Optional[typing.Union[_aws_cdk_aws_kms_ceddda9d.KeyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8ce2d58c9a66b894497fcb91691d41649f06370c9e15b72ef1373fbe0d05c6(
    id: builtins.str,
    *,
    state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
    cloud_watch_alarms_prefix: typing.Optional[builtins.str] = None,
    create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a251aca0d0848bcaeaed9669ce040e9bd9f304c875a3796313bd27abcdacc3(
    *,
    bucket_props: typing.Any = None,
    logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    log_s3_access_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e83545e4e90253a16e42d104a9338e2ce2020b20c95b614ea013e7c4918073(
    *,
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
    s3_logging_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357772658c56c210047c7fbddf97a03753fe395062f8ccafa942fbf9b229b6fb(
    *,
    dead_letter_queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
    deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
    enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    encryption_key_props: typing.Optional[typing.Union[_aws_cdk_aws_kms_ceddda9d.KeyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    queue_props: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.QueueProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd81db84d5c3594de6e2da5168709e73ddb24db1d425ea510f2e8891bc71e32(
    *,
    queue: _aws_cdk_aws_sqs_ceddda9d.Queue,
    dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
    key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ef38c5b8793990636642f918f311333d9be77dfc62aec7517d2993d778bdb1(
    *,
    state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
    cloud_watch_alarms_prefix: typing.Optional[builtins.str] = None,
    create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161202dcfa7b7271dad8c07356c59eacd279fc41c1b984608b687fc4baf227f5(
    *,
    log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
    cloudwatch_alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]] = None,
) -> None:
    """Type checking stubs"""
    pass
