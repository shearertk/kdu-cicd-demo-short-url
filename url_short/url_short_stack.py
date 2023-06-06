#https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html
from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb,
    aws_lambda,
    aws_apigateway,
    aws_ec2,
    # aws_sqs as sqs,
)
from constructs import Construct
import aws_cdk as core
import os
from .traffic import Traffic
from cdk_watchful import Watchful

ACCOUNT= os.environ['CDK_DEFAULT_ACCOUNT']
REGION = os.environ['CDK_DEFAULT_REGION']
# replace your VPCID
VPC_ID = os.environ.get('TESTENV_VPC_ID', 'vpc-05a23b12d88559226')
AWS_ENV = core.Environment(account=ACCOUNT, region=REGION)

class UrlShortStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "UrlShortQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        
        # dynamo db
        table = aws_dynamodb.Table(
            self, 
            "mapping", 
            partition_key = aws_dynamodb.Attribute(name="id", type=aws_dynamodb.AttributeType.STRING))
        
        # Lambda
        function = aws_lambda.Function(
            self, 
            "backend", 
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="handler.main",\
            code=aws_lambda.Code.from_asset("./lambda")
            )
        
        # grant read to lambda
        table.grant_read_write_data(function)
        
        # add env-var in lambda
        function.add_environment("TABLE_NAME", table.table_name)
        
        # add api-gw to connect lambda
        api = aws_apigateway.LambdaRestApi(self, "api", handler=function)
        
        # add Watchful
        # replace your email
        wf = Watchful(self, 'monitoring', alarm_email='qiang.chen@accenture.com')
        wf.watch_scope(self)

        
class TrafficStack(Stack):
     
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, env=AWS_ENV, **kwargs)
         
        # lookup our pre-created VPC by ID
        vpc_env = aws_ec2.Vpc.from_lookup(self, "vpc",
            vpc_id=VPC_ID)
 
        Traffic(self, 'TestTraffic',
            vpc= vpc_env,
            # replace your id and endpoint
            url="https://4jqn3pcnrj.execute-api.ap-northeast-1.amazonaws.com/prod/de437874",
            tps=15)


