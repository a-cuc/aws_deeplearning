import { useState } from "react";
import {
  Container,
  Typography,
  Paper,
  Grid,
  Divider
} from "@mui/material";

import SimpleUpload from "./components/SimpleUpload";
import PredictionChart from "./components/PredictionChart";

export default function App() {
  const [prediction, setPrediction] = useState([]);
  const [inputData, setInputData] = useState(null);

  return (
    <Container maxWidth="lg" sx={{ mt: 5 }}>
      <Typography variant="h3" align="center" gutterBottom>
        Solar Energy Prediction
      </Typography>

      <Typography
        variant="subtitle1"
        align="center"
        color="text.secondary"
        gutterBottom
      >
        LSTM Inference using AWS Lambda
      </Typography>

      <Divider sx={{ mb: 4 }} />

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Upload Input
            </Typography>

            <SimpleUpload setPrediction={setPrediction} setInputData={setInputData} />
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Prediction
            </Typography>

            <PredictionChart prediction={prediction} inputData={inputData} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}