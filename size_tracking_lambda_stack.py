from aws_cdk import (
    Stack,
    Duration,
    aws_s3_notifications as s3_notifications,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct

class SizeTrackingLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import existing DynamoDB table
        dynamodb_table = dynamodb.Table.from_table_name(
            self,
            "ImportedS3ObjectSizeHistory",
            table_name="cdk-S3-object-size-history"
        )

        # Import existing S3 bucket
        s3_bucket = s3.Bucket.from_bucket_name(
            self,
            "ImportedTMWTestBucket",
            bucket_name="cdk-tmw-testbucket"
        )

        # Lambda Function
        size_tracking_lambda = _lambda.Function(
            self,
            "SizeTrackingLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="size_tracking_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/size_tracking_lambda"),  # Folder containing Lambda code
            environment={
                "DYNAMODB_TABLE_NAME": dynamodb_table.table_name,
                "S3_BUCKET_NAME": s3_bucket.bucket_name
            },
            timeout=Duration.minutes(1)
        )

        # Define and attach full access policies for S3 and DynamoDB
        full_s3_policy = iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        full_dynamodb_policy = iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")

        size_tracking_lambda.role.add_managed_policy(full_s3_policy)
        size_tracking_lambda.role.add_managed_policy(full_dynamodb_policy)

        # Trigger Lambda on S3 "Object Created/Removed" events
        s3_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(size_tracking_lambda)
        )

        s3_bucket.add_event_notification(
            s3.EventType.OBJECT_REMOVED, 
            s3_notifications.LambdaDestination(size_tracking_lambda)
        )
