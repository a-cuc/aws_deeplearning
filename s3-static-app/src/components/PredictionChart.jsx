import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';


export default function PredictionChart({ prediction, inputData }) {

    if (!prediction.length) {
        return <p>Upload a file to generate a prediction.</p>;
    }

    const hasTarget =
        inputData &&
        Array.isArray(inputData.target) &&
        inputData.target.length === prediction.length;

    const chartData = prediction.map((pred, index) => ({
        index,
        prediction: pred,
        target: hasTarget ? inputData.target[index] : null
    }));

    return (
        <ResponsiveContainer width="100%" height={450}>
            <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="index" />

                <YAxis />

                <Tooltip />

                <Legend />

                <Line
                    type="monotone"
                    dataKey="prediction"
                    name="Prediction"
                    stroke="#1976d2"
                    strokeWidth={2}
                    dot={false}
                />

                {hasTarget && (
                    <Line
                        type="monotone"
                        dataKey="target"
                        name="Target"
                        stroke="#d32f2f"
                        strokeWidth={2}
                        dot={false}
                    />
                )}
            </LineChart>
        </ResponsiveContainer>
    );
}