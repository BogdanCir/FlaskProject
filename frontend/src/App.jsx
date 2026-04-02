import { useState } from "react"

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000" 
// const API_URL = "https://flask-backend-production-c1c9.up.railway.app"

export default function App() {
  const [input, setInput] = useState("")
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [error, setError] = useState(null)

  // filter by word and sort history
  const [historyWord, setHistoryWord] = useState("")
  const [historySort, setHistorySort] = useState("desc") // by default it would be desc

  async function handleSubmit() {
  const words = input.split(",")
    .map(w => w.trim()) //delete the spaces
    .filter(Boolean) //elimina elementele nule daca exista

  if(words.length === 0){
    setError("Enter at least one word")
    return
  }


  try{
    const response = await fetch(`${API_URL}/api/anagrams`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ words })
    })
    const data = await response.json()

    if (!response.ok) {
      setError(data.error || "Server error")
      return
    }
    setResult(data)
    setError(null)
  }catch{
    setError("Could not connect to the server")
  }
  }

async function handleHistory(filters={}) {
  try {
    const params = new URLSearchParams()

    if(filters.word){params.append("word", filters.word)}
    if(filters.sort){params.append("sort", filters.sort)}

    const url = `${API_URL}/api/history${params.toString() ? `?${params.toString()}` : ""}`
    const response = await fetch(url)
    // const response = await fetch(`${API_URL}/api/history`)
    if (!response.ok){throw new Error("Failed to load history")}
    setHistory(await response.json())
    setError(null)
  }catch{
    setError("Could not load history")
  }
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
          if(error) setError(null)
        }}
      />

      <button onClick={handleSubmit}>Process</button>

      {error && <p className="error">{error}</p>}
      
      {result && result.seen && (<p className="seen">Result loaded from db</p>)}

      {result && result.result.map((group, i) => (
        <div key={i}>{group.join(", ")}</div>
      ))}

      <hr />

      <h2>History Filters</h2>
      <input 
      type="text"
      placeholder="search word"
      value={historyWord}
      onChange={(e) => setHistoryWord(e.target.value)}
      />

      <select
        value={historySort}
        onChange={(e) => setHistorySort(e.target.value)}
      >
        <option value="desc">Newest first</option>
        <option value="asc">Oldest first</option>
      </select>

      <button onClick={() => handleHistory({
        word: historyWord,
        sort: historySort
      })}>History</button>

      <ul>
        {history.map((item) =>(
          <li key={item.id}>{item.words.join(", ") + "     ----   " + new Date(item.created_at).toLocaleString()}</li>
        ))}
      </ul>
    </div>
  )
}