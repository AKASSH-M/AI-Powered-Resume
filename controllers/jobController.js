 
const Job = require('../models/Job');

exports.createJob = async (req, res) => {
  try {
    const { title, description, requiredSkills } = req.body;

    const job = new Job({ title, description, requiredSkills });
    await job.save();

    res.status(201).json({ message: 'Job created', job });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
