const express = require('express');
const router = express.Router();
const { calculate, getResults } = require('./calculations.controller');

// POST /api/calculate - Perform Calculus computations
router.post('/calculate', calculate);

// GET /api/results - Fetch computation results  
router.get('/results', getResults);

module.exports = router;
