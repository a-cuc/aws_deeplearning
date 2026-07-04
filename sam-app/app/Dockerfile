FROM public.ecr.aws/lambda/python:3.12

COPY app.py requirements.txt ./
COPY quantized_pruned_lstm_model.pth /opt/ml/model/
COPY scaler.pkl /opt/ml/model/

RUN python3.12 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
