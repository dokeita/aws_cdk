from aws_cdk import (
    Stack,
    aws_s3 as s3,
)
from constructs import Construct

class S3ReplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # バケット作成
        source_bucket = s3.Bucket(
            self,
            "s3-replication-source",
            bucket_name="s3-replicatoin-source-bucket-dokeita"
        )

        destination_bucket = s3.Bucket(
            self,
            "s3-replication-destination",
            bucket_name="s3-replicatoin-destination-bucket-dokeita"
        )

        # s3.BucketからCfnBucketの要素を取得
        cfn_bucket = source_bucket.node.default_child

        # CfnBucket.ReplicationRuleProperty作成
        replication_rule = {
            "Id": "s3-replication-rule",
            # "Prefix": "replication" #レプリケーション対象をパス指定する場合に必要
            "Status": "Enabled",
            "Destination": {
                "Bucket": "arn:aws:s3:::s3-replicatoin-destination-bucket-dokeita"
            }
        }

        #レプリケーションを行うIAMロール作成
        replication_role = iam.Role(
            app,
            "s3-replication-role",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com")
        )

        # CfnBucket.ReplicationConfigurationPropertyをCfnBucketに設定
        cfn_bucket.add_property_override(
            "ReplicationConfiguration",
            {
                "Role": "arn:aws:iam::123456789012:role/MyReplicationRole",
                "Rules": [replication_rule]
            }
        )

        #メモ 記事には下記記載
        # CfnBucket.ReplicationConfiguration()を使ってもダメよ（プロパティ名で怒られる）
        # s3.Bucket.bucket_arnは使えないよ（ビルドのタイミングでは変数になっているから）