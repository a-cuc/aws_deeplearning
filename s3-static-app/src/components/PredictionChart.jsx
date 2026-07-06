import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';


export default function PredictionChart({ prediction }) {
    if (!prediction || prediction.length === 0) {
        return <p>No prediction available.</p>;
    }

    const chartData = prediction.map((value, index) => ({
        index,
        prediction: value,
    }));

    return (
        <ResponsiveContainer width="100%" height={400}>
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
                    stroke="#8884d8"
                    dot={false}
                />
            </LineChart>
        </ResponsiveContainer>
    );
}