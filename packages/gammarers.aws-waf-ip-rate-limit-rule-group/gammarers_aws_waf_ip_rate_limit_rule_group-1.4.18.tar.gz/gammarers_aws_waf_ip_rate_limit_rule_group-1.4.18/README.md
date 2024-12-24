# AWS WAF(V2) IP Rete Limit Rule Group

[![GitHub](https://img.shields.io/github/license/gammarers/aws-waf-ip-rate-limit-rule-group?style=flat-square)](https://github.com/gammarers/aws-waf-ip-rate-limit-rule-group/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-waf-ip-rate-limit-rule-group?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-waf-ip-rate-limit-rule-group)
[![PyPI](https://img.shields.io/pypi/v/gammarers.aws-waf-ip-rate-limit-rule-group?style=flat-square)](https://pypi.org/project/gammarers.aws-waf-ip-rate-limit-rule-group/)
[![Nuget](https://img.shields.io/nuget/v/Gammarers.CDK.AWS.WafIpRateLimitRuleGroup?style=flat-square)](https://www.nuget.org/packages/Gammarers.CDK.AWS.WafIpRateLimitRuleGroup/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-waf-ip-rate-limit-rule-group/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-waf-ip-rate-limit-rule-group/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-waf-ip-rate-limit-rule-group?sort=semver&style=flat-square)](https://github.com/gammarers/aws-waf-ip-rate-limit-rule-group/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarers/aws-waf-ip-rate-limit-rule-group)](https://constructs.dev/packages/@gammarers/aws-waf-ip-rate-limit-rule-group)

This is an AWS CDK Construct for IP Rate Limit Rule on WAF V2

## Resources

This construct creating resource list.

* WAF V2 RuleGroup

## Install

### TypeScript

```shell
# or

```

#### install by npm

```shell
npm install @gammarers/aws-waf-ip-rate-limit-rule-group
```

#### install by yarn

```shell
yarn add @gammarers/aws-waf-ip-rate-limit-rule-group
```

#### install by pnpm

```shell
pnpm add @gammarers/aws-waf-ip-rate-limit-rule-group
```

#### install by bun

```shell
bun add @gammarers/aws-waf-ip-rate-limit-rule-group
```

### Python

```shell
pip install gammarers.aws-waf-ip-rate-limit-rule-group
```

### C# / .Net

```shell
dotnet add package Gammarers.CDK.AWS.WafIpRateLimitRuleGroup
```

## Example

```python
import { Scope, WafRateLimitRuleGroup } from '@gammarers/aws-waf-ip-rate-limit-rule-group';

new WafIpRateLimitRuleGroup(stack, 'WafIpRateLimitRuleGroup', {
  name: 'rate-limit-rule-group',
  scope: Scope.REGIONAL,
  rateLimitCount: 3000, // default 1000
});
```

## License

This project is licensed under the Apache-2.0 License.
