r'''
# redis-cloud-peering

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Redis::Cloud::Peering` v1.0.0.

## Description

CloudFormation template for Subscription Peering.

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Redis::Cloud::Peering \
  --publisher-id 991a427d4922adc55ddc491f1a3a0421a61120bc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/991a427d4922adc55ddc491f1a3a0421a61120bc/Redis-Cloud-Peering \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Redis::Cloud::Peering`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fredis-cloud-peering+v1.0.0).
* Issues related to `Redis::Cloud::Peering` should be reported to the [publisher](undefined).

## License

Distributed under the Apache-2.0 License.
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
import constructs as _constructs_77d1e7e8


class CfnPeering(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/redis-cloud-peering.CfnPeering",
):
    '''A CloudFormation ``Redis::Cloud::Peering``.

    :cloudformationResource: Redis::Cloud::Peering
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subscription_id: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        base_url: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        vpc_cidr: typing.Optional[builtins.str] = None,
        vpc_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        vpc_network_name: typing.Optional[builtins.str] = None,
        vpc_project_uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Redis::Cloud::Peering``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subscription_id: [Required]. The ID of the Pro Subscription that will make a peering connection. Example: 163199
        :param aws_account_id: [Required for AWS]. AWS Account uid. Example: 178919255286
        :param base_url: [Required]. The Base URL where the API calls are sent.
        :param provider: [Optional]. Cloud provider. Example: AWS. Default: 'AWS'
        :param region: [Required for AWS]. Deployment region as defined by cloud provider. Example: us-east-1
        :param vpc_cidr: [Optional]. VPC CIDR. Example: '10.10.10.0/24'
        :param vpc_cidrs: [Optional]. List of VPC CIDRs. Example: '[10.10.10.0/24,10.10.20.0/24]'
        :param vpc_id: [Required for AWS]. VPC uid. Example: vpc-00e1a8cdca658ce8c
        :param vpc_network_name: [Required for GCP]. VPC network name.
        :param vpc_project_uid: [Required for GCP]. VPC project uid.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062623f60bb1f8062f7e8536f415b16c6788e78742d888d9cb4b04c60acd8cfb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPeeringProps(
            subscription_id=subscription_id,
            aws_account_id=aws_account_id,
            base_url=base_url,
            provider=provider,
            region=region,
            vpc_cidr=vpc_cidr,
            vpc_cidrs=vpc_cidrs,
            vpc_id=vpc_id,
            vpc_network_name=vpc_network_name,
            vpc_project_uid=vpc_project_uid,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPeeringID")
    def attr_peering_id(self) -> builtins.str:
        '''Attribute ``Redis::Cloud::Peering.PeeringID``.

        :link: http://unknown-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPeeringID"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnPeeringProps":
        '''Resource props.'''
        return typing.cast("CfnPeeringProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/redis-cloud-peering.CfnPeeringProps",
    jsii_struct_bases=[],
    name_mapping={
        "subscription_id": "subscriptionId",
        "aws_account_id": "awsAccountId",
        "base_url": "baseUrl",
        "provider": "provider",
        "region": "region",
        "vpc_cidr": "vpcCidr",
        "vpc_cidrs": "vpcCidrs",
        "vpc_id": "vpcId",
        "vpc_network_name": "vpcNetworkName",
        "vpc_project_uid": "vpcProjectUid",
    },
)
class CfnPeeringProps:
    def __init__(
        self,
        *,
        subscription_id: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        base_url: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        vpc_cidr: typing.Optional[builtins.str] = None,
        vpc_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        vpc_network_name: typing.Optional[builtins.str] = None,
        vpc_project_uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CloudFormation template for Subscription Peering.

        :param subscription_id: [Required]. The ID of the Pro Subscription that will make a peering connection. Example: 163199
        :param aws_account_id: [Required for AWS]. AWS Account uid. Example: 178919255286
        :param base_url: [Required]. The Base URL where the API calls are sent.
        :param provider: [Optional]. Cloud provider. Example: AWS. Default: 'AWS'
        :param region: [Required for AWS]. Deployment region as defined by cloud provider. Example: us-east-1
        :param vpc_cidr: [Optional]. VPC CIDR. Example: '10.10.10.0/24'
        :param vpc_cidrs: [Optional]. List of VPC CIDRs. Example: '[10.10.10.0/24,10.10.20.0/24]'
        :param vpc_id: [Required for AWS]. VPC uid. Example: vpc-00e1a8cdca658ce8c
        :param vpc_network_name: [Required for GCP]. VPC network name.
        :param vpc_project_uid: [Required for GCP]. VPC project uid.

        :schema: CfnPeeringProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed2d936d63880b2f8c659c29ec5117c898c28a54cfba68937d87d19a9a4ded6)
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument vpc_cidr", value=vpc_cidr, expected_type=type_hints["vpc_cidr"])
            check_type(argname="argument vpc_cidrs", value=vpc_cidrs, expected_type=type_hints["vpc_cidrs"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument vpc_network_name", value=vpc_network_name, expected_type=type_hints["vpc_network_name"])
            check_type(argname="argument vpc_project_uid", value=vpc_project_uid, expected_type=type_hints["vpc_project_uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subscription_id": subscription_id,
        }
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if base_url is not None:
            self._values["base_url"] = base_url
        if provider is not None:
            self._values["provider"] = provider
        if region is not None:
            self._values["region"] = region
        if vpc_cidr is not None:
            self._values["vpc_cidr"] = vpc_cidr
        if vpc_cidrs is not None:
            self._values["vpc_cidrs"] = vpc_cidrs
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id
        if vpc_network_name is not None:
            self._values["vpc_network_name"] = vpc_network_name
        if vpc_project_uid is not None:
            self._values["vpc_project_uid"] = vpc_project_uid

    @builtins.property
    def subscription_id(self) -> builtins.str:
        '''[Required].

        The ID of the Pro Subscription that will make a peering connection. Example: 163199

        :schema: CfnPeeringProps#SubscriptionID
        '''
        result = self._values.get("subscription_id")
        assert result is not None, "Required property 'subscription_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''[Required for AWS].

        AWS Account uid. Example: 178919255286

        :schema: CfnPeeringProps#AwsAccountId
        '''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''[Required].

        The Base URL where the API calls are sent.

        :schema: CfnPeeringProps#BaseUrl
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        Cloud provider. Example: AWS. Default: 'AWS'

        :schema: CfnPeeringProps#Provider
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''[Required for AWS].

        Deployment region as defined by cloud provider. Example: us-east-1

        :schema: CfnPeeringProps#Region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_cidr(self) -> typing.Optional[builtins.str]:
        '''[Optional].

        VPC CIDR. Example:  '10.10.10.0/24'

        :schema: CfnPeeringProps#VpcCidr
        '''
        result = self._values.get("vpc_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''[Optional].

        List of VPC CIDRs. Example: '[10.10.10.0/24,10.10.20.0/24]'

        :schema: CfnPeeringProps#VpcCidrs
        '''
        result = self._values.get("vpc_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''[Required for AWS].

        VPC uid. Example: vpc-00e1a8cdca658ce8c

        :schema: CfnPeeringProps#VpcId
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_network_name(self) -> typing.Optional[builtins.str]:
        '''[Required for GCP].

        VPC network name.

        :schema: CfnPeeringProps#VpcNetworkName
        '''
        result = self._values.get("vpc_network_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_project_uid(self) -> typing.Optional[builtins.str]:
        '''[Required for GCP].

        VPC project uid.

        :schema: CfnPeeringProps#VpcProjectUid
        '''
        result = self._values.get("vpc_project_uid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPeeringProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnPeering",
    "CfnPeeringProps",
]

publication.publish()

def _typecheckingstub__062623f60bb1f8062f7e8536f415b16c6788e78742d888d9cb4b04c60acd8cfb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subscription_id: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    base_url: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    vpc_cidr: typing.Optional[builtins.str] = None,
    vpc_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    vpc_network_name: typing.Optional[builtins.str] = None,
    vpc_project_uid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed2d936d63880b2f8c659c29ec5117c898c28a54cfba68937d87d19a9a4ded6(
    *,
    subscription_id: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    base_url: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    vpc_cidr: typing.Optional[builtins.str] = None,
    vpc_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    vpc_network_name: typing.Optional[builtins.str] = None,
    vpc_project_uid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
