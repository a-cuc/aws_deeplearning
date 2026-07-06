import joblib
import torch
import torchao
from torch import nn
import json
import numpy as np
import base64


# Defining the neural network architecture
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size, device=x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size, device=x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
with torch.device('meta'):
    model = LSTMModel(input_size=4, hidden_size=24, num_layers=3, output_size=96)

# Loading the trained model and scaler
model.load_state_dict(torch.load('/opt/ml/model/quantized_pruned_lstm_model.pth', map_location=torch.device('cpu'), weights_only=False), assign=True)
model.to(torch.device('cpu')).eval()
scaler = joblib.load('/opt/ml/model/scaler.pkl')

def preprocess_input(ac_power, dc_power, tod_sin, tod_cos):
    if not all(len(arr) == 96 for arr in [ac_power, dc_power, tod_sin, tod_cos]):
        raise ValueError(
            "AC_POWER, DC_POWER, TOD_SIN, and TOD_COS must each contain exactly 96 values"
        )

    # Scale only AC_POWER and DC_POWER
    scaled_power = scaler.transform(
        np.column_stack((ac_power, dc_power))
    )

    # Append the time features (already in [-1, 1], so don't scale)
    X = np.column_stack((
        scaled_power,
        tod_sin,
        tod_cos
    ))

    return torch.tensor(X, dtype=torch.float32).unsqueeze(0)


def inverse_scale_ac_power(prediction_scaled):
    ac_min = scaler.data_min_[0]
    ac_max = scaler.data_max_[0]
    return prediction_scaled * (ac_max - ac_min) + ac_min




def lambda_handler(event, context): 

    # Check if the event contains a body (for API Gateway) or is a direct invocation
    if "body" in event:
        body_str = event["body"]
        if event.get("isBase64Encoded", True):
            body_str = base64.b64decode(body_str).decode('utf-8')  
        body = json.loads(body_str)
    else:
        body = event

    ac_power = body["AC_POWER"]
    dc_power = body["DC_POWER"]
    tod_sin = body["TOD_SIN"]
    tod_cos = body["TOD_COS"]

    X = preprocess_input(ac_power, dc_power, tod_sin, tod_cos).cpu()

    with torch.no_grad():
        prediction_scaled = model(X).cpu().numpy().ravel()

    prediction = inverse_scale_ac_power(prediction_scaled).tolist()

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "predicted_result": prediction,
            }
        ),
        'headers': { # CORS headers
            'Access-Control-Allow-Origin': '*',  # NOTE: Bad practice, should be restricted to your frontend domain in production
            'Access-Control-Allow-Methods': 'POST, OPTIONS',  # Allow POST and OPTIONS methods
            'Access-Control-Allow-Headers': 'Content-Type',  # Allow Content-Type header
        }
    }
