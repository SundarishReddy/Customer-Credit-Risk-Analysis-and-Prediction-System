import React, { useState } from 'react'
import axios from 'axios'

const DEFAULT_FEATURES = {
  LIMIT_BAL: 20000,
  SEX: "2",
  EDUCATION: "2",
  MARRIAGE: "1",
  AGE: 30,
  PAY_0: "0",
  PAY_2: "0",
  PAY_3: "0",
  PAY_4: "0",
  PAY_5: "0",
  PAY_6: "0",
  BILL_AMT1: 0,
  BILL_AMT2: 0,
  BILL_AMT3: 0,
  BILL_AMT4: 0,
  BILL_AMT5: 0,
  BILL_AMT6: 0,
  PAY_AMT1: 0,
  PAY_AMT2: 0,
  PAY_AMT3: 0,
  PAY_AMT4: 0,
  PAY_AMT5: 0,
  PAY_AMT6: 0
}

export default function App(){
  const [form, setForm] = useState(DEFAULT_FEATURES)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try{
      const res = await axios.post('http://localhost:8000/predict', { data: form })
      setResult(res.data)
    }catch(err){
      alert(err?.response?.data?.detail || err.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div style={{maxWidth:800, margin:'0 auto', padding:20}}>
      <h1>Credit Default Risk</h1>
      <form onSubmit={submit}>
        {Object.keys(DEFAULT_FEATURES).map(key => (
          <div key={key} style={{marginBottom:8}}>
            <label style={{display:'block', fontWeight:600}}>{key}</label>
            <input name={key} value={form[key]} onChange={handleChange} style={{width:'100%', padding:8}} />
          </div>
        ))}
        <button type="submit" disabled={loading} style={{padding:'10px 20px'}}>{loading ? 'Predicting...' : 'Predict'}</button>
      </form>

      {result && (
        <div style={{marginTop:20}}>
          <h2>Result</h2>
          <p>Prediction (0 = no default, 1 = default): <strong>{result.prediction}</strong></p>
          <p>Default probability: <strong>{(result.probability*100).toFixed(2)}%</strong></p>
        </div>
      )}
    </div>
  )
}
