r'''
<div align="center">
    <h1> AWS CDK Network Firewall L2 </h1>
This repo holds some experimental L2 constructs for the

[AWS-CDK](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_networkfirewall-readme.html)
<br/>

[![release](https://github.com/durkinza/cdk-networkfirewall-l2/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/durkinza/cdk-networkfirewall-l2/actions/workflows/release.yml)

[![View on Construct Hub](https://constructs.dev/badge?package=%40durkinza%2Fcdk-networkfirewall-l2)](https://constructs.dev/packages/@durkinza/cdk-networkfirewall-l2)

</div>---


## Description

AWS Network Firewall is a stateful, managed, network firewall and intrusion detection and prevention service.
These L2 Constructs can be used to create managed network firewalls with stateful and stateless rules and rule groups.

The goal of these constructs is to provide a way to decouple the creation of firewall rules from their rule groups and reduce the amount of boilerplate code required to define a network firewall.

### Quick Start Examples

For new environments an example that matches the default Security Group rules [can be found here.](docs/example-only-outbound.md)

If you're adding a firewall to an existing environment that does not have an expectation of normal traffic, try the  [non-obtrusive approach here](docs/example-non-obtrusive.md).
This example passively monitors packets to build a baseline of "normal" traffic that can then be used as a reference to build appropriate firewall rules.

### Defaults

The ideal examples shown below provide only the parameters required to create a resource.
Wherever possible, optional parameters are available to give the same level of customization as the L1 API.

To keep the constructs unopinionated, default actions are required for deployment of new resources.
It may be possible to reduce boilerplate code more if default actions were to be defined.
Some examples of possible opinionated approaches:

An unobtrusive logging approach, to promote implementation of network firewalls in existing stacks.

> When a parameter in an L2 construct is optional, where it would normally be required for an L1 construct, an unobtrusive and logging default option would be implied. This allows resources to be implemented in an existing stack with minimal obstruction to the existing operation of the stack.
> After implementing a network firewall with logging defaults in a testing environment, a user can define a standard of "normal traffic" for their environment and implement firewall rules and default actions to restrict traffic.

A more obtrusive, but higher security approach could be:

> When a parameter in an L2 construct is optional, where it would normally be required for an L1 construct, a default drop rule would be implied. This ensures traffic that is not specifically allowed is blocked, a user would need to define rules to allow the traffic that is expected in their environment.

For new policies, it would also be possible to mirror the defaults set for security groups, where a default action of drop is set, with a single stateless rule being set to allow all outbound traffic. This approach would require generating an entire set of Policy, Stateless group, and stateless rule.

In any case a user can overwrite the default action(s) and create their own policies and rules as they see fit.
Given the relatively small amount of code required to define the resources with default actions, I would opt to leave the code unopinionated for the first revision, as defaults can be specified in a later revision if needed.

### Firewalls

An ideal implementation would allow users to create firewall with minimal boiler plate.

```python
const policy = NetFW.FirewallPolicy.fromFirewallPolicyName(stack, 'MyNetworkFirewallPolicy', 'MyFirewallPolicy');
new NetFW.Firewall(stack, 'MyNetworkFirewall', {
  vpc: vpc,
  policy: policy,
});
```

Where the firewall would be created in the provided vpc with the given firewall policy applied.

In this example, `policy` is defined only to meet the requirement that a firewall must have a firewall policy attached.
As explained in the Defaults section above, it may be possible to generate a default policy when one is not provided.

### Firewall Policies

Firewall policy definitions can be done by referencing an existing name/ARN as shown in the last example, or by generating a new policy.
Since a policy does not require rule groups to be attached, it will only need a few requirements to get started.

```python
new NetFW.FirewallPolicy(stack, 'MyNetworkFirewallPolicy', {
  statelessDefaultActions: [NetFW.StatelessStandardAction.DROP],
  statelessFragmentDefaultActions: [NetFW.StatelessStandardAction.DROP],
});
```

Editing an existing Policy (e.x. adding a rule group to an existing policy that has been referenced via ARN) would be out of scope.

When applying rule groups to a policy, a unique priority of must be provided for each group.

```python
const statelessRuleGroupList:NetFW.StatelessRuleGroupList[] = [
  {
    priority: 10,
    ruleGroup: statelessRuleGroup1,
  },
];
const statefulRuleGroupList:NetFW.StatefulRuleGroupList[] = [
  {
    priority: 10,
    ruleGroup: statefulRuleGroup1,
  },
  {
    priority: 20,
    ruleGroup: statefulRuleGroup2,
  },
  {
    priority: 30,
    ruleGroup: statefulRuleGroup3,
  },
];
const policy = new NetFW.FirewallPolicy(stack, 'MyNetworkFirewallPolicy', {
  statelessDefaultActions: [NetFW.StatelessStandardAction.DROP],
  statelessFragmentDefaultActions: [NetFW.StatelessStandardAction.DROP],
  statelessRuleGroups: statelessRuleGroupList,
  statefulRuleGroups: statefulRuleGroupList,
});
```

### Stateless Rule Groups

Stateless firewall rule groups can be defined by referencing an existing name/ARN, or by generating a new group.
New groups don't require any rules to be defined, so their implementation can be fairly quick.

```python
new NetFW.StatelessRuleGroup(stack, 'MyStatelessRuleGroup');
```

The capacity requirements of a stateless rule group is fairly trivial to determine programmatically, but it can't be edited throughout the life time of the rule group. ([ref](https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-group-managing.html#nwfw-rule-group-capacity))
The stateless rule group could programmatically determine the capacity required for the rules assigned to it when no capacity is provided. Using the exact capacity requirements for a rule group by default may cause the user issues later if they decide to add another rule to the group.

Editing an existing rule-group (e.x. adding a rule to an existing group referenced via ARN) would be out of scope.

##### Stateless Rules

Stateless rules are not defined as a resource in AWS, they only exist in the context of the rule group they are defined in.
To allow stateless rules to be decoupled from the rule group throughout the stack, they are defined as their own class, but reduce down to a L1 `RuleDefinitionProperty`

```python
new NetFW.StatelessRule({
  actions: [NetFW.StatelessStandardAction.DROP]
});
```

Assigning stateless rules to a stateless rule-group requires a priority mapping, similar to the way a rule-group requires a priority map when assigned to a policy.

```python
const statelessRule1 = new NetFW.StatelessRule({
  actions: [NetFW.StatelessStandardAction.DROP],
});
const statelessRule2 = new NetFW.StatelessRule({
  actions: [NetFW.StatelessStandardAction.DROP],
});
new NetFW.StatelessRuleGroup(stack, 'MyStatelessRuleGroup', {
  rules: [
    {
      rule: statelessRule1,
      priority: 10,
    },
    {
      rule: statelessRule2,
      priority: 20,
    },
  ],
});
```

### Stateful Rule Groups

Stateful firewall rules are split into 3 categories (5Tuple, Suricata, Domain List).
The console requires the category of rules to be defined when creating the rule group.
However, from my understanding, the L1 constructs reduced all 3 down into Suricata rules. So a single stateful rule group could hold a mix of all 3 types of rules.

It appeared easier to merge the three types in a future revision than to split them apart if the requirements happened to change.
I opted to match the AWS console, giving each rule group category has it's own class. Stateful rule groups are based on the same abstract class, to reduce duplicate code.

Stateful rule groups can be defined with no actionable rules within them, so the minimal implementation would be the same for all of them.

```python
new NetFW.Stateful5TupleRuleGroup(stack, 'MyStateful5TupleRuleGroup', {
  // Assumes the following
  // rules: None
  // ruleOrder: NetFW.StatefulRuleOptions.STRICT_ORDER,
  // capacity: 100
});
new NetFW.StatefulDomainListRuleGroup(stack, 'MyStatefulDomainListRuleGroup', {
  // Assumes the following
  // rule: None
  // ruleOrder: NetFW.StatefulRuleOptions.STRICT_ORDER,
  // capacity: 100
});
new NetFW.StatefulSuricataRuleGroup(stack, 'MyStatefulSuricataRuleGroup', {
  // Assumes the following
  // rules: ""
  // ruleOrder: NetFW.StatefulRuleOptions.STRICT_ORDER,
  // capacity: 100
});
```

##### Stateful 5 Tuple Rules

To define a stateful 5tuple rule, all parameters must be provided to the L1 construct. In most cases the ANY keyword is used to generalize the rule as much as possible by default. Allowing the user to narrow down the rule as needed. A default action must be specified to determine what the rule does when it matches the traffic.

```python
new NetFW.Stateful5TupleRule({
  action: NetFW.StatefulStandardAction.DROP,
  // Assumes the following
  // destination: 'ANY',
  // destinationPort: 'ANY',
  // direction: 'ANY',
  // protocol: 'IP',
  // source: 'ANY',
  // sourcePort: 'ANY',
  // ruleOptions: None
});
```

When adding the stateful 5Tuple rule to a stateful5Tuple rule-group, no priority is required, the ruleOrder assigned to the rule-group will be used.

```python
const stateful5TupleRule1 = new NetFW.Stateful5TupleRule({
  action: NetFW.StatefulStandardAction.DROP,
});
const stateful5TupleRule2 = new NetFW.Stateful5TupleRule({
  action: NetFW.StatefulStandardAction.PASS,
});
new NetFW.Stateful5TupleRuleGroup(stack, 'MyStateful5TupleRuleGroup', {
  capacity: 100,
  rules: [stateful5TupleRule1, stateful5TupleRule2],
});
```

##### Domain List Rules

When defining a Domain List, only a single set of targets can be provided, as set by the L1 construct.
All Domain List specific parameters are required for this rule.

```python
  const statefulDomainListRule = new NetFW.StatefulDomainListRule({
    type: NetFW.StatefulDomainListType.ALLOWLIST,
    targets: ["example.com"],
    targetTypes: [StatefulDomainListTargetType.HTTP_HOST],
  });
```

##### Suricata Rules

Suricata rules are just strings, so they don't have a class type, they are defined directly into the suricata rule-group.

```python
new NetFW.StatefulSuricataRuleGroup(stack, 'MyStatefulSuricataRuleGroup', {
  rules: 'drop tls $HOME_NET any -> $EXTERNAL_NET any (tls.sni; content:"evil.com"; startswith; nocase; endswith; msg:"matching TLS denylisted FQDNs"; priority:1; flow:to_server, established; sid:1; rev:1;)
          drop http $HOME_NET any -> $EXTERNAL_NET any (http.host; content:"evil.com"; startswith; endswith; msg:"matching HTTP denylisted FQDNs"; priority:1; flow:to_server, established; sid:2; rev:1;)'
});
```

Suricata rule groups can also be imported from a file.

```python
const ruleGroup:NetFW.StatefulSuricataRuleGroup = NetFW.StatefulSuricataRuleGroup.fromFile(stack, 'MyStatefulSuricataRuleGroup', {
      path: './suricata.rules'
});
```

All other arguments for creating a Suricata Rule Group are also supported here with an exception of the `rules` property.
The `rules` property will be filled in with the contents from the file path, anything supplied will be ignored.

### Firewall Logs

Logging can be done using 3 AWS services, Cloud Watch trails, S3 buckets, and Kinesis Data Firehose streams.

The logging locations are configured with a Logging type, either Flow or Alert logs.
In the case of Alert logs, it is up to the firewall policy to decide when a log should be generated.

Logs can be configured to be sent to multiple locations simultaneously.

```python
new NetFW.Firewall(stack, 'MyNetworkFirewall', {
  vpc: vpc,
  policy: policy,
  loggingCloudWatchLogGroups: [
    {
      logGroup: logGroup.logGroupName,
      logType: NetFW.LogType.ALERT,
    },
  ],
  loggingS3Buckets: [
    {
      bucketName: s3LoggingBucket.bucketName,
      logType: NetFW.LogType.ALERT,
      prefix: 'alerts',
    },
    {
      bucketName: s3LoggingBucket.bucketName,
      logType: NetFW.LogType.FLOW,
      prefix: 'flow',
    },
  ],
  loggingKinesisDataStreams: [
    {
      deliveryStream: kinesisStream.streamName,
      logType: NetFW.LogType.ALERT,
    }
  ],
});
```
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_networkfirewall as _aws_cdk_aws_networkfirewall_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.FirewallPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "stateless_default_actions": "statelessDefaultActions",
        "stateless_fragment_default_actions": "statelessFragmentDefaultActions",
        "description": "description",
        "firewall_policy_name": "firewallPolicyName",
        "stateful_default_actions": "statefulDefaultActions",
        "stateful_engine_options": "statefulEngineOptions",
        "stateful_rule_groups": "statefulRuleGroups",
        "stateless_custom_actions": "statelessCustomActions",
        "stateless_rule_groups": "statelessRuleGroups",
        "tags": "tags",
        "tls_inspection_configuration": "tlsInspectionConfiguration",
    },
)
class FirewallPolicyProps:
    def __init__(
        self,
        *,
        stateless_default_actions: typing.Sequence[builtins.str],
        stateless_fragment_default_actions: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        firewall_policy_name: typing.Optional[builtins.str] = None,
        stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_rule_groups: typing.Optional[typing.Sequence[typing.Union["StatefulRuleGroupList", typing.Dict[builtins.str, typing.Any]]]] = None,
        stateless_custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        stateless_rule_groups: typing.Optional[typing.Sequence[typing.Union["StatelessRuleGroupList", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
        tls_inspection_configuration: typing.Optional["ITLSInspectionConfiguration"] = None,
    ) -> None:
        '''(experimental) The Properties for defining a Firewall policy.

        :param stateless_default_actions: (experimental) The actions to take on a packet if it doesn't match any of the stateless rules in the policy.
        :param stateless_fragment_default_actions: (experimental) The actions to take on a fragmented packet if it doesn't match any of the stateless rules in the policy.
        :param description: (experimental) The description of the policy. Default: - undefined
        :param firewall_policy_name: (experimental) The descriptive name of the firewall policy. You can't change the name of a firewall policy after you create it. Default: - CloudFormation-generated name
        :param stateful_default_actions: (experimental) The default actions to take on a packet that doesn't match any stateful rules. The stateful default action is optional, and is only valid when using the strict rule order Default: - undefined
        :param stateful_engine_options: (experimental) Additional options governing how Network Firewall handles stateful rules. The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings Default: - undefined
        :param stateful_rule_groups: (experimental) The stateful rule groups that are used in the policy. Default: - undefined
        :param stateless_custom_actions: (experimental) The custom action definitions that are available for use in the firewall policy's statelessDefaultActions setting. Default: - undefined
        :param stateless_rule_groups: (experimental) References to the stateless rule groups that are used in the policy. Default: - undefined
        :param tags: (experimental) Tags to be added to the policy. Default: - No tags applied
        :param tls_inspection_configuration: (experimental) AWS Network Firewall uses a TLS inspection configuration to decrypt traffic. Network Firewall re-encrypts the traffic before sending it to its destination. Default: - No TLS Inspection performed.

        :stability: experimental
        '''
        if isinstance(stateful_engine_options, dict):
            stateful_engine_options = _aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty(**stateful_engine_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2ee17c56a70c25fdc61a7b9804a602c5694964b1af4a38b56f674abcc0045c)
            check_type(argname="argument stateless_default_actions", value=stateless_default_actions, expected_type=type_hints["stateless_default_actions"])
            check_type(argname="argument stateless_fragment_default_actions", value=stateless_fragment_default_actions, expected_type=type_hints["stateless_fragment_default_actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument firewall_policy_name", value=firewall_policy_name, expected_type=type_hints["firewall_policy_name"])
            check_type(argname="argument stateful_default_actions", value=stateful_default_actions, expected_type=type_hints["stateful_default_actions"])
            check_type(argname="argument stateful_engine_options", value=stateful_engine_options, expected_type=type_hints["stateful_engine_options"])
            check_type(argname="argument stateful_rule_groups", value=stateful_rule_groups, expected_type=type_hints["stateful_rule_groups"])
            check_type(argname="argument stateless_custom_actions", value=stateless_custom_actions, expected_type=type_hints["stateless_custom_actions"])
            check_type(argname="argument stateless_rule_groups", value=stateless_rule_groups, expected_type=type_hints["stateless_rule_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_inspection_configuration", value=tls_inspection_configuration, expected_type=type_hints["tls_inspection_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stateless_default_actions": stateless_default_actions,
            "stateless_fragment_default_actions": stateless_fragment_default_actions,
        }
        if description is not None:
            self._values["description"] = description
        if firewall_policy_name is not None:
            self._values["firewall_policy_name"] = firewall_policy_name
        if stateful_default_actions is not None:
            self._values["stateful_default_actions"] = stateful_default_actions
        if stateful_engine_options is not None:
            self._values["stateful_engine_options"] = stateful_engine_options
        if stateful_rule_groups is not None:
            self._values["stateful_rule_groups"] = stateful_rule_groups
        if stateless_custom_actions is not None:
            self._values["stateless_custom_actions"] = stateless_custom_actions
        if stateless_rule_groups is not None:
            self._values["stateless_rule_groups"] = stateless_rule_groups
        if tags is not None:
            self._values["tags"] = tags
        if tls_inspection_configuration is not None:
            self._values["tls_inspection_configuration"] = tls_inspection_configuration

    @builtins.property
    def stateless_default_actions(self) -> typing.List[builtins.str]:
        '''(experimental) The actions to take on a packet if it doesn't match any of the stateless rules in the policy.

        :stability: experimental
        '''
        result = self._values.get("stateless_default_actions")
        assert result is not None, "Required property 'stateless_default_actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def stateless_fragment_default_actions(self) -> typing.List[builtins.str]:
        '''(experimental) The actions to take on a fragmented packet if it doesn't match any of the stateless rules in the policy.

        :stability: experimental
        '''
        result = self._values.get("stateless_fragment_default_actions")
        assert result is not None, "Required property 'stateless_fragment_default_actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the policy.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the firewall policy.

        You can't change the name of a firewall policy after you create it.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("firewall_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stateful_default_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The default actions to take on a packet that doesn't match any stateful rules.

        The stateful default action is optional, and is only valid when using the strict rule order

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("stateful_default_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stateful_engine_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty]:
        '''(experimental) Additional options governing how Network Firewall handles stateful rules.

        The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("stateful_engine_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty], result)

    @builtins.property
    def stateful_rule_groups(
        self,
    ) -> typing.Optional[typing.List["StatefulRuleGroupList"]]:
        '''(experimental) The stateful rule groups that are used in the policy.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("stateful_rule_groups")
        return typing.cast(typing.Optional[typing.List["StatefulRuleGroupList"]], result)

    @builtins.property
    def stateless_custom_actions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty]]:
        '''(experimental) The custom action definitions that are available for use in the firewall policy's statelessDefaultActions setting.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("stateless_custom_actions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty]], result)

    @builtins.property
    def stateless_rule_groups(
        self,
    ) -> typing.Optional[typing.List["StatelessRuleGroupList"]]:
        '''(experimental) References to the stateless rule groups that are used in the policy.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("stateless_rule_groups")
        return typing.cast(typing.Optional[typing.List["StatelessRuleGroupList"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]]:
        '''(experimental) Tags to be added to the policy.

        :default: - No tags applied

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]], result)

    @builtins.property
    def tls_inspection_configuration(
        self,
    ) -> typing.Optional["ITLSInspectionConfiguration"]:
        '''(experimental) AWS Network Firewall uses a TLS inspection configuration to decrypt traffic.

        Network Firewall re-encrypts the traffic before sending it to its destination.

        :default: - No TLS Inspection performed.

        :stability: experimental
        '''
        result = self._values.get("tls_inspection_configuration")
        return typing.cast(typing.Optional["ITLSInspectionConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.FirewallProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "vpc": "vpc",
        "delete_protection": "deleteProtection",
        "description": "description",
        "firewall_name": "firewallName",
        "firewall_policy_change_protection": "firewallPolicyChangeProtection",
        "logging_cloud_watch_log_groups": "loggingCloudWatchLogGroups",
        "logging_kinesis_data_streams": "loggingKinesisDataStreams",
        "logging_s3_buckets": "loggingS3Buckets",
        "subnet_change_protection": "subnetChangeProtection",
        "subnet_mappings": "subnetMappings",
        "tags": "tags",
    },
)
class FirewallProps:
    def __init__(
        self,
        *,
        policy: "IFirewallPolicy",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        delete_protection: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_name: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[builtins.bool] = None,
        logging_cloud_watch_log_groups: typing.Optional[typing.Sequence[typing.Union["CloudWatchLogLocationProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        logging_kinesis_data_streams: typing.Optional[typing.Sequence[typing.Union["KinesisDataFirehoseLogLocationProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        logging_s3_buckets: typing.Optional[typing.Sequence[typing.Union["S3LogLocationProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_change_protection: typing.Optional[builtins.bool] = None,
        subnet_mappings: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''(experimental) The Properties for defining a Firewall Resource.

        :param policy: (experimental) Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.
        :param vpc: (experimental) The unique identifier of the VPC where the firewall is in use. You can't change the VPC of a firewall after you create the firewall.
        :param delete_protection: (experimental) A flag indicating whether it is possible to delete the firewall. A setting of TRUE indicates that the firewall is protected against deletion Default: - true
        :param description: (experimental) The description of the Firewall. Default: - undefined
        :param firewall_name: (experimental) The descriptive name of the firewall. You can't change the name of a firewall after you create it. Default: - CloudFormation-generated name
        :param firewall_policy_change_protection: (experimental) A setting indicating whether the firewall is protected against a change to the firewall policy association. Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. Default: - true
        :param logging_cloud_watch_log_groups: (experimental) A list of CloudWatch LogGroups to send logs to. Default: - Logs will not be sent to a cloudwatch group.
        :param logging_kinesis_data_streams: (experimental) A list of Kinesis Data Firehose to send logs to. Default: - Logs will not be sent to a Kinesis DataFirehose.
        :param logging_s3_buckets: (experimental) A list of S3 Buckets to send logs to. Default: - Logs will not be sent to an S3 bucket.
        :param subnet_change_protection: (experimental) A setting indicating whether the firewall is protected against changes to the subnet associations. Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. Default: - true
        :param subnet_mappings: (experimental) The public subnets that Network Firewall is using for the firewall. Each subnet must belong to a different Availability Zone. Default: - All public subnets of the VPC
        :param tags: (experimental) Tags to be added to the firewall. Default: - No tags applied

        :stability: experimental
        '''
        if isinstance(subnet_mappings, dict):
            subnet_mappings = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_mappings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59cd51c57140520e1402f72c6b992e6b19354a9aa93b962d68d999197e4b7254)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument delete_protection", value=delete_protection, expected_type=type_hints["delete_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument firewall_policy_change_protection", value=firewall_policy_change_protection, expected_type=type_hints["firewall_policy_change_protection"])
            check_type(argname="argument logging_cloud_watch_log_groups", value=logging_cloud_watch_log_groups, expected_type=type_hints["logging_cloud_watch_log_groups"])
            check_type(argname="argument logging_kinesis_data_streams", value=logging_kinesis_data_streams, expected_type=type_hints["logging_kinesis_data_streams"])
            check_type(argname="argument logging_s3_buckets", value=logging_s3_buckets, expected_type=type_hints["logging_s3_buckets"])
            check_type(argname="argument subnet_change_protection", value=subnet_change_protection, expected_type=type_hints["subnet_change_protection"])
            check_type(argname="argument subnet_mappings", value=subnet_mappings, expected_type=type_hints["subnet_mappings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "vpc": vpc,
        }
        if delete_protection is not None:
            self._values["delete_protection"] = delete_protection
        if description is not None:
            self._values["description"] = description
        if firewall_name is not None:
            self._values["firewall_name"] = firewall_name
        if firewall_policy_change_protection is not None:
            self._values["firewall_policy_change_protection"] = firewall_policy_change_protection
        if logging_cloud_watch_log_groups is not None:
            self._values["logging_cloud_watch_log_groups"] = logging_cloud_watch_log_groups
        if logging_kinesis_data_streams is not None:
            self._values["logging_kinesis_data_streams"] = logging_kinesis_data_streams
        if logging_s3_buckets is not None:
            self._values["logging_s3_buckets"] = logging_s3_buckets
        if subnet_change_protection is not None:
            self._values["subnet_change_protection"] = subnet_change_protection
        if subnet_mappings is not None:
            self._values["subnet_mappings"] = subnet_mappings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def policy(self) -> "IFirewallPolicy":
        '''(experimental) Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.

        :stability: experimental
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast("IFirewallPolicy", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The unique identifier of the VPC where the firewall is in use.

        You can't change the VPC of a firewall after you create the firewall.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def delete_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A flag indicating whether it is possible to delete the firewall.

        A setting of TRUE indicates that the firewall is protected against deletion

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("delete_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the Firewall.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the firewall.

        You can't change the name of a firewall after you create it.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("firewall_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_policy_change_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A setting indicating whether the firewall is protected against a change to the firewall policy association.

        Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("firewall_policy_change_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logging_cloud_watch_log_groups(
        self,
    ) -> typing.Optional[typing.List["CloudWatchLogLocationProps"]]:
        '''(experimental) A list of CloudWatch LogGroups to send logs to.

        :default: - Logs will not be sent to a cloudwatch group.

        :stability: experimental
        '''
        result = self._values.get("logging_cloud_watch_log_groups")
        return typing.cast(typing.Optional[typing.List["CloudWatchLogLocationProps"]], result)

    @builtins.property
    def logging_kinesis_data_streams(
        self,
    ) -> typing.Optional[typing.List["KinesisDataFirehoseLogLocationProps"]]:
        '''(experimental) A list of Kinesis Data Firehose to send logs to.

        :default: - Logs will not be sent to a Kinesis DataFirehose.

        :stability: experimental
        '''
        result = self._values.get("logging_kinesis_data_streams")
        return typing.cast(typing.Optional[typing.List["KinesisDataFirehoseLogLocationProps"]], result)

    @builtins.property
    def logging_s3_buckets(self) -> typing.Optional[typing.List["S3LogLocationProps"]]:
        '''(experimental) A list of S3 Buckets to send logs to.

        :default: - Logs will not be sent to an S3 bucket.

        :stability: experimental
        '''
        result = self._values.get("logging_s3_buckets")
        return typing.cast(typing.Optional[typing.List["S3LogLocationProps"]], result)

    @builtins.property
    def subnet_change_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A setting indicating whether the firewall is protected against changes to the subnet associations.

        Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("subnet_change_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet_mappings(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The public subnets that Network Firewall is using for the firewall.

        Each subnet must belong to a different Availability Zone.

        :default: - All public subnets of the VPC

        :stability: experimental
        '''
        result = self._values.get("subnet_mappings")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]]:
        '''(experimental) Tags to be added to the firewall.

        :default: - No tags applied

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.IFirewall")
class IFirewall(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Defines a Network Firewall in the stack.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="firewallArn")
    def firewall_arn(self) -> builtins.str:
        '''(experimental) The Arn of the Firewall.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="firewallId")
    def firewall_id(self) -> builtins.str:
        '''(experimental) The physical name of the Firewall.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IFirewallProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Defines a Network Firewall in the stack.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.IFirewall"

    @builtins.property
    @jsii.member(jsii_name="firewallArn")
    def firewall_arn(self) -> builtins.str:
        '''(experimental) The Arn of the Firewall.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallId")
    def firewall_id(self) -> builtins.str:
        '''(experimental) The physical name of the Firewall.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFirewall).__jsii_proxy_class__ = lambda : _IFirewallProxy


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.IFirewallPolicy")
class IFirewallPolicy(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Defines a Network Firewall Policy in the stack.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyArn")
    def firewall_policy_arn(self) -> builtins.str:
        '''(experimental) The Arn of the policy.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> builtins.str:
        '''(experimental) The physical name of the firewall policy.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IFirewallPolicyProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Defines a Network Firewall Policy in the stack.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.IFirewallPolicy"

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyArn")
    def firewall_policy_arn(self) -> builtins.str:
        '''(experimental) The Arn of the policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> builtins.str:
        '''(experimental) The physical name of the firewall policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFirewallPolicy).__jsii_proxy_class__ = lambda : _IFirewallPolicyProxy


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.ILogLocation")
class ILogLocation(typing_extensions.Protocol):
    '''(experimental) Defines a Log Location in the Stack.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logDestinationType")
    def log_destination_type(self) -> builtins.str:
        '''(experimental) The type of storage destination to send these logs to.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        ...


class _ILogLocationProxy:
    '''(experimental) Defines a Log Location in the Stack.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.ILogLocation"

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logDestination"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationType")
    def log_destination_type(self) -> builtins.str:
        '''(experimental) The type of storage destination to send these logs to.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logDestinationType"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogLocation).__jsii_proxy_class__ = lambda : _ILogLocationProxy


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.ILoggingConfiguration")
class ILoggingConfiguration(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Defines a Network Firewall Logging Configuration in the stack.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="firewallRef")
    def firewall_ref(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the Firewall that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ILoggingConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Defines a Network Firewall Logging Configuration in the stack.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.ILoggingConfiguration"

    @builtins.property
    @jsii.member(jsii_name="firewallRef")
    def firewall_ref(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the Firewall that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILoggingConfiguration).__jsii_proxy_class__ = lambda : _ILoggingConfigurationProxy


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.IStatefulRule")
class IStatefulRule(typing_extensions.Protocol):
    '''(experimental) The interface that represents the shared values of the StatefulRules.

    :stability: experimental
    '''

    pass


class _IStatefulRuleProxy:
    '''(experimental) The interface that represents the shared values of the StatefulRules.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.IStatefulRule"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStatefulRule).__jsii_proxy_class__ = lambda : _IStatefulRuleProxy


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.IStatefulRuleGroup")
class IStatefulRuleGroup(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) The Interface that represents a Stateful Rule Group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IStatefulRuleGroupProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) The Interface that represents a Stateful Rule Group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.IStatefulRuleGroup"

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStatefulRuleGroup).__jsii_proxy_class__ = lambda : _IStatefulRuleGroupProxy


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.IStatelessRule")
class IStatelessRule(typing_extensions.Protocol):
    '''(experimental) The interface that represents the values of a StatelessRule.

    :stability: experimental
    '''

    pass


class _IStatelessRuleProxy:
    '''(experimental) The interface that represents the values of a StatelessRule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.IStatelessRule"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStatelessRule).__jsii_proxy_class__ = lambda : _IStatelessRuleProxy


@jsii.interface(jsii_type="@durkinza/cdk-networkfirewall-l2.IStatelessRuleGroup")
class IStatelessRuleGroup(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Defines a Stateless rule Group in the stack.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IStatelessRuleGroupProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Defines a Stateless rule Group in the stack.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.IStatelessRuleGroup"

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStatelessRuleGroup).__jsii_proxy_class__ = lambda : _IStatelessRuleGroupProxy


@jsii.interface(
    jsii_type="@durkinza/cdk-networkfirewall-l2.ITLSInspectionConfiguration"
)
class ITLSInspectionConfiguration(
    _aws_cdk_ceddda9d.IResource,
    typing_extensions.Protocol,
):
    '''(experimental) Defines a TLS Inspection Configuration Resource in the stack.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="tlsInspectionConfigurationArn")
    def tls_inspection_configuration_arn(self) -> builtins.str:
        '''(experimental) The Arn of the TLS Inspection Configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tlsInspectionConfigurationId")
    def tls_inspection_configuration_id(self) -> builtins.str:
        '''(experimental) The name of the TLS Inspection Configuration.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ITLSInspectionConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Defines a TLS Inspection Configuration Resource in the stack.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@durkinza/cdk-networkfirewall-l2.ITLSInspectionConfiguration"

    @builtins.property
    @jsii.member(jsii_name="tlsInspectionConfigurationArn")
    def tls_inspection_configuration_arn(self) -> builtins.str:
        '''(experimental) The Arn of the TLS Inspection Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tlsInspectionConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="tlsInspectionConfigurationId")
    def tls_inspection_configuration_id(self) -> builtins.str:
        '''(experimental) The name of the TLS Inspection Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tlsInspectionConfigurationId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITLSInspectionConfiguration).__jsii_proxy_class__ = lambda : _ITLSInspectionConfigurationProxy


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.LogDestinationType")
class LogDestinationType(enum.Enum):
    '''(experimental) The type of storage destination to send these logs to.

    :stability: experimental
    '''

    CLOUDWATCH = "CLOUDWATCH"
    '''(experimental) Store logs to CloudWatch log group.

    :stability: experimental
    '''
    KINESISDATAFIREHOSE = "KINESISDATAFIREHOSE"
    '''(experimental) Store logs to a Kinesis Data Firehose delivery stream.

    :stability: experimental
    '''
    S3 = "S3"
    '''(experimental) Store logs to an S3 bucket.

    :stability: experimental
    '''


@jsii.implements(ILogLocation)
class LogLocationBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@durkinza/cdk-networkfirewall-l2.LogLocationBase",
):
    '''(experimental) Base Log Location class.

    :stability: experimental
    '''

    def __init__(
        self,
        log_destination_type: LogDestinationType,
        *,
        log_type: builtins.str,
    ) -> None:
        '''
        :param log_destination_type: The type of storage destination to send these logs to.
        :param log_type: (experimental) The type of log to send.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c969855b1e57c3f77f7527e0b14ed1a48e2993dab44eeebb2e88de6d3f8e54)
            check_type(argname="argument log_destination_type", value=log_destination_type, expected_type=type_hints["log_destination_type"])
        props = LogLocationProps(log_type=log_type)

        jsii.create(self.__class__, self, [log_destination_type, props])

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    @abc.abstractmethod
    def log_destination(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logDestinationType")
    def log_destination_type(self) -> builtins.str:
        '''(experimental) The type of storage destination to send these logs to.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logDestinationType"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logType"))


class _LogLocationBaseProxy(LogLocationBase):
    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logDestination"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LogLocationBase).__jsii_proxy_class__ = lambda : _LogLocationBaseProxy


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.LogLocationProps",
    jsii_struct_bases=[],
    name_mapping={"log_type": "logType"},
)
class LogLocationProps:
    def __init__(self, *, log_type: builtins.str) -> None:
        '''(experimental) Base Log Location structure.

        :param log_type: (experimental) The type of log to send.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c324b8a677fd1a0df70aa85bccc3288338dafbb97c5c8a1e5d46116b7ad474dc)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_type": log_type,
        }

    @builtins.property
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        result = self._values.get("log_type")
        assert result is not None, "Required property 'log_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogLocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.LogType")
class LogType(enum.Enum):
    '''(experimental) The type of log to send.

    :stability: experimental
    '''

    ALERT = "ALERT"
    '''(experimental) Alert logs report traffic that matches a stateful rule with an action setting that sends an alert log message.

    :stability: experimental
    '''
    FLOW = "FLOW"
    '''(experimental) Flow logs are standard network traffic flow logs.

    :stability: experimental
    '''


@jsii.implements(ILoggingConfiguration)
class LoggingConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.LoggingConfiguration",
):
    '''(experimental) Defines a Logging Configuration in the Stack.

    :stability: experimental
    :resource: AWS::NetworkFirewall::LoggingConfiguration
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        firewall_ref: builtins.str,
        firewall_name: typing.Optional[builtins.str] = None,
        logging_configuration_name: typing.Optional[builtins.str] = None,
        logging_locations: typing.Optional[typing.Sequence[ILogLocation]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param firewall_ref: (experimental) The Amazon Resource Name (ARN) of the Firewall that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.
        :param firewall_name: (experimental) The name of the firewall that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration. Default: - No firewall name is logged.
        :param logging_configuration_name: (experimental) The physical name of this logging configuration. Default: - CloudFormation-generated name
        :param logging_locations: (experimental) Defines how AWS Network Firewall performs logging for a Firewall. Default: - No logging locations are configured, no logs will be sent.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46589e30dbca05715df2fc8b312a6a7078e3918ff0acdefb719f2765a73f011d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LoggingConfigurationProps(
            firewall_ref=firewall_ref,
            firewall_name=firewall_name,
            logging_configuration_name=logging_configuration_name,
            logging_locations=logging_locations,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="iLogLocationsToLogDestinationConfigProperty")
    def i_log_locations_to_log_destination_config_property(
        self,
        log_locations: typing.Sequence[ILogLocation],
    ) -> typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnLoggingConfiguration.LogDestinationConfigProperty]:
        '''(experimental) Convert ILogLocation array to L1 LogDestinationConfigProperty array.

        :param log_locations: An array of assorted Log Locations.

        :return: Array of LogDestinationConfigProperty objects.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bfa58d0b28a9fff7797847dc6fb8f8da707b707cdba55022ad68325bfc0ee2)
            check_type(argname="argument log_locations", value=log_locations, expected_type=type_hints["log_locations"])
        return typing.cast(typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnLoggingConfiguration.LogDestinationConfigProperty], jsii.invoke(self, "iLogLocationsToLogDestinationConfigProperty", [log_locations]))

    @builtins.property
    @jsii.member(jsii_name="firewallRef")
    def firewall_ref(self) -> builtins.str:
        '''(experimental) The associated firewall Arn.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRef"))

    @builtins.property
    @jsii.member(jsii_name="firewallName")
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The associated firewall Name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallName"))

    @builtins.property
    @jsii.member(jsii_name="loggingLocations")
    def logging_locations(self) -> typing.List[ILogLocation]:
        '''(experimental) Defines how AWS Network Firewall performs logging for a Firewall.

        :stability: experimental
        '''
        return typing.cast(typing.List[ILogLocation], jsii.get(self, "loggingLocations"))

    @logging_locations.setter
    def logging_locations(self, value: typing.List[ILogLocation]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b335d6947dc4cfacd2dbc21b6a86d3fe52f4eeef15eb5e262fec2272bde663bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingLocations", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.LoggingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_ref": "firewallRef",
        "firewall_name": "firewallName",
        "logging_configuration_name": "loggingConfigurationName",
        "logging_locations": "loggingLocations",
    },
)
class LoggingConfigurationProps:
    def __init__(
        self,
        *,
        firewall_ref: builtins.str,
        firewall_name: typing.Optional[builtins.str] = None,
        logging_configuration_name: typing.Optional[builtins.str] = None,
        logging_locations: typing.Optional[typing.Sequence[ILogLocation]] = None,
    ) -> None:
        '''(experimental) The Properties for defining a Logging Configuration.

        :param firewall_ref: (experimental) The Amazon Resource Name (ARN) of the Firewall that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.
        :param firewall_name: (experimental) The name of the firewall that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration. Default: - No firewall name is logged.
        :param logging_configuration_name: (experimental) The physical name of this logging configuration. Default: - CloudFormation-generated name
        :param logging_locations: (experimental) Defines how AWS Network Firewall performs logging for a Firewall. Default: - No logging locations are configured, no logs will be sent.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df75dcff12eb45788a994841d82b6f8af893265985ff4b0cfa0365464c84841)
            check_type(argname="argument firewall_ref", value=firewall_ref, expected_type=type_hints["firewall_ref"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument logging_configuration_name", value=logging_configuration_name, expected_type=type_hints["logging_configuration_name"])
            check_type(argname="argument logging_locations", value=logging_locations, expected_type=type_hints["logging_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_ref": firewall_ref,
        }
        if firewall_name is not None:
            self._values["firewall_name"] = firewall_name
        if logging_configuration_name is not None:
            self._values["logging_configuration_name"] = logging_configuration_name
        if logging_locations is not None:
            self._values["logging_locations"] = logging_locations

    @builtins.property
    def firewall_ref(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the Firewall that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :stability: experimental
        '''
        result = self._values.get("firewall_ref")
        assert result is not None, "Required property 'firewall_ref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the firewall that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :default: - No firewall name is logged.

        :stability: experimental
        '''
        result = self._values.get("firewall_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical name of this logging configuration.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("logging_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_locations(self) -> typing.Optional[typing.List[ILogLocation]]:
        '''(experimental) Defines how AWS Network Firewall performs logging for a Firewall.

        :default: - No logging locations are configured, no logs will be sent.

        :stability: experimental
        '''
        result = self._values.get("logging_locations")
        return typing.cast(typing.Optional[typing.List[ILogLocation]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3LogLocation(
    LogLocationBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.S3LogLocation",
):
    '''(experimental) Defines a S3 Bucket Logging configuration.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
        log_type: builtins.str,
    ) -> None:
        '''
        :param bucket_name: (experimental) The name of the S3 bucket to send logs to.
        :param prefix: (experimental) The location prefix to use. Default: - no prefix is used.
        :param log_type: (experimental) The type of log to send.

        :stability: experimental
        '''
        props = S3LogLocationProps(
            bucket_name=bucket_name, prefix=prefix, log_type=log_type
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logDestination"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationType")
    def log_destination_type(self) -> builtins.str:
        '''(experimental) The type of storage destination to send these logs to.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logDestinationType"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.S3LogLocationProps",
    jsii_struct_bases=[LogLocationProps],
    name_mapping={
        "log_type": "logType",
        "bucket_name": "bucketName",
        "prefix": "prefix",
    },
)
class S3LogLocationProps(LogLocationProps):
    def __init__(
        self,
        *,
        log_type: builtins.str,
        bucket_name: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Defines a S3 Bucket Logging Option.

        :param log_type: (experimental) The type of log to send.
        :param bucket_name: (experimental) The name of the S3 bucket to send logs to.
        :param prefix: (experimental) The location prefix to use. Default: - no prefix is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9566111f1fea55135e7160f79ac8189860c019719e48087c2e8a661188b9c34e)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_type": log_type,
            "bucket_name": bucket_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        result = self._values.get("log_type")
        assert result is not None, "Required property 'log_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''(experimental) The name of the S3 bucket to send logs to.

        :stability: experimental
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The location prefix to use.

        :default: - no prefix is used.

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3LogLocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.Stateful5TupleDirection")
class Stateful5TupleDirection(enum.Enum):
    '''(experimental) The direction of traffic flow to inspect.

    :stability: experimental
    '''

    ANY = "ANY"
    '''(experimental) Inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source.

    :stability: experimental
    '''
    FORWARD = "FORWARD"
    '''(experimental) Inspection only matches traffic going from the source to the destination.

    :stability: experimental
    '''


@jsii.implements(IStatefulRuleGroup)
class Stateful5TupleRuleGroup(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.Stateful5TupleRuleGroup",
):
    '''(experimental) A Stateful Rule group that holds 5Tuple Rules.

    :stability: experimental
    :resource: AWS::NetworkFirewall::RuleGroup
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional["StatefulRuleOptions"] = None,
        rules: typing.Optional[typing.Sequence["Stateful5TupleRule"]] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param rules: (experimental) The rule group rules. Default: - undefined
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d354536559ae5c79502835ce91ecd498376a49e28c0e94909bd1effd716162)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Stateful5TupleRuleGroupProps(
            capacity=capacity,
            description=description,
            rule_group_name=rule_group_name,
            rule_order=rule_order,
            rules=rules,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRuleGroupArn")
    @builtins.classmethod
    def from_rule_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        rule_group_arn: builtins.str,
    ) -> IStatefulRuleGroup:
        '''(experimental) Reference existing Rule Group.

        :param scope: -
        :param id: -
        :param rule_group_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30506ba2b8c70f0a197eb50472e01c9f595c8f0b8d054be707786bc72bb51b50)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule_group_arn", value=rule_group_arn, expected_type=type_hints["rule_group_arn"])
        return typing.cast(IStatefulRuleGroup, jsii.sinvoke(cls, "fromRuleGroupArn", [scope, id, rule_group_arn]))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupId"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.Stateful5TupleRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "description": "description",
        "rule_group_name": "ruleGroupName",
        "rule_order": "ruleOrder",
        "rules": "rules",
        "variables": "variables",
    },
)
class Stateful5TupleRuleGroupProps:
    def __init__(
        self,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional["StatefulRuleOptions"] = None,
        rules: typing.Optional[typing.Sequence["Stateful5TupleRule"]] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for defining a Stateful 5 Tuple Rule Group.

        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param rules: (experimental) The rule group rules. Default: - undefined
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        :resource: AWS::NetworkFIrewall::RuleGroup
        '''
        if isinstance(variables, dict):
            variables = _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty(**variables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b471389c990532ca98eadf99cec5936497f7ba575edbae7a6229b11feddbedb)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if description is not None:
            self._values["description"] = description
        if rule_group_name is not None:
            self._values["rule_group_name"] = rule_group_name
        if rule_order is not None:
            self._values["rule_order"] = rule_order
        if rules is not None:
            self._values["rules"] = rules
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum operating resources that this rule group can use.

        Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime.
        You can't change this setting after you create the rule group

        :default: - 200

        :stability: experimental
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the rule group.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the stateful rule group.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("rule_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_order(self) -> typing.Optional["StatefulRuleOptions"]:
        '''(experimental) Rule Order.

        :default: - STRICT_ORDER

        :stability: experimental
        '''
        result = self._values.get("rule_order")
        return typing.cast(typing.Optional["StatefulRuleOptions"], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["Stateful5TupleRule"]]:
        '''(experimental) The rule group rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["Stateful5TupleRule"]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty]:
        '''(experimental) Settings that are available for use in the rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Stateful5TupleRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IStatefulRuleGroup)
class StatefulDomainListRuleGroup(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulDomainListRuleGroup",
):
    '''(experimental) A Stateful Rule group that holds Domain List Rules.

    :stability: experimental
    :resource: AWS::NetworkFirewall::RuleGroup
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        rule: typing.Optional["StatefulDomainListRule"] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional["StatefulRuleOptions"] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule: (experimental) The Domain List rule. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db8aa1719bfb18562efe72ca2175431fe159270f8397b8caf3cb1b533448c70)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StatefulDomainListRuleGroupProps(
            capacity=capacity,
            description=description,
            rule=rule,
            rule_group_name=rule_group_name,
            rule_order=rule_order,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRuleGroupArn")
    @builtins.classmethod
    def from_rule_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        rule_group_arn: builtins.str,
    ) -> IStatefulRuleGroup:
        '''(experimental) Reference existing Rule Group.

        :param scope: -
        :param id: -
        :param rule_group_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e95866eb2f5a18a22c37d81b4688a24e2b74dde351e03c6e7ee5e66fff16746)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule_group_arn", value=rule_group_arn, expected_type=type_hints["rule_group_arn"])
        return typing.cast(IStatefulRuleGroup, jsii.sinvoke(cls, "fromRuleGroupArn", [scope, id, rule_group_arn]))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupId"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulDomainListRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "description": "description",
        "rule": "rule",
        "rule_group_name": "ruleGroupName",
        "rule_order": "ruleOrder",
        "variables": "variables",
    },
)
class StatefulDomainListRuleGroupProps:
    def __init__(
        self,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        rule: typing.Optional["StatefulDomainListRule"] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional["StatefulRuleOptions"] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Defines a Stateful Domain List Rule group in the stack.

        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule: (experimental) The Domain List rule. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        :resource: AWS::NetworkFIrewall::RuleGroup
        '''
        if isinstance(variables, dict):
            variables = _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty(**variables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475ae631eb0efaeba527029eed7ee37a29cb2729e0d5cc6b0cb753ae8e3021e4)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if description is not None:
            self._values["description"] = description
        if rule is not None:
            self._values["rule"] = rule
        if rule_group_name is not None:
            self._values["rule_group_name"] = rule_group_name
        if rule_order is not None:
            self._values["rule_order"] = rule_order
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum operating resources that this rule group can use.

        Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime.
        You can't change this setting after you create the rule group

        :default: - 200

        :stability: experimental
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the rule group.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule(self) -> typing.Optional["StatefulDomainListRule"]:
        '''(experimental) The Domain List rule.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional["StatefulDomainListRule"], result)

    @builtins.property
    def rule_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the stateful rule group.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("rule_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_order(self) -> typing.Optional["StatefulRuleOptions"]:
        '''(experimental) Rule Order.

        :default: - STRICT_ORDER

        :stability: experimental
        '''
        result = self._values.get("rule_order")
        return typing.cast(typing.Optional["StatefulRuleOptions"], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty]:
        '''(experimental) Settings that are available for use in the rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatefulDomainListRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulDomainListTargetType")
class StatefulDomainListTargetType(enum.Enum):
    '''(experimental) The types of targets to inspect for.

    You can inspect HTTP or HTTPS protocols, or both.

    :stability: experimental
    '''

    TLS_SNI = "TLS_SNI"
    '''(experimental) Target HTTPS traffic For HTTPS traffic, Network Firewall uses the Server Name Indication (SNI) extension in the TLS handshake to determine the hostname, or domain name, that the client is trying to connect to.

    :stability: experimental
    '''
    HTTP_HOST = "HTTP_HOST"
    '''(experimental) Target HTTP traffic.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulDomainListType")
class StatefulDomainListType(enum.Enum):
    '''(experimental) The type of domain list to generate.

    :stability: experimental
    '''

    DENYLIST = "DENYLIST"
    '''(experimental) Deny domain(s) through.

    :stability: experimental
    '''
    ALLOWLIST = "ALLOWLIST"
    '''(experimental) Allow domain(s) through.

    :stability: experimental
    '''


@jsii.implements(IStatefulRule)
class StatefulRuleBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulRuleBase",
):
    '''(experimental) The shared base class of stateful rules.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])


class _StatefulRuleBaseProxy(StatefulRuleBase):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, StatefulRuleBase).__jsii_proxy_class__ = lambda : _StatefulRuleBaseProxy


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulRuleBaseProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class StatefulRuleBaseProps:
    def __init__(self) -> None:
        '''(experimental) The properties for defining a generic Stateful Rule.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatefulRuleBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulRuleGroupList",
    jsii_struct_bases=[],
    name_mapping={"rule_group": "ruleGroup", "priority": "priority"},
)
class StatefulRuleGroupList:
    def __init__(
        self,
        *,
        rule_group: IStatefulRuleGroup,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Maps a priority to a stateful rule group item.

        :param rule_group: (experimental) The stateful rule group.
        :param priority: (experimental) The priority of the rule group in the policy. Default: - Priority is only used when Strict order is set.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ec66b096d7b56fc7112f4faa1a444073f7bb1ca04c40a908646a9c3d662c69)
            check_type(argname="argument rule_group", value=rule_group, expected_type=type_hints["rule_group"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_group": rule_group,
        }
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def rule_group(self) -> IStatefulRuleGroup:
        '''(experimental) The stateful rule group.

        :stability: experimental
        '''
        result = self._values.get("rule_group")
        assert result is not None, "Required property 'rule_group' is missing"
        return typing.cast(IStatefulRuleGroup, result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of the rule group in the policy.

        :default: - Priority is only used when Strict order is set.

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatefulRuleGroupList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulRuleOptions")
class StatefulRuleOptions(enum.Enum):
    '''(experimental) Indicates how to manage the order of the rule evaluation for the rule group.

    :stability: experimental
    '''

    ACTION_ORDER = "ACTION_ORDER"
    '''(experimental) Rules with a pass action are processed first, followed by drop, reject, and alert actions.

    This option was previously named Default Acton Order.

    :stability: experimental
    '''
    STRICT_ORDER = "STRICT_ORDER"
    '''(experimental) With strict ordering, the rule groups are evaluated by order of priority, starting from the lowest number, and the rules in each rule group are processed in the order in which they're defined.

    Recommended Order

    :stability: experimental
    '''


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulStandardAction")
class StatefulStandardAction(enum.Enum):
    '''(experimental) Defines what Network Firewall should do with the packets in a traffic flow when the flow matches the stateful rule criteria.

    :stability: experimental
    '''

    PASS = "PASS"
    '''(experimental) Permits the packets to go to the intended destination.

    :stability: experimental
    '''
    DROP = "DROP"
    '''(experimental) Blocks the packets from going to the intended destination and sends an alert log message, if alert logging is configured in the firewall.

    :stability: experimental
    '''
    ALERT = "ALERT"
    '''(experimental) Permits the packets to go to the intended destination and sends an alert log message, if alert logging is configured in the firewall.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulStrictAction")
class StatefulStrictAction(enum.Enum):
    '''(experimental) The default actions to take on a packet that doesn't match any stateful rules.

    :stability: experimental
    '''

    DROP_STRICT = "DROP_STRICT"
    '''(experimental) Drops all packets.

    :stability: experimental
    '''
    DROP_ESTABLISHED = "DROP_ESTABLISHED"
    '''(experimental) Drops only the packets that are in established connections.

    This allows the layer 3 and 4 connection establishment packets that are needed for the upper-layer connections to be established, while dropping the packets for connections that are already established.
    This allows application-layer pass rules to be written in a default-deny setup without the need to write additional rules to allow the lower-layer handshaking parts of the underlying protocols.

    :stability: experimental
    '''
    ALERT_STRICT = "ALERT_STRICT"
    '''(experimental) Logs an ALERT message on all packets.

    This does not drop packets, but alerts you to what would be dropped if you were to choose Drop all.

    :stability: experimental
    '''
    ALERT_ESTABLISHED = "ALERT_ESTABLISHED"
    '''(experimental) Logs an ALERT message on only the packets that are in established connections.

    This does not drop packets, but alerts you to what would be dropped if you were to choose Drop established.

    :stability: experimental
    '''


@jsii.implements(IStatefulRuleGroup)
class StatefulSuricataRuleGroup(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulSuricataRuleGroup",
):
    '''(experimental) A Stateful Rule group that holds Suricata Rules.

    :stability: experimental
    :resource: AWS::NetworkFirewall::RuleGroup
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional[StatefulRuleOptions] = None,
        rules: typing.Optional[builtins.str] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param rules: (experimental) The suricata rules. Default: - undefined
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a4572db82842b82805cb8495f44d81c4ea72914aa229b47b87c39baeab428d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StatefulSuricataRuleGroupProps(
            capacity=capacity,
            description=description,
            rule_group_name=rule_group_name,
            rule_order=rule_order,
            rules=rules,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional[StatefulRuleOptions] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "StatefulSuricataRuleGroup":
        '''(experimental) Reference Suricata rules from a file,.

        :param scope: -
        :param id: -
        :param path: (experimental) The suricata rules file location.
        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param encoding: (experimental) The encoding to use for the file. Default: - uft-8
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        :resource: AWS::NetworkFirewall::RuleGroup
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2afaa1480e87fa8bd625ff6985dfad168d9ba6d1e13e0c84d0cc9efb78668da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StatefulSuricataRuleGroupFromFileProps(
            path=path,
            capacity=capacity,
            description=description,
            encoding=encoding,
            rule_group_name=rule_group_name,
            rule_order=rule_order,
            variables=variables,
        )

        return typing.cast("StatefulSuricataRuleGroup", jsii.sinvoke(cls, "fromFile", [scope, id, props]))

    @jsii.member(jsii_name="fromRuleGroupArn")
    @builtins.classmethod
    def from_rule_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        rule_group_arn: builtins.str,
    ) -> IStatefulRuleGroup:
        '''(experimental) Reference existing Rule Group.

        :param scope: -
        :param id: -
        :param rule_group_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d4ceba10ad19d785444a5cefc47ebfc90a8d5bbf5d7818f8be4cb15ce8d56e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule_group_arn", value=rule_group_arn, expected_type=type_hints["rule_group_arn"])
        return typing.cast(IStatefulRuleGroup, jsii.sinvoke(cls, "fromRuleGroupArn", [scope, id, rule_group_arn]))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupId"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulSuricataRuleGroupFromFileProps",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "capacity": "capacity",
        "description": "description",
        "encoding": "encoding",
        "rule_group_name": "ruleGroupName",
        "rule_order": "ruleOrder",
        "variables": "variables",
    },
)
class StatefulSuricataRuleGroupFromFileProps:
    def __init__(
        self,
        *,
        path: builtins.str,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional[StatefulRuleOptions] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for defining a Stateful Suricata Rule Group from a file.

        :param path: (experimental) The suricata rules file location.
        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param encoding: (experimental) The encoding to use for the file. Default: - uft-8
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        :resource: AWS::NetworkFIrewall::RuleGroup
        '''
        if isinstance(variables, dict):
            variables = _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty(**variables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5485a09476759c5e75fb7cce8b3bd4b9889793dfe6d19aea78857a4938935089)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if capacity is not None:
            self._values["capacity"] = capacity
        if description is not None:
            self._values["description"] = description
        if encoding is not None:
            self._values["encoding"] = encoding
        if rule_group_name is not None:
            self._values["rule_group_name"] = rule_group_name
        if rule_order is not None:
            self._values["rule_order"] = rule_order
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) The suricata rules file location.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum operating resources that this rule group can use.

        Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime.
        You can't change this setting after you create the rule group

        :default: - 200

        :stability: experimental
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the rule group.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''(experimental) The encoding to use for the file.

        :default: - uft-8

        :stability: experimental
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the stateful rule group.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("rule_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_order(self) -> typing.Optional[StatefulRuleOptions]:
        '''(experimental) Rule Order.

        :default: - STRICT_ORDER

        :stability: experimental
        '''
        result = self._values.get("rule_order")
        return typing.cast(typing.Optional[StatefulRuleOptions], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty]:
        '''(experimental) Settings that are available for use in the rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatefulSuricataRuleGroupFromFileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulSuricataRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "description": "description",
        "rule_group_name": "ruleGroupName",
        "rule_order": "ruleOrder",
        "rules": "rules",
        "variables": "variables",
    },
)
class StatefulSuricataRuleGroupProps:
    def __init__(
        self,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional[StatefulRuleOptions] = None,
        rules: typing.Optional[builtins.str] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for defining a Stateful Suricata Rule Group.

        :param capacity: (experimental) The maximum operating resources that this rule group can use. Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime. You can't change this setting after you create the rule group Default: - 200
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateful rule group. Default: - CloudFormation-generated name
        :param rule_order: (experimental) Rule Order. Default: - STRICT_ORDER
        :param rules: (experimental) The suricata rules. Default: - undefined
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        :resource: AWS::NetworkFIrewall::RuleGroup
        '''
        if isinstance(variables, dict):
            variables = _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty(**variables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23856d3a152b06d39d4ba08d112a04dc652a95ac2d69d1f1ad6f54049b658a18)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if description is not None:
            self._values["description"] = description
        if rule_group_name is not None:
            self._values["rule_group_name"] = rule_group_name
        if rule_order is not None:
            self._values["rule_order"] = rule_order
        if rules is not None:
            self._values["rules"] = rules
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum operating resources that this rule group can use.

        Estimate a stateful rule group's capacity as the number of rules that you expect to have in it during its lifetime.
        You can't change this setting after you create the rule group

        :default: - 200

        :stability: experimental
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the rule group.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the stateful rule group.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("rule_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_order(self) -> typing.Optional[StatefulRuleOptions]:
        '''(experimental) Rule Order.

        :default: - STRICT_ORDER

        :stability: experimental
        '''
        result = self._values.get("rule_order")
        return typing.cast(typing.Optional[StatefulRuleOptions], result)

    @builtins.property
    def rules(self) -> typing.Optional[builtins.str]:
        '''(experimental) The suricata rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty]:
        '''(experimental) Settings that are available for use in the rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatefulSuricataRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IStatelessRule)
class StatelessRule(
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatelessRule",
):
    '''(experimental) Defines a Network Firewall Stateless Rule.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        destination_ports: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
        source_ports: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_flags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param actions: (experimental) Rule Actions. The actions to take on a packet that matches one of the stateless rule definition's match attributes.
        :param destination_ports: (experimental) The destination port to inspect for. You can specify an individual port, for example 1994 and you can specify a port range, for example 1990:1994. To match with any port, specify ANY. Default: - ANY
        :param destinations: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: - ANY
        :param protocols: (experimental) The protocols to inspect for, specified using each protocol's assigned internet protocol number (IANA). Default: - ANY
        :param source_ports: (experimental) The source ports to inspect for. Default: - ANY
        :param sources: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: - ANY
        :param tcp_flags: (experimental) TCP flags and masks to inspect packets for. Default: - undefined

        :stability: experimental
        '''
        props = StatelessRuleProps(
            actions=actions,
            destination_ports=destination_ports,
            destinations=destinations,
            protocols=protocols,
            source_ports=source_ports,
            sources=sources,
            tcp_flags=tcp_flags,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="calculateCapacity")
    def calculate_capacity(self) -> jsii.Number:
        '''(experimental) Calculate Rule Capacity Requirements.

        https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-group-managing.html#nwfw-rule-group-capacity

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "calculateCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(
        self,
    ) -> _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleDefinitionProperty:
        '''(experimental) The L1 Stateless Rule Property.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleDefinitionProperty, jsii.get(self, "resource"))

    @resource.setter
    def resource(
        self,
        value: _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleDefinitionProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0feb55e3ca55cf06df0c3dac06774dff4ba0ca73f349bb1a212206dd088ed1fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]


