const express = require('express');
const { exec } = require('child_process');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.post('/', (req, res) => {
    const { message } = req.body;

    if (!message) {
        return res.status(400).send('Message is required');
    }

    // Execute the Python script
    exec(`python3 script.py "${message}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send('Server error');
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.status(500).send('Error in Python script');
        }
        // Send the Python script's response back to the client
        res.send(stdout.trim());
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
