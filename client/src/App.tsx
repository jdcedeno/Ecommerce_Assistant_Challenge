import React, { useState } from "react"

interface ToolResult {
  status_code: number
  data: Record<string, unknown>[]
}

interface ServerResponse {
  llm_response: string
  tool_results: {
    [toolName: string]: ToolResult
  }
  answer: string
}

interface ChatEntry {
  query: string
  response?: ServerResponse
}

const App: React.FC = () => {
  const [query, setQuery] = useState<string>("")
  const [chatHistory, setChatHistory] = useState<ChatEntry[]>([])
  const [loading, setLoading] = useState<boolean>(false)

  const handleSend = async () => {
    if (!query.trim()) return

    // Add the user's query to the chat history
    const currentQuery = query
    setChatHistory((prev) => [...prev, { query: currentQuery }])
    setQuery("")
    setLoading(true)

    try {
      // Send POST request to the server /query endpoint
      const response = await fetch("http://localhost:3001/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: currentQuery }),
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data: ServerResponse = await response.json()

      // Update the last chat entry with the server response
      setChatHistory((prev) => {
        const newHistory = [...prev]
        newHistory[newHistory.length - 1].response = data
        return newHistory
      })
    } catch (error) {
      console.error("Error querying server:", error)
      // Optionally, update chat history with error details
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      style={{
        width: "90vw",
        margin: "auto",
        padding: "1rem",
        background: "#fff",
        borderRadius: "8px",
        boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
      }}
    >
      <h1 style={{ textAlign: "center" }}>Chat Client</h1>

      {/* Chat history display */}
      <div
        style={{
          border: "1px solid #ccc",
          padding: "1rem",
          height: "400px",
          overflowY: "auto",
          marginBottom: "1rem",
        }}
      >
        {chatHistory.map((entry, index) => (
          <div key={index} style={{ marginBottom: "1rem" }}>
            <div style={{ fontWeight: "bold" }}>You:</div>
            <div style={{ marginBottom: "0.5rem" }}>{entry.query}</div>
            {entry.response && (
              <div
                style={{
                  background: "#f4f4f4",
                  padding: "0.5rem",
                  borderRadius: "4px",
                }}
              >
                <div>
                  <strong>LLM Response:</strong> {entry.response.llm_response}
                </div>
                <div>
                  <strong>Answer:</strong> {entry.response.answer}
                </div>
                <div>
                  <strong>Tool Results:</strong>
                  <pre
                    style={{ whiteSpace: "pre-wrap", wordBreak: "break-all" }}
                  >
                    {JSON.stringify(entry.response.tool_results, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && <p>Loading...</p>}
      </div>

      {/* Input and Send Button */}
      <div style={{ display: "flex" }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSend()
          }}
          style={{ flexGrow: 1, padding: "0.5rem", fontSize: "1rem" }}
          placeholder="Enter your query..."
        />
        <button
          onClick={handleSend}
          style={{
            padding: "0.5rem 1rem",
            marginLeft: "0.5rem",
            fontSize: "1rem",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  )
}

export default App
