import { useState } from "react"

// const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000" 
const API_URL = "https://flask-backend-production-c1c9.up.railway.app"

export default function App() {
  const [input, setInput] = useState("")
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  async function handleSubmit() {
  const words = input.split(",")
    .map(w => w.trim()) //delete the spaces
    .filter(Boolean) //elimina elementele nule daca exista
  const response = await fetch(`${API_URL}/api/anagrams`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ words })
  })
  setResult(await response.json())
}

async function handleHistory() {
  const response = await fetch(`${API_URL}/api/history`)
  setHistory(await response.json())
}

  return (
    <div>
      <h1>Group Anagram</h1>

      <input
        type="text"
        placeholder="ana, naa, ban, nab, dan"
        value={input}
        onChange={function (e) {
          setInput(e.target.value)
        }}
      />

      <button onClick={handleSubmit}>Process</button>

      {result && result.result.map((group, i) => (
        <div key={i}>{group.join(", ")}</div>
      ))}

      <hr />

      <button onClick={handleHistory}>History</button>

      <ul>
        {history.map((item) =>(
          <li key={item.id}>{item.words.join(", ") + "     ----   " + new Date(item.created_at).toLocaleString()}</li>
        ))}
      </ul>
    </div>
  )
}