@jsii.implements(IStatelessRuleGroup)
class StatelessRuleGroup(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatelessRuleGroup",
):
    '''(experimental) A Stateless Rule group that holds Stateless Rules.

    :stability: experimental
    :resource: AWS::NetworkFirewall::RuleGroup
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["StatelessRuleList", typing.Dict[builtins.str, typing.Any]]]] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param capacity: (experimental) The maximum operating resources that this rule group can use. Default: - Capacity is Calculated from rule requirements.
        :param custom_actions: (experimental) An optional Non-standard action to use. Default: - undefined
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateless rule group. Default: - CloudFormation-generated name
        :param rules: (experimental) The rule group rules. Default: - undefined
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2220d5307100f1182f363164af18cdb14d888a598917ca19bb4265807d34f79a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StatelessRuleGroupProps(
            capacity=capacity,
            custom_actions=custom_actions,
            description=description,
            rule_group_name=rule_group_name,
            rules=rules,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromStatelessRuleGroupArn")
    @builtins.classmethod
    def from_stateless_rule_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        stateless_rule_group_arn: builtins.str,
    ) -> IStatelessRuleGroup:
        '''(experimental) Reference existing Rule Group by Arn.

        :param scope: -
        :param id: -
        :param stateless_rule_group_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2507a0a9b3165e01f0e8a37f5dfd2861a0ac9b4b25f64e1fbff53df67b6dc851)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stateless_rule_group_arn", value=stateless_rule_group_arn, expected_type=type_hints["stateless_rule_group_arn"])
        return typing.cast(IStatelessRuleGroup, jsii.sinvoke(cls, "fromStatelessRuleGroupArn", [scope, id, stateless_rule_group_arn]))

    @jsii.member(jsii_name="fromStatelessRuleGroupName")
    @builtins.classmethod
    def from_stateless_rule_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        stateless_rule_group_name: builtins.str,
    ) -> IStatelessRuleGroup:
        '''(experimental) Reference existing Rule Group by Name.

        :param scope: -
        :param id: -
        :param stateless_rule_group_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c69638ad7336255acbfc0082be6daccc578d189437b85326eaebd35f02c7b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stateless_rule_group_name", value=stateless_rule_group_name, expected_type=type_hints["stateless_rule_group_name"])
        return typing.cast(IStatelessRuleGroup, jsii.sinvoke(cls, "fromStatelessRuleGroupName", [scope, id, stateless_rule_group_name]))

    @jsii.member(jsii_name="calculateCapacity")
    def calculate_capacity(self) -> jsii.Number:
        '''(experimental) Calculates the expected capacity required for all applied stateful rules.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "calculateCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupArn")
    def rule_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> builtins.str:
        '''(experimental) the physical name of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupId"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatelessRuleGroupList",
    jsii_struct_bases=[],
    name_mapping={"priority": "priority", "rule_group": "ruleGroup"},
)
class StatelessRuleGroupList:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        rule_group: IStatelessRuleGroup,
    ) -> None:
        '''(experimental) Maps a priority to a stateless rule group item.

        :param priority: (experimental) The priority of the rule group in the policy.
        :param rule_group: (experimental) The stateless rule.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73080b7b020bc5c160cd8a42ce7d0241a82581c931f47f204a7aed2df4c63dca)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument rule_group", value=rule_group, expected_type=type_hints["rule_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "rule_group": rule_group,
        }

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The priority of the rule group in the policy.

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rule_group(self) -> IStatelessRuleGroup:
        '''(experimental) The stateless rule.

        :stability: experimental
        '''
        result = self._values.get("rule_group")
        assert result is not None, "Required property 'rule_group' is missing"
        return typing.cast(IStatelessRuleGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatelessRuleGroupList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatelessRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "custom_actions": "customActions",
        "description": "description",
        "rule_group_name": "ruleGroupName",
        "rules": "rules",
        "variables": "variables",
    },
)
class StatelessRuleGroupProps:
    def __init__(
        self,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["StatelessRuleList", typing.Dict[builtins.str, typing.Any]]]] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The properties for defining a Stateless Rule Group.

        :param capacity: (experimental) The maximum operating resources that this rule group can use. Default: - Capacity is Calculated from rule requirements.
        :param custom_actions: (experimental) An optional Non-standard action to use. Default: - undefined
        :param description: (experimental) Description of the rule group. Default: - undefined
        :param rule_group_name: (experimental) The descriptive name of the stateless rule group. Default: - CloudFormation-generated name
        :param rules: (experimental) The rule group rules. Default: - undefined
        :param variables: (experimental) Settings that are available for use in the rules. Default: - undefined

        :stability: experimental
        '''
        if isinstance(variables, dict):
            variables = _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty(**variables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241fb05e364cf4d111e50f9ea8a21f9e78cf7a1d27b4970df79bf90ef319ef6e)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument custom_actions", value=custom_actions, expected_type=type_hints["custom_actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if custom_actions is not None:
            self._values["custom_actions"] = custom_actions
        if description is not None:
            self._values["description"] = description
        if rule_group_name is not None:
            self._values["rule_group_name"] = rule_group_name
        if rules is not None:
            self._values["rules"] = rules
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum operating resources that this rule group can use.

        :default: - Capacity is Calculated from rule requirements.

        :stability: experimental
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_actions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.CustomActionProperty]]:
        '''(experimental) An optional Non-standard action to use.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("custom_actions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.CustomActionProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the rule group.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the stateless rule group.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("rule_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["StatelessRuleList"]]:
        '''(experimental) The rule group rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["StatelessRuleList"]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty]:
        '''(experimental) Settings that are available for use in the rules.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatelessRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatelessRuleList",
    jsii_struct_bases=[],
    name_mapping={"priority": "priority", "rule": "rule"},
)
class StatelessRuleList:
    def __init__(self, *, priority: jsii.Number, rule: StatelessRule) -> None:
        '''(experimental) Maps a priority to a stateless rule.

        :param priority: (experimental) The priority of the rule in the rule group.
        :param rule: (experimental) The stateless rule.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7286b333ec55d796a606e5b8422198497b7c9dc9c149a2e4e8d07d957f32cd2)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "rule": rule,
        }

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The priority of the rule in the rule group.

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rule(self) -> StatelessRule:
        '''(experimental) The stateless rule.

        :stability: experimental
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(StatelessRule, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatelessRuleList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatelessRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "destination_ports": "destinationPorts",
        "destinations": "destinations",
        "protocols": "protocols",
        "source_ports": "sourcePorts",
        "sources": "sources",
        "tcp_flags": "tcpFlags",
    },
)
class StatelessRuleProps:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        destination_ports: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
        source_ports: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tcp_flags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for defining a stateless rule.

        :param actions: (experimental) Rule Actions. The actions to take on a packet that matches one of the stateless rule definition's match attributes.
        :param destination_ports: (experimental) The destination port to inspect for. You can specify an individual port, for example 1994 and you can specify a port range, for example 1990:1994. To match with any port, specify ANY. Default: - ANY
        :param destinations: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: - ANY
        :param protocols: (experimental) The protocols to inspect for, specified using each protocol's assigned internet protocol number (IANA). Default: - ANY
        :param source_ports: (experimental) The source ports to inspect for. Default: - ANY
        :param sources: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: - ANY
        :param tcp_flags: (experimental) TCP flags and masks to inspect packets for. Default: - undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7678a94ab703685cdd8ac5e3f1a2211f1929000eeb1e32b742966afc387ca2)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument source_ports", value=source_ports, expected_type=type_hints["source_ports"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tcp_flags", value=tcp_flags, expected_type=type_hints["tcp_flags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }
        if destination_ports is not None:
            self._values["destination_ports"] = destination_ports
        if destinations is not None:
            self._values["destinations"] = destinations
        if protocols is not None:
            self._values["protocols"] = protocols
        if source_ports is not None:
            self._values["source_ports"] = source_ports
        if sources is not None:
            self._values["sources"] = sources
        if tcp_flags is not None:
            self._values["tcp_flags"] = tcp_flags

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''(experimental) Rule Actions.

        The actions to take on a packet that matches one of the stateless rule definition's match attributes.

        :stability: experimental
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def destination_ports(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty]]:
        '''(experimental) The destination port to inspect for.

        You can specify an individual port, for example 1994 and you can specify a port range, for example 1990:1994.
        To match with any port, specify ANY.

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("destination_ports")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty]], result)

    @builtins.property
    def destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation.

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) The protocols to inspect for, specified using each protocol's assigned internet protocol number (IANA).

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def source_ports(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty]]:
        '''(experimental) The source ports to inspect for.

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("source_ports")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty]], result)

    @builtins.property
    def sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation.

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tcp_flags(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty]]:
        '''(experimental) TCP flags and masks to inspect packets for.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("tcp_flags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatelessRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@durkinza/cdk-networkfirewall-l2.StatelessStandardAction")
class StatelessStandardAction(enum.Enum):
    '''(experimental) The actions to take on a packet that matches one of the stateless rule definition's match attributes.

    :stability: experimental
    '''

    FORWARD = "FORWARD"
    '''(experimental) Discontinues stateless inspection of the packet and forwards it to the stateful rule engine for inspection.

    :stability: experimental
    '''
    PASS = "PASS"
    '''(experimental) Discontinues all inspection of the packet and permits it to go to its intended destination.

    :stability: experimental
    '''
    DROP = "DROP"
    '''(experimental) Discontinues all inspection of the packet and blocks it from going to its intended destination.

    :stability: experimental
    '''


@jsii.implements(ITLSInspectionConfiguration)
class TLSInspectionConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.TLSInspectionConfiguration",
):
    '''(experimental) Defines a Network Firewall TLS Inspection Configuration in the Stack.

    :stability: experimental
    :resource: AWS::NetworkFirewall::TLSInspectionConfiguration
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        server_certificate_configurations: typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnTLSInspectionConfiguration.ServerCertificateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        configuration_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param server_certificate_configurations: (experimental) The TLS Server Certificate Configuration Property.
        :param configuration_name: (experimental) The descriptive name of the TLS inspection configuration. You can't change the name of a TLS inspection configuration after you create it. Default: - CloudFormation-generated name
        :param description: (experimental) The Description of the TLS Inspection Configuration. Default: - No Description
        :param tags: (experimental) Tags to be added to the configuration. Default: - No tags applied

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4490d64476b988d55325cd3e8964d7635c97161b87fde2a9053c85c8807b08c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TLSInspectionConfigurationProps(
            server_certificate_configurations=server_certificate_configurations,
            configuration_name=configuration_name,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromConfigurationArn")
    @builtins.classmethod
    def from_configuration_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        configuration_arn: builtins.str,
    ) -> ITLSInspectionConfiguration:
        '''(experimental) Reference an existing TLS Inspection Configuration, defined outside of the CDK code, by arn.

        :param scope: -
        :param id: -
        :param configuration_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07a777541ab7b13bd78a3dd648c8bf46c5f15e0bbbae16e0dd0f28a18b306d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument configuration_arn", value=configuration_arn, expected_type=type_hints["configuration_arn"])
        return typing.cast(ITLSInspectionConfiguration, jsii.sinvoke(cls, "fromConfigurationArn", [scope, id, configuration_arn]))

    @jsii.member(jsii_name="fromConfigurationName")
    @builtins.classmethod
    def from_configuration_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        tls_inspection_configuration_name: builtins.str,
    ) -> ITLSInspectionConfiguration:
        '''(experimental) Reference an existing TLS Inspection Configuration, defined outside of the CDK code, by name.

        :param scope: -
        :param id: -
        :param tls_inspection_configuration_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7c3236b5d2b6b1f1b6e354a51218d5df7d29a2a50ea7b021a8724b1b11a92b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tls_inspection_configuration_name", value=tls_inspection_configuration_name, expected_type=type_hints["tls_inspection_configuration_name"])
        return typing.cast(ITLSInspectionConfiguration, jsii.sinvoke(cls, "fromConfigurationName", [scope, id, tls_inspection_configuration_name]))

    @builtins.property
    @jsii.member(jsii_name="tlsInspectionConfigurationArn")
    def tls_inspection_configuration_arn(self) -> builtins.str:
        '''(experimental) The Arn of the TLS Inspection Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tlsInspectionConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="tlsInspectionConfigurationId")
    def tls_inspection_configuration_id(self) -> builtins.str:
        '''(experimental) The physical name of the TLS Inspection Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tlsInspectionConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Description of the TLS Inspection Configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]]:
        '''(experimental) Tags to be added to the TLS Inspection Configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]], jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.TLSInspectionConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "server_certificate_configurations": "serverCertificateConfigurations",
        "configuration_name": "configurationName",
        "description": "description",
        "tags": "tags",
    },
)
class TLSInspectionConfigurationProps:
    def __init__(
        self,
        *,
        server_certificate_configurations: typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnTLSInspectionConfiguration.ServerCertificateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        configuration_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''(experimental) The Properties for defining a Firewall TLS Inspection Configuration.

        :param server_certificate_configurations: (experimental) The TLS Server Certificate Configuration Property.
        :param configuration_name: (experimental) The descriptive name of the TLS inspection configuration. You can't change the name of a TLS inspection configuration after you create it. Default: - CloudFormation-generated name
        :param description: (experimental) The Description of the TLS Inspection Configuration. Default: - No Description
        :param tags: (experimental) Tags to be added to the configuration. Default: - No tags applied

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc5ba4c985beaaaaa17a4aceb32882df3f00533c667ffe2d6e7156cb89ff48f)
            check_type(argname="argument server_certificate_configurations", value=server_certificate_configurations, expected_type=type_hints["server_certificate_configurations"])
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_certificate_configurations": server_certificate_configurations,
        }
        if configuration_name is not None:
            self._values["configuration_name"] = configuration_name
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def server_certificate_configurations(
        self,
    ) -> typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnTLSInspectionConfiguration.ServerCertificateConfigurationProperty]:
        '''(experimental) The TLS Server Certificate Configuration Property.

        :stability: experimental
        '''
        result = self._values.get("server_certificate_configurations")
        assert result is not None, "Required property 'server_certificate_configurations' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnTLSInspectionConfiguration.ServerCertificateConfigurationProperty], result)

    @builtins.property
    def configuration_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The descriptive name of the TLS inspection configuration.

        You can't change the name of a TLS inspection configuration after you create it.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Description of the TLS Inspection Configuration.

        :default: - No Description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]]:
        '''(experimental) Tags to be added to the configuration.

        :default: - No tags applied

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TLSInspectionConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWatchLogLocation(
    LogLocationBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.CloudWatchLogLocation",
):
    '''(experimental) Defines a Cloud Watch Log Group Logging Configuration.

    :stability: experimental
    '''

    def __init__(self, *, log_group: builtins.str, log_type: builtins.str) -> None:
        '''
        :param log_group: (experimental) The name of the CloudWatch Log Group to send logs to.
        :param log_type: (experimental) The type of log to send.

        :stability: experimental
        '''
        props = CloudWatchLogLocationProps(log_group=log_group, log_type=log_type)

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logDestination"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationType")
    def log_destination_type(self) -> builtins.str:
        '''(experimental) The type of storage destination to send these logs to.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logDestinationType"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.CloudWatchLogLocationProps",
    jsii_struct_bases=[LogLocationProps],
    name_mapping={"log_type": "logType", "log_group": "logGroup"},
)
class CloudWatchLogLocationProps(LogLocationProps):
    def __init__(self, *, log_type: builtins.str, log_group: builtins.str) -> None:
        '''(experimental) Defines a Cloud Watch Log Group Logging Option.

        :param log_type: (experimental) The type of log to send.
        :param log_group: (experimental) The name of the CloudWatch Log Group to send logs to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baadd44a1d965b4866bdaca7c611c5a544d263b94bd05dbb5821ef58acd6777)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_type": log_type,
            "log_group": log_group,
        }

    @builtins.property
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        result = self._values.get("log_type")
        assert result is not None, "Required property 'log_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group(self) -> builtins.str:
        '''(experimental) The name of the CloudWatch Log Group to send logs to.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchLogLocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IFirewall)
class Firewall(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.Firewall",
):
    '''(experimental) Defines a Network Firewall in the Stack.

    :stability: experimental
    :resource: AWS::NetworkFirewall::Firewall
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        policy: IFirewallPolicy,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        delete_protection: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_name: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[builtins.bool] = None,
        logging_cloud_watch_log_groups: typing.Optional[typing.Sequence[typing.Union[CloudWatchLogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        logging_kinesis_data_streams: typing.Optional[typing.Sequence[typing.Union["KinesisDataFirehoseLogLocationProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        logging_s3_buckets: typing.Optional[typing.Sequence[typing.Union[S3LogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_change_protection: typing.Optional[builtins.bool] = None,
        subnet_mappings: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param policy: (experimental) Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.
        :param vpc: (experimental) The unique identifier of the VPC where the firewall is in use. You can't change the VPC of a firewall after you create the firewall.
        :param delete_protection: (experimental) A flag indicating whether it is possible to delete the firewall. A setting of TRUE indicates that the firewall is protected against deletion Default: - true
        :param description: (experimental) The description of the Firewall. Default: - undefined
        :param firewall_name: (experimental) The descriptive name of the firewall. You can't change the name of a firewall after you create it. Default: - CloudFormation-generated name
        :param firewall_policy_change_protection: (experimental) A setting indicating whether the firewall is protected against a change to the firewall policy association. Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. Default: - true
        :param logging_cloud_watch_log_groups: (experimental) A list of CloudWatch LogGroups to send logs to. Default: - Logs will not be sent to a cloudwatch group.
        :param logging_kinesis_data_streams: (experimental) A list of Kinesis Data Firehose to send logs to. Default: - Logs will not be sent to a Kinesis DataFirehose.
        :param logging_s3_buckets: (experimental) A list of S3 Buckets to send logs to. Default: - Logs will not be sent to an S3 bucket.
        :param subnet_change_protection: (experimental) A setting indicating whether the firewall is protected against changes to the subnet associations. Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. Default: - true
        :param subnet_mappings: (experimental) The public subnets that Network Firewall is using for the firewall. Each subnet must belong to a different Availability Zone. Default: - All public subnets of the VPC
        :param tags: (experimental) Tags to be added to the firewall. Default: - No tags applied

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b730af95c09a69e15fc1ac1f259d6c144a1657509e13130121043179b6775d47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallProps(
            policy=policy,
            vpc=vpc,
            delete_protection=delete_protection,
            description=description,
            firewall_name=firewall_name,
            firewall_policy_change_protection=firewall_policy_change_protection,
            logging_cloud_watch_log_groups=logging_cloud_watch_log_groups,
            logging_kinesis_data_streams=logging_kinesis_data_streams,
            logging_s3_buckets=logging_s3_buckets,
            subnet_change_protection=subnet_change_protection,
            subnet_mappings=subnet_mappings,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFirewallArn")
    @builtins.classmethod
    def from_firewall_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        firewall_arn: builtins.str,
    ) -> IFirewall:
        '''(experimental) Reference an existing Network Firewall, defined outside of the CDK code, by arn.

        :param scope: -
        :param id: -
        :param firewall_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9866258c46b18bc89db26eba1917c8b33fa58a35712e63b842265e9cdc11db45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_arn", value=firewall_arn, expected_type=type_hints["firewall_arn"])
        return typing.cast(IFirewall, jsii.sinvoke(cls, "fromFirewallArn", [scope, id, firewall_arn]))

    @jsii.member(jsii_name="fromFirewallName")
    @builtins.classmethod
    def from_firewall_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        firewall_name: builtins.str,
    ) -> IFirewall:
        '''(experimental) Reference an existing Network Firewall, defined outside of the CDK code, by name.

        :param scope: -
        :param id: -
        :param firewall_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec91d3618ad807524296145c696696140e77ed8fcc85425ceadf933e637fd0d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
        return typing.cast(IFirewall, jsii.sinvoke(cls, "fromFirewallName", [scope, id, firewall_name]))

    @jsii.member(jsii_name="addLoggingConfigurations")
    def add_logging_configurations(
        self,
        configuration_name: builtins.str,
        log_locations: typing.Sequence[ILogLocation],
    ) -> LoggingConfiguration:
        '''(experimental) Add a Logging Configuration to the Firewall.

        :param configuration_name: The Name of the Logging configuration type.
        :param log_locations: An array of Log Locations.

        :return: A LoggingConfiguration Resource.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806586dc2df8d42c847b7c783e840df37f31e035fbad0b9fb912b218ade526f1)
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument log_locations", value=log_locations, expected_type=type_hints["log_locations"])
        return typing.cast(LoggingConfiguration, jsii.invoke(self, "addLoggingConfigurations", [configuration_name, log_locations]))

    @builtins.property
    @jsii.member(jsii_name="endpointIds")
    def endpoint_ids(self) -> typing.List[builtins.str]:
        '''(experimental) The unique IDs of the firewall endpoints for all of the subnets that you attached to the firewall.

        The subnets are not listed in any particular order.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "endpointIds"))

    @builtins.property
    @jsii.member(jsii_name="firewallArn")
    def firewall_arn(self) -> builtins.str:
        '''(experimental) The Arn of the Firewall.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallId")
    def firewall_id(self) -> builtins.str:
        '''(experimental) The physical name of the Firewall.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallId"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> IFirewallPolicy:
        '''(experimental) The associated firewall Policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(IFirewallPolicy, jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="loggingCloudWatchLogGroups")
    def logging_cloud_watch_log_groups(self) -> typing.List[CloudWatchLogLocationProps]:
        '''(experimental) The Cloud Watch Log Groups to send logs to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List[CloudWatchLogLocationProps], jsii.get(self, "loggingCloudWatchLogGroups"))

    @logging_cloud_watch_log_groups.setter
    def logging_cloud_watch_log_groups(
        self,
        value: typing.List[CloudWatchLogLocationProps],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa4b6efa55141c129124bdbbca205cd81c8c760c3a5ddaf3223dd79ede378b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingCloudWatchLogGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingConfigurations")
    def logging_configurations(self) -> typing.List[ILoggingConfiguration]:
        '''(experimental) The list of references to the generated logging configurations.

        :stability: experimental
        '''
        return typing.cast(typing.List[ILoggingConfiguration], jsii.get(self, "loggingConfigurations"))

    @logging_configurations.setter
    def logging_configurations(self, value: typing.List[ILoggingConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540fd1fb1bf804d0d70c20899f8780003186578e4e2f57daa9148754e20cbea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingConfigurations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingKinesisDataStreams")
    def logging_kinesis_data_streams(
        self,
    ) -> typing.List["KinesisDataFirehoseLogLocationProps"]:
        '''(experimental) The Kinesis Data Stream locations.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List["KinesisDataFirehoseLogLocationProps"], jsii.get(self, "loggingKinesisDataStreams"))

    @logging_kinesis_data_streams.setter
    def logging_kinesis_data_streams(
        self,
        value: typing.List["KinesisDataFirehoseLogLocationProps"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d979390b80e5947a9b72aedb49fabf95892daf6751fb1d506e673abaf8006eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingKinesisDataStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingS3Buckets")
    def logging_s3_buckets(self) -> typing.List[S3LogLocationProps]:
        '''(experimental) The S3 Buckets to send logs to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List[S3LogLocationProps], jsii.get(self, "loggingS3Buckets"))

    @logging_s3_buckets.setter
    def logging_s3_buckets(self, value: typing.List[S3LogLocationProps]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d48d1362e4ba1359cf24a315878eaaded69ce2af8cf3154537b1f4b324b4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingS3Buckets", value) # pyright: ignore[reportArgumentType]


@jsii.implements(IFirewallPolicy)
class FirewallPolicy(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.FirewallPolicy",
):
    '''(experimental) Defines a Firewall Policy in the stack.

    :stability: experimental
    :resource: AWS::NetworkFirewall::FirewallPolicy
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stateless_default_actions: typing.Sequence[builtins.str],
        stateless_fragment_default_actions: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        firewall_policy_name: typing.Optional[builtins.str] = None,
        stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        stateful_rule_groups: typing.Optional[typing.Sequence[typing.Union[StatefulRuleGroupList, typing.Dict[builtins.str, typing.Any]]]] = None,
        stateless_custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        stateless_rule_groups: typing.Optional[typing.Sequence[typing.Union[StatelessRuleGroupList, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
        tls_inspection_configuration: typing.Optional[ITLSInspectionConfiguration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stateless_default_actions: (experimental) The actions to take on a packet if it doesn't match any of the stateless rules in the policy.
        :param stateless_fragment_default_actions: (experimental) The actions to take on a fragmented packet if it doesn't match any of the stateless rules in the policy.
        :param description: (experimental) The description of the policy. Default: - undefined
        :param firewall_policy_name: (experimental) The descriptive name of the firewall policy. You can't change the name of a firewall policy after you create it. Default: - CloudFormation-generated name
        :param stateful_default_actions: (experimental) The default actions to take on a packet that doesn't match any stateful rules. The stateful default action is optional, and is only valid when using the strict rule order Default: - undefined
        :param stateful_engine_options: (experimental) Additional options governing how Network Firewall handles stateful rules. The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings Default: - undefined
        :param stateful_rule_groups: (experimental) The stateful rule groups that are used in the policy. Default: - undefined
        :param stateless_custom_actions: (experimental) The custom action definitions that are available for use in the firewall policy's statelessDefaultActions setting. Default: - undefined
        :param stateless_rule_groups: (experimental) References to the stateless rule groups that are used in the policy. Default: - undefined
        :param tags: (experimental) Tags to be added to the policy. Default: - No tags applied
        :param tls_inspection_configuration: (experimental) AWS Network Firewall uses a TLS inspection configuration to decrypt traffic. Network Firewall re-encrypts the traffic before sending it to its destination. Default: - No TLS Inspection performed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec858c58bfaa7933e7b6829f8f661bbde0ea7e933c633ceaee820ef3eca1a7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallPolicyProps(
            stateless_default_actions=stateless_default_actions,
            stateless_fragment_default_actions=stateless_fragment_default_actions,
            description=description,
            firewall_policy_name=firewall_policy_name,
            stateful_default_actions=stateful_default_actions,
            stateful_engine_options=stateful_engine_options,
            stateful_rule_groups=stateful_rule_groups,
            stateless_custom_actions=stateless_custom_actions,
            stateless_rule_groups=stateless_rule_groups,
            tags=tags,
            tls_inspection_configuration=tls_inspection_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFirewallPolicyArn")
    @builtins.classmethod
    def from_firewall_policy_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        firewall_policy_arn: builtins.str,
    ) -> IFirewallPolicy:
        '''(experimental) Reference existing firewall policy by Arn.

        :param scope: -
        :param id: -
        :param firewall_policy_arn: the ARN of the existing firewall policy.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5230369997faa0159fe46efcfe4dde6a3d5e7449a62639743895ad6a75c81fa2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_policy_arn", value=firewall_policy_arn, expected_type=type_hints["firewall_policy_arn"])
        return typing.cast(IFirewallPolicy, jsii.sinvoke(cls, "fromFirewallPolicyArn", [scope, id, firewall_policy_arn]))

    @jsii.member(jsii_name="fromFirewallPolicyName")
    @builtins.classmethod
    def from_firewall_policy_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        firewall_policy_name: builtins.str,
    ) -> IFirewallPolicy:
        '''(experimental) Reference existing firewall policy name.

        :param scope: -
        :param id: -
        :param firewall_policy_name: The name of the existing firewall policy.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37639be68ef42b725039f900cfaa8e9fc66d1073f7baf84bda60411cd2263093)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_policy_name", value=firewall_policy_name, expected_type=type_hints["firewall_policy_name"])
        return typing.cast(IFirewallPolicy, jsii.sinvoke(cls, "fromFirewallPolicyName", [scope, id, firewall_policy_name]))

    @jsii.member(jsii_name="addStatefulRuleGroup")
    def add_stateful_rule_group(
        self,
        *,
        rule_group: IStatefulRuleGroup,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Add a stateful rule group to the policy.

        :param rule_group: (experimental) The stateful rule group.
        :param priority: (experimental) The priority of the rule group in the policy. Default: - Priority is only used when Strict order is set.

        :stability: experimental
        '''
        rule_group_ = StatefulRuleGroupList(rule_group=rule_group, priority=priority)

        return typing.cast(None, jsii.invoke(self, "addStatefulRuleGroup", [rule_group_]))

    @jsii.member(jsii_name="addStatelessRuleGroup")
    def add_stateless_rule_group(
        self,
        *,
        priority: jsii.Number,
        rule_group: IStatelessRuleGroup,
    ) -> None:
        '''(experimental) Add a stateless rule group to the policy.

        :param priority: (experimental) The priority of the rule group in the policy.
        :param rule_group: (experimental) The stateless rule.

        :stability: experimental
        '''
        rule_group_ = StatelessRuleGroupList(priority=priority, rule_group=rule_group)

        return typing.cast(None, jsii.invoke(self, "addStatelessRuleGroup", [rule_group_]))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyArn")
    def firewall_policy_arn(self) -> builtins.str:
        '''(experimental) The Arn of the policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> builtins.str:
        '''(experimental) The physical name of the firewall policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="statefulDefaultActions")
    def stateful_default_actions(self) -> typing.List[builtins.str]:
        '''(experimental) The Default actions for packets that don't match a stateful rule.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "statefulDefaultActions"))

    @builtins.property
    @jsii.member(jsii_name="statefulRuleGroups")
    def stateful_rule_groups(self) -> typing.List[StatefulRuleGroupList]:
        '''(experimental) The stateful rule groups in this policy.

        :stability: experimental
        '''
        return typing.cast(typing.List[StatefulRuleGroupList], jsii.get(self, "statefulRuleGroups"))

    @builtins.property
    @jsii.member(jsii_name="statelessDefaultActions")
    def stateless_default_actions(self) -> typing.List[builtins.str]:
        '''(experimental) The Default actions for packets that don't match a stateless rule.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "statelessDefaultActions"))

    @builtins.property
    @jsii.member(jsii_name="statelessFragmentDefaultActions")
    def stateless_fragment_default_actions(self) -> typing.List[builtins.str]:
        '''(experimental) The Default actions for fragment packets that don't match a stateless rule.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "statelessFragmentDefaultActions"))

    @builtins.property
    @jsii.member(jsii_name="statelessRuleGroups")
    def stateless_rule_groups(self) -> typing.List[StatelessRuleGroupList]:
        '''(experimental) The stateless rule groups in this policy.

        :stability: experimental
        '''
        return typing.cast(typing.List[StatelessRuleGroupList], jsii.get(self, "statelessRuleGroups"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[_aws_cdk_ceddda9d.Tag]:
        '''(experimental) Tags to be added to the policy.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_ceddda9d.Tag], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="tlsInspectionConfiguration")
    def tls_inspection_configuration(
        self,
    ) -> typing.Optional[ITLSInspectionConfiguration]:
        '''(experimental) The TLS Inspection Configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ITLSInspectionConfiguration], jsii.get(self, "tlsInspectionConfiguration"))


class KinesisDataFirehoseLogLocation(
    LogLocationBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.KinesisDataFirehoseLogLocation",
):
    '''(experimental) Defines a Kinesis Delivery Stream Logging Configuration.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        delivery_stream: builtins.str,
        log_type: builtins.str,
    ) -> None:
        '''
        :param delivery_stream: (experimental) The name of the Kinesis Data Firehose delivery stream to send logs to.
        :param log_type: (experimental) The type of log to send.

        :stability: experimental
        '''
        props = KinesisDataFirehoseLogLocationProps(
            delivery_stream=delivery_stream, log_type=log_type
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logDestination"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationType")
    def log_destination_type(self) -> builtins.str:
        '''(experimental) The type of storage destination to send these logs to.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logDestinationType"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.KinesisDataFirehoseLogLocationProps",
    jsii_struct_bases=[LogLocationProps],
    name_mapping={"log_type": "logType", "delivery_stream": "deliveryStream"},
)
class KinesisDataFirehoseLogLocationProps(LogLocationProps):
    def __init__(
        self,
        *,
        log_type: builtins.str,
        delivery_stream: builtins.str,
    ) -> None:
        '''(experimental) Defines a Kinesis Delivery Stream Logging Option.

        :param log_type: (experimental) The type of log to send.
        :param delivery_stream: (experimental) The name of the Kinesis Data Firehose delivery stream to send logs to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacae67b7131e56f8b22344ec230b83126f25cd592e5584a58c8b38ac4b7e03b)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_type": log_type,
            "delivery_stream": delivery_stream,
        }

    @builtins.property
    def log_type(self) -> builtins.str:
        '''(experimental) The type of log to send.

        :stability: experimental
        '''
        result = self._values.get("log_type")
        assert result is not None, "Required property 'log_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delivery_stream(self) -> builtins.str:
        '''(experimental) The name of the Kinesis Data Firehose delivery stream to send logs to.

        :stability: experimental
        '''
        result = self._values.get("delivery_stream")
        assert result is not None, "Required property 'delivery_stream' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisDataFirehoseLogLocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Stateful5TupleRule(
    StatefulRuleBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.Stateful5TupleRule",
):
    '''(experimental) Generates a Stateful Rule from a 5 Tuple.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        action: builtins.str,
        destination: typing.Optional[builtins.str] = None,
        destination_port: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        rule_options: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[builtins.str] = None,
        source_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: (experimental) The action to perform when a rule is matched.
        :param destination: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: = ANY
        :param destination_port: (experimental) The destination port to inspect for. You can specify an individual port, for example 1994 and you can specify a port range, for example 1990:1994 . To match with any port, specify ANY Default: - ANY
        :param direction: (experimental) The direction of traffic flow to inspect. If set to ANY, the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source. If set to FORWARD , the inspection only matches traffic going from the source to the destination. Default: - ANY
        :param protocol: (experimental) The protocol to inspect for. To specify all, you can use IP , because all traffic on AWS and on the internet is IP. Default: - IP
        :param rule_options: (experimental) Additional settings for a stateful rule, provided as keywords and settings. Default: - undefined
        :param source: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: = ANY
        :param source_port: (experimental) The source IP address or address range to inspect for, in CIDR notation. To match with any address, specify ANY. Default: - ANY

        :stability: experimental
        '''
        props = Stateful5TupleRuleProps(
            action=action,
            destination=destination,
            destination_port=destination_port,
            direction=direction,
            protocol=protocol,
            rule_options=rule_options,
            source=source,
            source_port=source_port,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(
        self,
    ) -> _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatefulRuleProperty:
        '''(experimental) The L1 Stateful Rule Property.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatefulRuleProperty, jsii.get(self, "resource"))

    @resource.setter
    def resource(
        self,
        value: _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatefulRuleProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95688bab05b21b605b8612dc57c58c609a52b39d3c6fd93a7ca6a9f2ed0ed1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.Stateful5TupleRuleProps",
    jsii_struct_bases=[StatefulRuleBaseProps],
    name_mapping={
        "action": "action",
        "destination": "destination",
        "destination_port": "destinationPort",
        "direction": "direction",
        "protocol": "protocol",
        "rule_options": "ruleOptions",
        "source": "source",
        "source_port": "sourcePort",
    },
)
class Stateful5TupleRuleProps(StatefulRuleBaseProps):
    def __init__(
        self,
        *,
        action: builtins.str,
        destination: typing.Optional[builtins.str] = None,
        destination_port: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        rule_options: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[builtins.str] = None,
        source_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a 5 Tuple rule.

        :param action: (experimental) The action to perform when a rule is matched.
        :param destination: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: = ANY
        :param destination_port: (experimental) The destination port to inspect for. You can specify an individual port, for example 1994 and you can specify a port range, for example 1990:1994 . To match with any port, specify ANY Default: - ANY
        :param direction: (experimental) The direction of traffic flow to inspect. If set to ANY, the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source. If set to FORWARD , the inspection only matches traffic going from the source to the destination. Default: - ANY
        :param protocol: (experimental) The protocol to inspect for. To specify all, you can use IP , because all traffic on AWS and on the internet is IP. Default: - IP
        :param rule_options: (experimental) Additional settings for a stateful rule, provided as keywords and settings. Default: - undefined
        :param source: (experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Default: = ANY
        :param source_port: (experimental) The source IP address or address range to inspect for, in CIDR notation. To match with any address, specify ANY. Default: - ANY

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efa7c644eb542b84138187f15d1b30b0cac78af42d4d0f187c2ed31b34fedb1)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument rule_options", value=rule_options, expected_type=type_hints["rule_options"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
        }
        if destination is not None:
            self._values["destination"] = destination
        if destination_port is not None:
            self._values["destination_port"] = destination_port
        if direction is not None:
            self._values["direction"] = direction
        if protocol is not None:
            self._values["protocol"] = protocol
        if rule_options is not None:
            self._values["rule_options"] = rule_options
        if source is not None:
            self._values["source"] = source
        if source_port is not None:
            self._values["source_port"] = source_port

    @builtins.property
    def action(self) -> builtins.str:
        '''(experimental) The action to perform when a rule is matched.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation.

        :default: = ANY

        :stability: experimental
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_port(self) -> typing.Optional[builtins.str]:
        '''(experimental) The destination port to inspect for.

        You can specify an individual port, for example 1994 and you can specify a port range, for example 1990:1994 .
        To match with any port, specify ANY

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("destination_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''(experimental) The direction of traffic flow to inspect.

        If set to ANY, the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source.
        If set to FORWARD , the inspection only matches traffic going from the source to the destination.

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''(experimental) The protocol to inspect for.

        To specify all, you can use IP , because all traffic on AWS and on the internet is IP.

        :default: - IP

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_options(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleOptionProperty]]:
        '''(experimental) Additional settings for a stateful rule, provided as keywords and settings.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("rule_options")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleOptionProperty]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify an array of IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation.

        :default: = ANY

        :stability: experimental
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_port(self) -> typing.Optional[builtins.str]:
        '''(experimental) The source IP address or address range to inspect for, in CIDR notation.

        To match with any address, specify ANY.

        :default: - ANY

        :stability: experimental
        '''
        result = self._values.get("source_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Stateful5TupleRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StatefulDomainListRule(
    StatefulRuleBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulDomainListRule",
):
    '''(experimental) Generates a Stateful Rule from a Domain List.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        targets: typing.Sequence[builtins.str],
        target_types: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param targets: (experimental) The domains that you want to inspect for in your traffic flows.
        :param target_types: (experimental) The types of targets to inspect for.
        :param type: (experimental) Whether you want to allow or deny access to the domains in your target list.

        :stability: experimental
        '''
        props = StatefulDomainListRuleProps(
            targets=targets, target_types=target_types, type=type
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(
        self,
    ) -> _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RulesSourceListProperty:
        '''(experimental) The L1 Stateful Rule Property.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RulesSourceListProperty, jsii.get(self, "resource"))

    @resource.setter
    def resource(
        self,
        value: _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RulesSourceListProperty,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76aa6c9b0acbf66de597ac8f58443f69b75eb429f3e24e188409926d4305fc29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@durkinza/cdk-networkfirewall-l2.StatefulDomainListRuleProps",
    jsii_struct_bases=[StatefulRuleBaseProps],
    name_mapping={"targets": "targets", "target_types": "targetTypes", "type": "type"},
)
class StatefulDomainListRuleProps(StatefulRuleBaseProps):
    def __init__(
        self,
        *,
        targets: typing.Sequence[builtins.str],
        target_types: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''(experimental) The properties for defining a Stateful Domain List Rule.

        :param targets: (experimental) The domains that you want to inspect for in your traffic flows.
        :param target_types: (experimental) The types of targets to inspect for.
        :param type: (experimental) Whether you want to allow or deny access to the domains in your target list.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1345566fc37b422a1c0e4c9c860a077bbf190212d3e41bf7a0a726fea0b251)
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument target_types", value=target_types, expected_type=type_hints["target_types"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "targets": targets,
            "target_types": target_types,
            "type": type,
        }

    @builtins.property
    def targets(self) -> typing.List[builtins.str]:
        '''(experimental) The domains that you want to inspect for in your traffic flows.

        :stability: experimental
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target_types(self) -> typing.List[builtins.str]:
        '''(experimental) The types of targets to inspect for.

        :stability: experimental
        '''
        result = self._values.get("target_types")
        assert result is not None, "Required property 'target_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) Whether you want to allow or deny access to the domains in your target list.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatefulDomainListRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudWatchLogLocation",
    "CloudWatchLogLocationProps",
    "Firewall",
    "FirewallPolicy",
    "FirewallPolicyProps",
    "FirewallProps",
    "IFirewall",
    "IFirewallPolicy",
    "ILogLocation",
    "ILoggingConfiguration",
    "IStatefulRule",
    "IStatefulRuleGroup",
    "IStatelessRule",
    "IStatelessRuleGroup",
    "ITLSInspectionConfiguration",
    "KinesisDataFirehoseLogLocation",
    "KinesisDataFirehoseLogLocationProps",
    "LogDestinationType",
    "LogLocationBase",
    "LogLocationProps",
    "LogType",
    "LoggingConfiguration",
    "LoggingConfigurationProps",
    "S3LogLocation",
    "S3LogLocationProps",
    "Stateful5TupleDirection",
    "Stateful5TupleRule",
    "Stateful5TupleRuleGroup",
    "Stateful5TupleRuleGroupProps",
    "Stateful5TupleRuleProps",
    "StatefulDomainListRule",
    "StatefulDomainListRuleGroup",
    "StatefulDomainListRuleGroupProps",
    "StatefulDomainListRuleProps",
    "StatefulDomainListTargetType",
    "StatefulDomainListType",
    "StatefulRuleBase",
    "StatefulRuleBaseProps",
    "StatefulRuleGroupList",
    "StatefulRuleOptions",
    "StatefulStandardAction",
    "StatefulStrictAction",
    "StatefulSuricataRuleGroup",
    "StatefulSuricataRuleGroupFromFileProps",
    "StatefulSuricataRuleGroupProps",
    "StatelessRule",
    "StatelessRuleGroup",
    "StatelessRuleGroupList",
    "StatelessRuleGroupProps",
    "StatelessRuleList",
    "StatelessRuleProps",
    "StatelessStandardAction",
    "TLSInspectionConfiguration",
    "TLSInspectionConfigurationProps",
]

