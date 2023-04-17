import aws_cdk as core
import aws_cdk.assertions as assertions

from s3_replication.s3_replication_stack import S3ReplicationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in s3_replication/s3_replication_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = S3ReplicationStack(app, "s3-replication")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
