# cdk version確認  (2.80.0はNG)
cdk --version
# cdk version最新化
npm install -g aws-cdk --force


# プロジェクト生成
mkdir url-short
cd url-short
cdk init --language python

# バーチャル環境有効化
source .venv/bin/activate

# 依存のPackageをインストール
# requirements.txt事前準備する必要がある
pip3 install -r requirements.txt

# CDK Bootstrap
# Error発生時に作成されたS3 Bucketを手動削除必要があるので注意
cdk bootstrap aws://290969947481/ap-northeast-1

cdk bootstrap aws://719253072179/us-east-1

# CDK deploy
cdk deploy



# Test
https://4jqn3pcnrj.execute-api.ap-northeast-1.amazonaws.com/prod/?targetUrl=https://www.kddi.com

Outputs:
UrlShortStack.apiEndpoint9349E63C = https://9ho6qre0x0.execute-api.us-east-1.amazonaws.com/prod/
UrlShortStack.monitoringWatchfulDashboard0D77215A = https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=monitoringDashboard9DC4C66B-te3Mr4PbjmBv




# 性能テストapp
mkdir pinger
cd pinger

cat > ping.sh <<EOL
#!/bin/sh
while true; do
  curl -i \$URL
  sleep 1
done
EOL

chmod +x ./ping.sh

# Test agin (remember to change the path)
URL=https://9ho6qre0x0.execute-api.us-east-1.amazonaws.com/prod/3817fdb8 ./ping.sh


# Create Docker file
cat > Dockerfile <<EOL
FROM adoptopenjdk/openjdk11:alpine 
RUN apk add curl
ADD ping.sh /ping.sh
CMD [ "/bin/sh", "/ping.sh" ]
EOL

# Build Docker Image
docker build -t pinger .

# Run docker local to test 
docker run -it -e URL=https://9ho6qre0x0.execute-api.us-east-1.amazonaws.com/prod/3817fdb8 pinger


# Code to create farget
# traffic.py追加 


# 
cd ..
cdk deploy --all


# Delete Stack
aws cloudformation describe-stacks --stack-name CDKToolkit --query "Stacks[0].Outputs[0].OutputValue"
# replace your bucket 
aws s3 rm s3://cdktoolkit-stagingbucket-yrlacd8hy29p --recursive
aws cloudformation delete-stack --stack-name CDKToolkit





#########################3
known issues
---------------------------
25714   (cli) cdk deploy fails when stacks share assets

        Overview: A single asset used in two stacks that depend on each other
                  causes 'cdk deploy' to exit early.

        Affected versions: cli: 2.80.0

        More information at: https://github.com/aws/aws-cdk/issues/25714





