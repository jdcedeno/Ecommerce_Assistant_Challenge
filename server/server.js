const express = require("express");
const { execFile, exec } = require("child_process");
const path = require("path");

const app = express();
const PORT = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Endpoint to handle queries
app.post("/query", (req, res) => {
  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: "Query is required" });
  }

  const scriptPath = path.join(__dirname, "rag_qa_llm", "query_llm.py");

  execFile("python3", [scriptPath, query], (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error.message}`);
      return res.status(500).json({ error: "Failed to process query" });
    }

    if (stderr) {
      console.error(`Script stderr: ${stderr}`);
      return res.status(500).json({ error: "Error during script execution" });
    }

    // Return the script's output
    res.status(200).json({ response: stdout.trim() });
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
