from aws_cdk import Stack, RemovalPolicy
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct

class ResourcesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the S3 bucket with a unique name
        s3_bucket = s3.Bucket(
            self,
            "TMWTestBucket",
            bucket_name="cdk-tmw-testbucket",  # Updated unique name
            removal_policy=RemovalPolicy.DESTROY  # Use RETAIN for production
        )

        # Create the DynamoDB table with a unique name
        dynamodb_table = dynamodb.Table(
            self,
            "S3ObjectSizeHistory",
            table_name="cdk-S3-object-size-history",  # Updated unique name
            partition_key=dynamodb.Attribute(name="bucket_name", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="timestamp", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # Use RETAIN for production
        )

        # Output resource names for confirmation
        print(f"S3 bucket '{s3_bucket.bucket_name}' and DynamoDB table '{dynamodb_table.table_name}' created successfully.")
