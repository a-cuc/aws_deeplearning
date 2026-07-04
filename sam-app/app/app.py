import joblib
import torch
from torch import nn
import json


device = "cpu"

# Defining the neural network architecture
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size, device=x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size, device=x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
model = LSTMModel(input_size=2, hidden_size=24, num_layers=2, output_size=1).to(device)

# Loading the trained model and scaler
model.load_state_dict(torch.load('/opt/ml/model/lstm_model.pth'))
scaler = joblib.load('/opt/ml/model/scaler.pkl')

""" Preprocessing input data for prediction
data_scaled = scaler.transform(raw_data)  # Example input data

"""




def lambda_handler(event, context): 
    # TODO: Consider input for preprocessing

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "predicted_result": prediction,
            }
        )
    }
