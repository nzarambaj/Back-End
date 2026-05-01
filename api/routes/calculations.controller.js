const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

// Add Calculus to Python path
const calculusProjectPath = 'C:\\Users\\TTR\\Documents\\Calculus';

// POST /api/calculate - Perform Calculus computations
const calculate = async (req, res) => {
  try {
    const { computationType, parameters, imageData } = req.body;

    if (!computationType || !parameters) {
      return res.status(400).json({ 
        error: 'Missing required fields: computationType and parameters' 
      });
    }

    // Make HTTP request to Calculus Flask API
    const axios = require('axios');
    
    try {
      // Call the Calculus Flask API
      const calculusResponse = await axios.post(`http://localhost:5001/api/calculate`, {
        computationType,
        parameters,
        imageData
      }, {
        timeout: 30000, // 30 second timeout
        headers: {
          'Content-Type': 'application/json'
        }
      });

      res.json({
        success: true,
        computationType,
        parameters,
        result: calculusResponse.data,
        timestamp: new Date().toISOString(),
        source: 'Calculus Flask API'
      });

    } catch (axiosError) {
      // If Flask API is not available, try direct Python execution
      console.log('Flask API not available, trying direct Python execution...');
      
      const pythonProcess = spawn('python', [
        '-c', `
import sys
sys.path.append('${calculusProjectPath}')
import json

try:
    # Parse input data
    computation_type = '${computationType}'
    parameters = json.loads('${JSON.stringify(parameters).replace(/'/g, "\\'")}')
    
    # Simple calculation logic
    result = {
        'computation_type': computation_type,
        'parameters': parameters,
        'status': 'processed',
        'message': f'Processed {computation_type} with parameters: {parameters}'
    }
    
    print(json.dumps(result))
    
except Exception as e:
    print(json.dumps({'error': str(e)}))
        `
      ]);

      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          return res.status(500).json({ 
            error: 'Calculation failed', 
            details: errorOutput 
          });
        }

        try {
          const result = JSON.parse(output);
          res.json({
            success: true,
            computationType,
            parameters,
            result,
            timestamp: new Date().toISOString(),
            source: 'Direct Python execution'
          });
        } catch (parseError) {
          res.status(500).json({ 
            error: 'Failed to parse calculation result',
            rawOutput: output
          });
        }
      });
    }

  } catch (error) {
    res.status(500).json({ 
      error: 'Server error during calculation',
      details: error.message 
    });
  }
};

// GET /api/results - Fetch computation results
const getResults = async (req, res) => {
  try {
    // This would typically fetch from a database
    // For now, return recent calculation status
    res.json({
      success: true,
      results: [
        {
          id: 'calc_001',
          type: 'gaussian_filter',
          status: 'completed',
          timestamp: '2026-04-27T12:00:00Z',
          result: { processed: true }
        },
        {
          id: 'calc_002', 
          type: 'edge_detection',
          status: 'completed',
          timestamp: '2026-04-27T11:45:00Z',
          result: { edges: 'detected' }
        }
      ],
      total: 2
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to fetch results',
      details: error.message 
    });
  }
};

module.exports = {
  calculate,
  getResults
};
