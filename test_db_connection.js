const { Pool } = require('pg');

async function testConnection() {
  const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'medical_imaging',
    password: 'Sibo25mana',
    port: 5432,
    ssl: false
  });

  try {
    const result = await pool.query('SELECT NOW()');
    console.log('Database connection: SUCCESS');
    console.log('Current time:', result.rows[0].now);
    await pool.end();
    return true;
  } catch (error) {
    console.error('Database connection: FAILED');
    console.error('Error:', error.message);
    return false;
  }
}

testConnection().then(success => {
  if (success) {
    console.log('PostgreSQL authentication: WORKING');
  } else {
    console.log('PostgreSQL authentication: FAILED');
  }
});
