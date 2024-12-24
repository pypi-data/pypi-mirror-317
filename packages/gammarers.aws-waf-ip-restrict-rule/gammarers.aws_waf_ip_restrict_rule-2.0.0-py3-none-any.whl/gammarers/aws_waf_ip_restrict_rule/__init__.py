r'''
# AWS WAF(V2) IP Restrict Rule Group

[![GitHub](https://img.shields.io/github/license/gammarers/aws-waf-ip-restrict-rule?style=flat-square)](https://github.com/gammarers/aws-waf-ip-restrict-rule/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-waf-ip-restrict-rule?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-waf-ip-restrict-rule)
[![PyPI](https://img.shields.io/pypi/v/gammarers.aws-waf-ip-restrict-rule?style=flat-square)](https://pypi.org/project/gammarers.aws-waf-ip-restrict-rule/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-waf-ip-restrict-rule/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-waf-ip-restrict-rule/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-waf-ip-restrict-rule?sort=semver&style=flat-square)](https://github.com/gammarers/aws-waf-ip-restrict-rule/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarers/aws-waf-ip-restrict-rule)](https://constructs.dev/packages/@gammarers/aws-waf-ip-restrict-rule)

This is an AWS CDK Construct for IP Restriction Rule Group on WAF V2

## Install

### TypeScript

#### install by npm

```shell
npm install @gammarers/aws-waf-ip-restrict-rule
```

#### install by yarn

```shell
yarn add @gammarers/aws-waf-ip-restrict-rule
```

### Python

```shell
pip install gammarers.aws-waf-ip-restrict-rule
```

## Example

```python
import { WAFIPRestrictRule } from '@gammarers/aws-waf-ip-restrict-rule';

const ipRestrictRule = new WAFIPRestrictRule(stack, 'WAFIPRestrictRule', {
  allowIpAddresses: [
    '192.0.2.0/24',
    '198.51.100.0/24',
    '203.0.113.0/24',
  ],
  scope: WAFIPRestrictRuleScope.GLOBAL,
  priority: 1,
});

new wafv2.CfnWebACL(stack, 'WebACL', {
  defaultAction: { allow: {} },
  scope: 'CLOUD_FRONT',
  name: 'WebAclWithCustomRules',
  visibilityConfig: {
    cloudWatchMetricsEnabled: true,
    metricName: 'WebAclMetric',
    sampledRequestsEnabled: true,
  },
  rules: [ipRestrictRule.rule],
});
```

## License

This project is licensed under the Apache-2.0 License.
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

import aws_cdk.aws_wafv2 as _aws_cdk_aws_wafv2_ceddda9d
import constructs as _constructs_77d1e7e8


class WAFIPRestrictRule(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarers/aws-waf-ip-restrict-rule.WAFIPRestrictRule",
):
    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allow_ip_addresses: typing.Sequence[builtins.str],
        priority: jsii.Number,
        scope: "WAFIPRestrictRuleScope",
        allow_ip_set_name: typing.Optional[builtins.str] = None,
        cloud_watch_metrics_name: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope_: -
        :param id: -
        :param allow_ip_addresses: 
        :param priority: 
        :param scope: 
        :param allow_ip_set_name: 
        :param cloud_watch_metrics_name: 
        :param rule_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7effff35cda2ec5c68fc5091d88259103726628a8e720f9588fb2aee3226eed)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WAFIPRestrictRuleProps(
            allow_ip_addresses=allow_ip_addresses,
            priority=priority,
            scope=scope,
            allow_ip_set_name=allow_ip_set_name,
            cloud_watch_metrics_name=cloud_watch_metrics_name,
            rule_name=rule_name,
        )

        jsii.create(self.__class__, self, [scope_, id, props])

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> _aws_cdk_aws_wafv2_ceddda9d.CfnWebACL.RuleProperty:
        return typing.cast(_aws_cdk_aws_wafv2_ceddda9d.CfnWebACL.RuleProperty, jsii.get(self, "rule"))


@jsii.data_type(
    jsii_type="@gammarers/aws-waf-ip-restrict-rule.WAFIPRestrictRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_ip_addresses": "allowIpAddresses",
        "priority": "priority",
        "scope": "scope",
        "allow_ip_set_name": "allowIpSetName",
        "cloud_watch_metrics_name": "cloudWatchMetricsName",
        "rule_name": "ruleName",
    },
)
class WAFIPRestrictRuleProps:
    def __init__(
        self,
        *,
        allow_ip_addresses: typing.Sequence[builtins.str],
        priority: jsii.Number,
        scope: "WAFIPRestrictRuleScope",
        allow_ip_set_name: typing.Optional[builtins.str] = None,
        cloud_watch_metrics_name: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_ip_addresses: 
        :param priority: 
        :param scope: 
        :param allow_ip_set_name: 
        :param cloud_watch_metrics_name: 
        :param rule_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806fc823d81f071a81d15d8b650b27177eadf1fd6470404d2e6da0d461383624)
            check_type(argname="argument allow_ip_addresses", value=allow_ip_addresses, expected_type=type_hints["allow_ip_addresses"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument allow_ip_set_name", value=allow_ip_set_name, expected_type=type_hints["allow_ip_set_name"])
            check_type(argname="argument cloud_watch_metrics_name", value=cloud_watch_metrics_name, expected_type=type_hints["cloud_watch_metrics_name"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_ip_addresses": allow_ip_addresses,
            "priority": priority,
            "scope": scope,
        }
        if allow_ip_set_name is not None:
            self._values["allow_ip_set_name"] = allow_ip_set_name
        if cloud_watch_metrics_name is not None:
            self._values["cloud_watch_metrics_name"] = cloud_watch_metrics_name
        if rule_name is not None:
            self._values["rule_name"] = rule_name

    @builtins.property
    def allow_ip_addresses(self) -> typing.List[builtins.str]:
        result = self._values.get("allow_ip_addresses")
        assert result is not None, "Required property 'allow_ip_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def priority(self) -> jsii.Number:
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scope(self) -> "WAFIPRestrictRuleScope":
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast("WAFIPRestrictRuleScope", result)

    @builtins.property
    def allow_ip_set_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("allow_ip_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_metrics_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_watch_metrics_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WAFIPRestrictRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@gammarers/aws-waf-ip-restrict-rule.WAFIPRestrictRuleScope")
class WAFIPRestrictRuleScope(enum.Enum):
    GLOBAL = "GLOBAL"
    REGIONAL = "REGIONAL"


__all__ = [
    "WAFIPRestrictRule",
    "WAFIPRestrictRuleProps",
    "WAFIPRestrictRuleScope",
]

publication.publish()

def _typecheckingstub__b7effff35cda2ec5c68fc5091d88259103726628a8e720f9588fb2aee3226eed(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_ip_addresses: typing.Sequence[builtins.str],
    priority: jsii.Number,
    scope: WAFIPRestrictRuleScope,
    allow_ip_set_name: typing.Optional[builtins.str] = None,
    cloud_watch_metrics_name: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806fc823d81f071a81d15d8b650b27177eadf1fd6470404d2e6da0d461383624(
    *,
    allow_ip_addresses: typing.Sequence[builtins.str],
    priority: jsii.Number,
    scope: WAFIPRestrictRuleScope,
    allow_ip_set_name: typing.Optional[builtins.str] = None,
    cloud_watch_metrics_name: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
