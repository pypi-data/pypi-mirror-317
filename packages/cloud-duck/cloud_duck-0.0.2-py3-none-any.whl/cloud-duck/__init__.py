r'''
<p align="center">
  <img src="src/frontend/public/icon.png" alt="CloudDuck Icon" style="max-width: 400px; max-height: 400px;" />
</p>

CloudDuck is a simple and easy-to-use analysis environment for S3 data, featuring DuckDB with built-in authentication.

<p align="center">
  <img src="images/cloudduck.gif" alt="CloudDuck Display Image" />
</p>

## Architecture

![Architecture](images/architecture.png)

## Installation

```bash
npm i cloud-duck
```

## Setup

### Deploy

```python
import { CloudDuck } from 'cloud-duck';

declare const logBucket: s3.IBucket;

new CloudDuck(this, 'CloudDuck', {
  // The S3 bucket to analyze
  // CloudDuck can access to all of the buckets in the account by default.
  // If you want to restrict the access, you can use the targetBuckets property.
  targetBuckets: [logBucket],
});
```

### Add user to the Cognito User Pool

Add user to the Cognito User Pool to access the CloudDuck.

```sh
aws cognito-idp admin-create-user \
--user-pool-id "us-east-1_XXXXX" \
--username "naonao@example.com" \
--user-attributes Name=email,Value="naonao@example.com" Name=email_verified,Value=true \
--message-action SUPPRESS \
--temporary-password Password1!
```

### Access

Access to the CloudDuck with the cloudfront URL.

```bash
❯ npx cdk deploy
...
AwsStack.CloudDuckDistributionUrl84FC8296 = https://dosjykpv096qr.cloudfront.net
Stack ARN:
arn:aws:cloudformation:us-east-1:123456789012:stack/AwsStack/dd0960c0-b3d5-11ef-bcfc-12cf7722116f

✨  Total time: 73.59s
```

Enter the username and password.

![Login](images/login.png)

When you log in at the first time, you need to change the password.

![Change Password](images/change-password.png)

Play with the CloudDuck!

![CloudDuck](images/home.png)

## Usage

### Query

You can query the S3 data with SQL.

```sql
SELECT * FROM read_csv_auto('s3://your-bucket-name/your-file.csv');
SELECT * FROM parquet_scan('s3://your-bucket-name/your-file.parquet');
```

Ofcourse, you can store the result as a new table.

```sql
CREATE TABLE new_table AS SELECT * FROM read_csv_auto('s3://your-bucket-name/your-file.csv');
```

### Persistence

All query results are persisted in individual DuckDB files for each user.
Therefore, you can freely save your query results without worrying about affecting other users.

### Note

CloudDuck is still under development. Updates may include breaking changes. If you encounter any bugs, please report them via issues.
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
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class CloudDuck(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cloud-duck.CloudDuck",
):
    '''The CloudDuck construct.

    This construct creates a serverless analysis environment using DuckDB for S3 data
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        memory: _aws_cdk_ceddda9d.Size,
        target_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.Bucket],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param memory: The amount of memory to allocate to the Lambda function. Default: - 1024 MiB
        :param target_buckets: The S3 buckets which the cloud duck will analyze. Default: - All buckets in the account
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a1bd8481ad382bf2de434f834d943837b048924a6a7fda2780116bdc8eb49e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudDuckProps(memory=memory, target_buckets=target_buckets)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cloud-duck.CloudDuckProps",
    jsii_struct_bases=[],
    name_mapping={"memory": "memory", "target_buckets": "targetBuckets"},
)
class CloudDuckProps:
    def __init__(
        self,
        *,
        memory: _aws_cdk_ceddda9d.Size,
        target_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.Bucket],
    ) -> None:
        '''Props for the CloudDuck construct.

        :param memory: The amount of memory to allocate to the Lambda function. Default: - 1024 MiB
        :param target_buckets: The S3 buckets which the cloud duck will analyze. Default: - All buckets in the account
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4870f9e8a524193de639c56e5437d7d75591e9e40d10dd1877bcb74bdba97e)
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument target_buckets", value=target_buckets, expected_type=type_hints["target_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory": memory,
            "target_buckets": target_buckets,
        }

    @builtins.property
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''The amount of memory to allocate to the Lambda function.

        :default: - 1024 MiB
        '''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Size, result)

    @builtins.property
    def target_buckets(self) -> typing.List[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        '''The S3 buckets which the cloud duck will analyze.

        :default: - All buckets in the account
        '''
        result = self._values.get("target_buckets")
        assert result is not None, "Required property 'target_buckets' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_s3_ceddda9d.Bucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudDuckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudDuck",
    "CloudDuckProps",
]

publication.publish()

def _typecheckingstub__10a1bd8481ad382bf2de434f834d943837b048924a6a7fda2780116bdc8eb49e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    memory: _aws_cdk_ceddda9d.Size,
    target_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.Bucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4870f9e8a524193de639c56e5437d7d75591e9e40d10dd1877bcb74bdba97e(
    *,
    memory: _aws_cdk_ceddda9d.Size,
    target_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.Bucket],
) -> None:
    """Type checking stubs"""
    pass
