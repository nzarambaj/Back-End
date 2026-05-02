const { Pool } = require('pg');

async function createDatabase() {
  const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'postgres', // Connect to default database first
    password: 'Sibo25mana',
    port: 5432,
    ssl: false
  });

  try {
    // Create the medical_imaging database
    await pool.query('CREATE DATABASE medical_imaging');
    console.log('Database "medical_imaging" created successfully');
    
    await pool.end();
    
    // Test connection to the new database
    await testConnection();
    
  } catch (error) {
    if (error.code === '42P04') { // Database already exists
      console.log('Database "medical_imaging" already exists');
      await pool.end();
      await testConnection();
    } else {
      console.error('Error creating database:', error.message);
      await pool.end();
    }
  }
}

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
    await pool.end();
    return false;
  }
}

createDatabase();
