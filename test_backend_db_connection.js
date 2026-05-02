// Test Backend Database Connection
// Verify PostgreSQL 18 connection with password Sibo25Mana

const { Pool } = require('pg');

// Use same configuration as backend
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'medical_db',
  password: 'Sibo25Mana',
  port: 5432,
  ssl: false,
  max: 25,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  options: '-c default_transaction_isolation=read_committed -c statement_timeout=30s'
});

async function testBackendDatabaseConnection() {
  console.log('🔍 Testing Backend Database Connection...');
  console.log('📋 Configuration:');
  console.log(`   Host: ${pool.options.host}`);
  console.log(`   Database: ${pool.options.database}`);
  console.log(`   User: ${pool.options.user}`);
  console.log(`   Port: ${pool.options.port}`);
  console.log(`   Password: ${pool.options.password ? '✓ Set (Sibo25Mana)' : '✗ Missing'}`);
  console.log(`   Max Connections: ${pool.options.max}`);
  
  try {
    console.log('\n🔄 Connecting to PostgreSQL 18...');
    const client = await pool.connect();
    
    console.log('✅ Backend database connection successful!');
    
    // Test basic query
    const result = await client.query('SELECT version()');
    console.log('📊 PostgreSQL Version:', result.rows[0].version.substring(0, 60) + '...');
    
    // Test database exists
    const dbResult = await client.query('SELECT current_database()');
    console.log('📋 Current Database:', dbResult.rows[0].current_database);
    
    // Test tables
    console.log('\n🔍 Checking tables...');
    const tablesResult = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      ORDER BY table_name
    `);
    
    if (tablesResult.rows.length > 0) {
      console.log('📋 Tables found:');
      tablesResult.rows.forEach(row => {
        console.log(`   - ${row.table_name}`);
      });
      
      // Test sample data access
      console.log('\n🔍 Testing data access...');
      for (const row of tablesResult.rows) {
        try {
          const countResult = await client.query(`SELECT COUNT(*) as count FROM ${row.table_name}`);
          console.log(`📊 ${row.table_name}: ${countResult.rows[0].count} rows`);
        } catch (error) {
          console.log(`⚠️  ${row.table_name}: Cannot access (${error.message})`);
        }
      }
    } else {
      console.log('⚠️  No tables found. Database may need setup.');
    }
    
    // Test backend-specific operations
    console.log('\n🔍 Testing backend operations...');
    
    // Test JSONB operations (for medical data)
    const jsonbTest = await client.query(`
      SELECT 
        '{"patient": "John Doe", "age": 45, "studies": ["MRI", "CT"]}'::jsonb as medical_data
    `);
    console.log('✅ JSONB Operations:', jsonbTest.rows[0].medical_data);
    
    // Test UUID operations
    const uuidTest = await client.query('SELECT uuid_generate_v4() as new_id');
    console.log('✅ UUID Generation:', uuidTest.rows[0].new_id);
    
    // Test timestamp operations
    const timestampTest = await client.query('SELECT CURRENT_TIMESTAMP as current_time');
    console.log('✅ Timestamp:', timestampTest.rows[0].current_time);
    
    client.release();
    console.log('\n🎉 Backend database test completed successfully!');
    console.log('📋 Backend Ready Status:');
    console.log('   ✅ PostgreSQL 18 connection');
    console.log('   ✅ Database: medical_db');
    console.log('   ✅ Password: Sibo25Mana');
    console.log('   ✅ JSONB operations');
    console.log('   ✅ UUID generation');
    console.log('   ✅ Timestamp operations');
    console.log('   ✅ Backend can serve API requests');
    
  } catch (error) {
    console.error('\n❌ Backend database connection failed:');
    console.error('Error:', error.message);
    console.error('Code:', error.code);
    
    console.log('\n🔧 Backend Troubleshooting:');
    console.log('1. Check PostgreSQL 18 service status');
    console.log('2. Verify password: Sibo25Mana');
    console.log('3. Ensure medical_db database exists');
    console.log('4. Run postgresql18_setup.sql if needed');
    
    if (error.code === '28P01') {
      console.log('\n💡 Password Authentication Failed');
      console.log('   Solution: Set postgres password to Sibo25Mana');
    } else if (error.code === '3D000') {
      console.log('\n💡 Database Not Found');
      console.log('   Solution: CREATE DATABASE medical_db');
    } else if (error.code === 'ECONNREFUSED') {
      console.log('\n💡 Connection Refused');
      console.log('   Solution: Start PostgreSQL 18 service');
    }
    
  } finally {
    await pool.end();
    console.log('\n🔌 Backend database connection closed');
  }
}

// Test backend database connection
testBackendDatabaseConnection().catch(console.error);