publication.publish()

def _typecheckingstub__6e2ee17c56a70c25fdc61a7b9804a602c5694964b1af4a38b56f674abcc0045c(
    *,
    stateless_default_actions: typing.Sequence[builtins.str],
    stateless_fragment_default_actions: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    firewall_policy_name: typing.Optional[builtins.str] = None,
    stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_rule_groups: typing.Optional[typing.Sequence[typing.Union[StatefulRuleGroupList, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateless_custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateless_rule_groups: typing.Optional[typing.Sequence[typing.Union[StatelessRuleGroupList, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    tls_inspection_configuration: typing.Optional[ITLSInspectionConfiguration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cd51c57140520e1402f72c6b992e6b19354a9aa93b962d68d999197e4b7254(
    *,
    policy: IFirewallPolicy,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    delete_protection: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    firewall_name: typing.Optional[builtins.str] = None,
    firewall_policy_change_protection: typing.Optional[builtins.bool] = None,
    logging_cloud_watch_log_groups: typing.Optional[typing.Sequence[typing.Union[CloudWatchLogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    logging_kinesis_data_streams: typing.Optional[typing.Sequence[typing.Union[KinesisDataFirehoseLogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    logging_s3_buckets: typing.Optional[typing.Sequence[typing.Union[S3LogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_change_protection: typing.Optional[builtins.bool] = None,
    subnet_mappings: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c969855b1e57c3f77f7527e0b14ed1a48e2993dab44eeebb2e88de6d3f8e54(
    log_destination_type: LogDestinationType,
    *,
    log_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c324b8a677fd1a0df70aa85bccc3288338dafbb97c5c8a1e5d46116b7ad474dc(
    *,
    log_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46589e30dbca05715df2fc8b312a6a7078e3918ff0acdefb719f2765a73f011d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    firewall_ref: builtins.str,
    firewall_name: typing.Optional[builtins.str] = None,
    logging_configuration_name: typing.Optional[builtins.str] = None,
    logging_locations: typing.Optional[typing.Sequence[ILogLocation]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bfa58d0b28a9fff7797847dc6fb8f8da707b707cdba55022ad68325bfc0ee2(
    log_locations: typing.Sequence[ILogLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b335d6947dc4cfacd2dbc21b6a86d3fe52f4eeef15eb5e262fec2272bde663bc(
    value: typing.List[ILogLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df75dcff12eb45788a994841d82b6f8af893265985ff4b0cfa0365464c84841(
    *,
    firewall_ref: builtins.str,
    firewall_name: typing.Optional[builtins.str] = None,
    logging_configuration_name: typing.Optional[builtins.str] = None,
    logging_locations: typing.Optional[typing.Sequence[ILogLocation]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9566111f1fea55135e7160f79ac8189860c019719e48087c2e8a661188b9c34e(
    *,
    log_type: builtins.str,
    bucket_name: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d354536559ae5c79502835ce91ecd498376a49e28c0e94909bd1effd716162(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    rules: typing.Optional[typing.Sequence[Stateful5TupleRule]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30506ba2b8c70f0a197eb50472e01c9f595c8f0b8d054be707786bc72bb51b50(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    rule_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b471389c990532ca98eadf99cec5936497f7ba575edbae7a6229b11feddbedb(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    rules: typing.Optional[typing.Sequence[Stateful5TupleRule]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db8aa1719bfb18562efe72ca2175431fe159270f8397b8caf3cb1b533448c70(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    rule: typing.Optional[StatefulDomainListRule] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e95866eb2f5a18a22c37d81b4688a24e2b74dde351e03c6e7ee5e66fff16746(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    rule_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475ae631eb0efaeba527029eed7ee37a29cb2729e0d5cc6b0cb753ae8e3021e4(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    rule: typing.Optional[StatefulDomainListRule] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ec66b096d7b56fc7112f4faa1a444073f7bb1ca04c40a908646a9c3d662c69(
    *,
    rule_group: IStatefulRuleGroup,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a4572db82842b82805cb8495f44d81c4ea72914aa229b47b87c39baeab428d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    rules: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2afaa1480e87fa8bd625ff6985dfad168d9ba6d1e13e0c84d0cc9efb78668da(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    path: builtins.str,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d4ceba10ad19d785444a5cefc47ebfc90a8d5bbf5d7818f8be4cb15ce8d56e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    rule_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5485a09476759c5e75fb7cce8b3bd4b9889793dfe6d19aea78857a4938935089(
    *,
    path: builtins.str,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23856d3a152b06d39d4ba08d112a04dc652a95ac2d69d1f1ad6f54049b658a18(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[StatefulRuleOptions] = None,
    rules: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0feb55e3ca55cf06df0c3dac06774dff4ba0ca73f349bb1a212206dd088ed1fb(
    value: _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleDefinitionProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2220d5307100f1182f363164af18cdb14d888a598917ca19bb4265807d34f79a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capacity: typing.Optional[jsii.Number] = None,
    custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[StatelessRuleList, typing.Dict[builtins.str, typing.Any]]]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2507a0a9b3165e01f0e8a37f5dfd2861a0ac9b4b25f64e1fbff53df67b6dc851(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    stateless_rule_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c69638ad7336255acbfc0082be6daccc578d189437b85326eaebd35f02c7b4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    stateless_rule_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73080b7b020bc5c160cd8a42ce7d0241a82581c931f47f204a7aed2df4c63dca(
    *,
    priority: jsii.Number,
    rule_group: IStatelessRuleGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241fb05e364cf4d111e50f9ea8a21f9e78cf7a1d27b4970df79bf90ef319ef6e(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[StatelessRuleList, typing.Dict[builtins.str, typing.Any]]]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7286b333ec55d796a606e5b8422198497b7c9dc9c149a2e4e8d07d957f32cd2(
    *,
    priority: jsii.Number,
    rule: StatelessRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7678a94ab703685cdd8ac5e3f1a2211f1929000eeb1e32b742966afc387ca2(
    *,
    actions: typing.Sequence[builtins.str],
    destination_ports: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
    source_ports: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tcp_flags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4490d64476b988d55325cd3e8964d7635c97161b87fde2a9053c85c8807b08c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    server_certificate_configurations: typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnTLSInspectionConfiguration.ServerCertificateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    configuration_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07a777541ab7b13bd78a3dd648c8bf46c5f15e0bbbae16e0dd0f28a18b306d2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7c3236b5d2b6b1f1b6e354a51218d5df7d29a2a50ea7b021a8724b1b11a92b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    tls_inspection_configuration_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc5ba4c985beaaaaa17a4aceb32882df3f00533c667ffe2d6e7156cb89ff48f(
    *,
    server_certificate_configurations: typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnTLSInspectionConfiguration.ServerCertificateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    configuration_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baadd44a1d965b4866bdaca7c611c5a544d263b94bd05dbb5821ef58acd6777(
    *,
    log_type: builtins.str,
    log_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b730af95c09a69e15fc1ac1f259d6c144a1657509e13130121043179b6775d47(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    policy: IFirewallPolicy,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    delete_protection: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    firewall_name: typing.Optional[builtins.str] = None,
    firewall_policy_change_protection: typing.Optional[builtins.bool] = None,
    logging_cloud_watch_log_groups: typing.Optional[typing.Sequence[typing.Union[CloudWatchLogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    logging_kinesis_data_streams: typing.Optional[typing.Sequence[typing.Union[KinesisDataFirehoseLogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    logging_s3_buckets: typing.Optional[typing.Sequence[typing.Union[S3LogLocationProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_change_protection: typing.Optional[builtins.bool] = None,
    subnet_mappings: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9866258c46b18bc89db26eba1917c8b33fa58a35712e63b842265e9cdc11db45(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec91d3618ad807524296145c696696140e77ed8fcc85425ceadf933e637fd0d9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806586dc2df8d42c847b7c783e840df37f31e035fbad0b9fb912b218ade526f1(
    configuration_name: builtins.str,
    log_locations: typing.Sequence[ILogLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa4b6efa55141c129124bdbbca205cd81c8c760c3a5ddaf3223dd79ede378b3(
    value: typing.List[CloudWatchLogLocationProps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540fd1fb1bf804d0d70c20899f8780003186578e4e2f57daa9148754e20cbea1(
    value: typing.List[ILoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d979390b80e5947a9b72aedb49fabf95892daf6751fb1d506e673abaf8006eb9(
    value: typing.List[KinesisDataFirehoseLogLocationProps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d48d1362e4ba1359cf24a315878eaaded69ce2af8cf3154537b1f4b324b4c5(
    value: typing.List[S3LogLocationProps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec858c58bfaa7933e7b6829f8f661bbde0ea7e933c633ceaee820ef3eca1a7f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stateless_default_actions: typing.Sequence[builtins.str],
    stateless_fragment_default_actions: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    firewall_policy_name: typing.Optional[builtins.str] = None,
    stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    stateful_rule_groups: typing.Optional[typing.Sequence[typing.Union[StatefulRuleGroupList, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateless_custom_actions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateless_rule_groups: typing.Optional[typing.Sequence[typing.Union[StatelessRuleGroupList, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    tls_inspection_configuration: typing.Optional[ITLSInspectionConfiguration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5230369997faa0159fe46efcfe4dde6a3d5e7449a62639743895ad6a75c81fa2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37639be68ef42b725039f900cfaa8e9fc66d1073f7baf84bda60411cd2263093(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacae67b7131e56f8b22344ec230b83126f25cd592e5584a58c8b38ac4b7e03b(
    *,
    log_type: builtins.str,
    delivery_stream: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95688bab05b21b605b8612dc57c58c609a52b39d3c6fd93a7ca6a9f2ed0ed1ef(
    value: _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatefulRuleProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efa7c644eb542b84138187f15d1b30b0cac78af42d4d0f187c2ed31b34fedb1(
    *,
    action: builtins.str,
    destination: typing.Optional[builtins.str] = None,
    destination_port: typing.Optional[builtins.str] = None,
    direction: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    rule_options: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RuleOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[builtins.str] = None,
    source_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76aa6c9b0acbf66de597ac8f58443f69b75eb429f3e24e188409926d4305fc29(
    value: _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.RulesSourceListProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1345566fc37b422a1c0e4c9c860a077bbf190212d3e41bf7a0a726fea0b251(
    *,
    targets: typing.Sequence[builtins.str],
    target_types: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
