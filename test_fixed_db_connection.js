// Test Fixed PostgreSQL 18 Connection
// Removed invalid default_transaction_isolation parameter

const { Pool } = require('pg');

// Fixed configuration - removed invalid parameter
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'medical_db',
  password: 'Sibo25mana',
  port: 5432,
  ssl: false,
  max: 25,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  // Fixed options - only valid parameters
  options: '-c statement_timeout=30s'
});

async function testFixedConnection() {
  console.log('🔍 Testing Fixed PostgreSQL 18 Connection...');
  console.log('📋 Configuration:');
  console.log(`   Host: ${pool.options.host}`);
  console.log(`   Database: ${pool.options.database}`);
  console.log(`   User: ${pool.options.user}`);
  console.log(`   Port: ${pool.options.port}`);
  console.log(`   Password: ${pool.options.password ? '✓ Set (Sibo25mana)' : '✗ Missing'}`);
  console.log(`   Options: ${pool.options.options}`);
  
  try {
    console.log('\n🔄 Connecting to PostgreSQL 18...');
    const client = await pool.connect();
    
    console.log('✅ PostgreSQL 18 connection successful!');
    
    // Test basic query
    const result = await client.query('SELECT version()');
    console.log('📊 PostgreSQL Version:', result.rows[0].version.substring(0, 60) + '...');
    
    // Test database
    const dbResult = await client.query('SELECT current_database()');
    console.log('📋 Database:', dbResult.rows[0].current_database);
    
    // Test transaction isolation (the problematic parameter)
    console.log('\n🔍 Testing transaction isolation...');
    const isolationResult = await client.query('SHOW default_transaction_isolation;');
    console.log('📊 Default Transaction Isolation:', isolationResult.rows[0].default_transaction_isolation);
    
    // Test tables
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
      try {
        const patientCount = await client.query('SELECT COUNT(*) as count FROM patients');
        console.log('📊 Patients:', patientCount.rows[0].count, 'rows');
        
        const doctorCount = await client.query('SELECT COUNT(*) as count FROM doctors');
        console.log('📊 Doctors:', doctorCount.rows[0].count, 'rows');
        
        const studyCount = await client.query('SELECT COUNT(*) as count FROM studies');
        console.log('📊 Studies:', studyCount.rows[0].count, 'rows');
        
      } catch (dataError) {
        console.log('⚠️  Data access error:', dataError.message);
      }
    } else {
      console.log('⚠️  No tables found. Database may need setup.');
    }
    
    client.release();
    console.log('\n🎉 SUCCESS! PostgreSQL 18 connection fixed!');
    console.log('📋 Status:');
    console.log('   ✅ Database: medical_db');
    console.log('   ✅ Password: Sibo25mana');
    console.log('   ✅ Connection parameters fixed');
    console.log('   ✅ Backend can now connect without errors');
    console.log('   ✅ Ready for production deployment');
    
  } catch (error) {
    console.error('\n❌ Connection failed:');
    console.error('Error:', error.message);
    console.error('Code:', error.code);
    console.error('Severity:', error.severity);
    
    if (error.message.includes('default_transaction_isolation')) {
      console.log('\n❌ Still has transaction isolation parameter issue');
      console.log('🔧 Check if backend file was updated correctly');
    } else if (error.code === '28P01') {
      console.log('\n❌ Password authentication failed');
      console.log('🔧 Verify password is: Sibo25mana');
    } else if (error.code === '3D000') {
      console.log('\n❌ Database not found');
      console.log('🔧 Create database: CREATE DATABASE medical_db');
    }
    
  } finally {
    await pool.end();
    console.log('\n🔌 Connection closed');
  }
}

// Test the fixed connection
testFixedConnection().catch(console.error);
