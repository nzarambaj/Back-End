const { Pool } = require('pg');

async function testPostgreSQLConnection() {
  const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'medical_imaging',
    password: 'Sibo25Mana',
    port: 5432,
    ssl: false,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
  });

  try {
    console.log('Testing PostgreSQL connection...');
    const result = await pool.query('SELECT NOW() as server_time, version() as version');
    console.log('PostgreSQL Connection: SUCCESS');
    console.log('Server Time:', result.rows[0].server_time);
    console.log('Version:', result.rows[0].version);
    
    // Test table creation
    await pool.query(`
      CREATE TABLE IF NOT EXISTS doctors (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(200) NOT NULL,
        specialization VARCHAR(100),
        phone VARCHAR(20),
        email VARCHAR(100) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    console.log('Doctors table: READY');
    
    // Insert sample data
    const insertResult = await pool.query(`
      INSERT INTO doctors (full_name, specialization, phone, email) 
      VALUES ($1, $2, $3, $4) 
      ON CONFLICT (email) DO NOTHING
      RETURNING *
    `, ['Dr. Test Connection', 'Test Specialization', '555-1234', 'test.connection@medical.com']);
    
    if (insertResult.rows.length > 0) {
      console.log('Sample data inserted:', insertResult.rows[0].full_name);
    }
    
    // Test query
    const selectResult = await pool.query('SELECT COUNT(*) as count FROM doctors');
    console.log('Total doctors:', selectResult.rows[0].count);
    
    await pool.end();
    console.log('PostgreSQL Connection Test: COMPLETE');
    return true;
    
  } catch (error) {
    console.error('PostgreSQL Connection Test: FAILED');
    console.error('Error:', error.message);
    return false;
  }
}

testPostgreSQLConnection().then(success => {
  if (success) {
    console.log('PostgreSQL is ready for system integration');
  } else {
    console.log('PostgreSQL connection failed - using fallback');
  }
});
