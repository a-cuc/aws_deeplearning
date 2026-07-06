import joblib
import torch
from torchao.quantization import quantize_, Int8DynamicActivationInt8WeightConfig
from torch import nn
import json
import numpy as np



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
model = LSTMModel(input_size=2, hidden_size=24, num_layers=3, output_size=96).cpu()
quantize_(model, Int8DynamicActivationInt8WeightConfig())

# Loading the trained model and scaler
model.load_state_dict(torch.load('/opt/ml/model/quantized_pruned_lstm_model.pth', map_location=torch.device('cpu')))
scaler = joblib.load('/opt/ml/model/scaler.pkl')

def preprocess_input(ac_power, dc_power):
    if len(ac_power) != 96 or len(dc_power) != 96:
        raise ValueError("AC_POWER and DC_POWER must each contain exactly 96 values")

    raw_data = np.column_stack((ac_power, dc_power))
    scaled_data = scaler.transform(raw_data)
    return torch.tensor(scaled_data, dtype=torch.float32).unsqueeze(0)


def inverse_scale_ac_power(prediction_scaled):
    ac_min = scaler.data_min_[0]
    ac_max = scaler.data_max_[0]
    return prediction_scaled * (ac_max - ac_min) + ac_min




def lambda_handler(event, context): 
    # Console check for debugging
    print("Event:", json.dumps(event, indent=2))

    # Check if the event contains a body (for API Gateway) or is a direct invocation
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    ac_power = body["AC_POWER"]
    dc_power = body["DC_POWER"]

    X = preprocess_input(ac_power, dc_power).cpu()

    with torch.no_grad():
        prediction_scaled = model(X).cpu().numpy().ravel()

    prediction = inverse_scale_ac_power(prediction_scaled).tolist()

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "predicted_result": prediction,
            }
        )
    }
