import { useState } from 'react'
import './App.css'
import React from 'react' 

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>{count}</h1>
      <button onClick={() => (setCount(prevCount => prevCount - 1))}>
      -
      </button>
      <button onClick={() => (setCount(0))}>
      Reset
      </button>
      <button onClick={() => (setCount(prevCount => prevCount + 1))}>
      +
      </button>
    </>
  )
}

export default App
