const express = require("express")
const axios = require("axios")
const cors = require("cors")


const app = express()
const port = process.env.SERVER_PORT || 3000

// Middleware
app.use(express.json())
app.use(cors())

// Endpoint that receives the user query from the client
app.post("/query", async (req, res) => {
  try {
    // Extract the query from the request body
    const { query } = req.body
    
    if (!query) {
      return res.status(400).json({ error: "Query parameter is required." })
    }

    // Call the query_llm_service at port 8000 using Axios
    const response = await axios.post(`${process.env.LLM_SERVICE_URL}/query`, {query: query})

    // Return the response from the LLM service back to the client
    res.json(response.data)
  } catch (error) {
    console.error("Error calling query_llm_service:", error.message)
    res.status(500).json({ error: "An error occurred while processing your request." })
  }
})

// Start the server
app.listen(port, () => {
  console.log(`Express server listening on port ${port}`)
})
