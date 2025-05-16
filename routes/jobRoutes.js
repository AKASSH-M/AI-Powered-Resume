const express = require('express');
const router = express.Router();

// Example route
router.get('/', (req, res) => {
  res.send('Job route is working!');
});

module.exports = router;
