// app.js
const express = require('express');
const cors = require('cors');
const userRoutes = require('./routes/userRoutes');
const resumeRoutes = require('./routes/resumeRoutes');
const jobRoutes = require('./routes/jobRoutes');
const { errorHandler } = require('./middlewares/errorHandler');

const app = express();

app.use(cors());
app.use(express.json());

// Define the root route
app.get('/', (req, res) => {
  res.send('Welcome to the AI-Powered Resume API');
});

app.use('/api/users', userRoutes);
app.use('/api/resumes', resumeRoutes);
app.use('/api/jobs', jobRoutes);

app.use(errorHandler);

module.exports = app;
