const Resume = require('../models/Resume');

exports.uploadResume = async (req, res) => {
  try {
    const { userId, content } = req.body;

    const resume = new Resume({ userId, content });
    await resume.save();

    res.status(201).json({ message: 'Resume uploaded', resume });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

