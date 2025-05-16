 
const mongoose = require('mongoose');

const jobSchema = new mongoose.Schema({
  title: String,
  description: String,
  requiredSkills: [String],
});

module.exports = mongoose.model('Job', jobSchema);
