from aws_cdk import (
    Stack,
    aws_s3 as s3
)
from constructs import Construct

class S3ReplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a bucket
        bucket = s3.Bucket(
            self,
            "MyBucket",
            bucket_name="my-bucket-name"
        )

        # Get the underlying CloudFormation bucket resource
        cfn_bucket = bucket.node.default_child

        # Create a replication rule
        replication_rule = {
            "Id": "MyReplicationRule",
            "Prefix": "prefix/to/replicate",
            "Status": "Enabled",
            "Destination": {
                "Bucket": "arn:aws:s3:::my-replica-bucket",
                "StorageClass": "STANDARD_IA"
            }
        }

        replication_configuration = s3.CfnBucket.ReplicationConfigurationProperty(
            role="arn:aws:iam::123456789012:role/MyReplicationRole",
            rules = s3.CfnBucket.ReplicationRuleProperty(
                id="MyReplicationRule",
                status="Enabled",
                destination = s3.CfnBucket.ReplicationDestinationProperty(
                    bucket="arn:aws:s3:::my-replica-bucket"
                )
            )
        )
        cfn_bucket.add_property_override("ReplicationConfiguration", replication_configuration)

        # # Set the replication configuration on the CloudFormation bucket resource
        # cfn_bucket.add_property_override(
        #     "ReplicationConfiguration",
        #     {
        #         "Role": "arn:aws:iam::123456789012:role/MyReplicationRole",
        #         "Rules": [replication_rule]
        #     }
        # )