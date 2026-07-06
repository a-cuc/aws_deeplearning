import { useState } from 'react'
import SimpleUpload from './components/SimpleUpload'
import PredictionChart from './components/PredictionChart'

function App() {
  const [prediction, setPrediction] = useState(null)

  return (
    <>
      <h1>Hello World</h1>
      <SimpleUpload setPrediction={setPrediction} />
      <PredictionChart prediction={prediction} />
    </>
  )
}

export default App
