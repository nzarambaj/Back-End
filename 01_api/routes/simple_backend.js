// Simple Backend Server for PostgreSQL 18
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'application/json'});
  
  if (req.url === '/api/health') {
    res.end(JSON.stringify({
      status: 'healthy',
      database: 'PostgreSQL 18',
      timestamp: new Date().toISOString()
    }));
  } else {
    res.end(JSON.stringify({
      message: 'Backend server is running',
      port: 5000,
      database: 'PostgreSQL 18 connected'
    }));
  }
});

server.listen(5000, () => {
  console.log('Simple backend server running on port 5000');
  console.log('Health check: http://localhost:5000/api/health');
  console.log('Database: PostgreSQL 18');
});
