const express = require("express");
const mongoose = require("mongoose");
const { exec } = require("child_process");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Schema
const trendSchema = new mongoose.Schema({
    uniqueID: String,
    trend1: String,
    trend2: String,
    trend3: String,
    trend4: String,
    trend5: String,
    timestamp: Date,
    ipAddress: String,
});
const Trend = mongoose.model("Trend", trendSchema);

// Function to start the server after MongoDB connects
const startServer = async () => {
    try {
        // MongoDB Connection
        await mongoose.connect(process.env.MONGO_URI);
        console.log("Connected to MongoDB");

        // Run Selenium Script Endpoint
        app.get("/run-script", (req, res) => {
            exec("python ../scrapper/selenium_script.py", (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error: ${stderr}`);
                    return res.status(500).send("Error running Selenium script.");
                }
                res.send("Script executed successfully!");
            });
        });

        // Fetch Latest Trends Endpoint
        app.get("/get-latest", async (req, res) => {
            try {
                const latestRecord = await Trend.findOne().sort({ _id: -1 });
                if (!latestRecord) return res.status(404).send("No data found.");
                res.json(latestRecord);
            } catch (error) {
                res.status(500).send("Error fetching data.");
            }
        });

        // Start the server
        app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
    } catch (error) {
        console.error("Error connecting to MongoDB:", error);
        process.exit(1); // Exit process with failure
    }
};

// Start the server only after MongoDB connection is established
startServer();
