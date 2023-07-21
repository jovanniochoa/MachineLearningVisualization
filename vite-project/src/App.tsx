import { useState } from 'react'
import './App.css';
import './Button.css';
import Navbar from './component/Navbar';
import TileCard from './TileCard';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>{count}</h1>
      <button className = "button glow-button " onClick={() => setCount((prevCount) => prevCount - 1)}>
        -
      </button>
      <button className = "button glow-button " onClick={() => setCount(0)}>
        RESET
      </button>
      <button className = "button glow-button " onClick={() => setCount((prevCount) => prevCount + 1)}>
        +
      </button>
      <Navbar />
      <TileCard />
    </>
  )
}

export default App
