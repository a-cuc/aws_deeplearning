# Deploying AI Solutions with AWS

This is my attempt at learning AWS services by trying to create a static web application deployed at **S3** with **Lambda** and **API Gateway** for the inferencing API.

- AI Model is trained on [model_training.ipynb](model_training.ipynb)
- AWS Services are created using a SAM template in [/sam-app](sam-app) directory
- S3 static website is made through React+Vite in [/s3-static-app](s3-static-app) directory

For inference, the expected JSON format are 2 arrays for `AC_POWER` and `DC_POWER` with a count of 96 (data taken 15 mins for 24 hours), and `TOD_SIN` and `TOD_COS` which are time of day features:
```
{
    "AC_POWER" : [1.0, 2.0, ... , 96.0],
    "DC_POWER" : [1.0, 2.0, ... , 96.0],
    "TOD_SIN"  : [1.0, 2.0, ... , 96.0],
    "TOD_COS"  : [1.0, 2.0, ... , 96.0]
}
```
Sample data can be found in [/samples](samples) directory. Note that the sample file contains another feature called `target` which are the original values from the dataset, which is used for visualizing the difference between the model and actual output

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

Test the API functionality
```sh
sam local start-api
```

In a separate terminal, use cURL to invoke the API
```sh
curl -X POST \
  http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d @samples/sample_0.json
```

Or, use the web app directly
```sh
cd s3-static-app
npm run dev
```

Modify [SimpleUpload.jsx](./s3-static-app/src/components/SimpleUpload.jsx) to point the API locally:
```jsx
const response = await fetch('http://localhost:3000/predict', {
  method: 'POST',
  body: fileContent,
});
```

## Deployment

1. Build the container thru the commands below:
```sh
cd sam-app
sam build
```
2. Deploy using the script:
```sh
cd ../
./deploy
```