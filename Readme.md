# Deploying AI Solutions with AWS

This is my attempt at learning AWS services by trying to create a static web application deployed at **S3** with **Lambda** and **API Gateway** for the inferencing API.

- AI Model is trained on [model_training.ipynb](model_training.ipynb)
- AWS Services are created using a SAM template in [/sam-app](sam-app) directory

For inference, the expected JSON format are 2 arrays for `AC_POWER` and `DC_POWER` with a count of 96 (data taken 15 mins for 24 hours):
```
{
    "AC_POWER" : [1.0, 2.0, ... , 96.0],
    "DC_POWER" : [1.0, 2.0, ... , 96.0]
}
```
Sample data can be found in [/samples](samples) directory

## Trying it out locally

Build the container
```sh
cd sam-app
sam build
```

Start the lambda function locally
```sh
sam local start-lambda
```

In a separate terminal, invoke the lambda function
```sh
aws lambda invoke --function-name "InferenceFunction" \
--endpoint-url "http://127.0.0.1:3001" \
--no-verify-ssl --payload "file://samples/sample_0.json" \
--cli-binary-format "raw-in-base64-out" out.txt
```