// PostgreSQL Database Connection Test
// Password: Sibo25Mana

const { Pool } = require('pg');

// Database configuration
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'medical_db',
  password: 'Sibo25Mana',
  port: 5432,
  ssl: false,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

async function testDatabaseConnection() {
  console.log('🔍 Testing PostgreSQL Database Connection...');
  console.log('📋 Configuration:');
  console.log(`   Host: ${pool.options.host}`);
  console.log(`   Database: ${pool.options.database}`);
  console.log(`   User: ${pool.options.user}`);
  console.log(`   Port: ${pool.options.port}`);
  console.log(`   Password: ${pool.options.password ? '✓ Set' : '✗ Missing'}`);
  
  try {
    // Test connection
    console.log('\n🔄 Connecting to database...');
    const client = await pool.connect();
    
    console.log('✅ Database connection successful!');
    
    // Test basic query
    console.log('\n🔍 Testing basic query...');
    const result = await client.query('SELECT version()');
    console.log('📊 PostgreSQL Version:', result.rows[0].version);
    
    // Test database exists
    console.log('\n🔍 Checking database structure...');
    const dbResult = await client.query('SELECT current_database()');
    console.log('📊 Current Database:', dbResult.rows[0].current_database);
    
    // List tables
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
    } else {
      console.log('⚠️  No tables found. You may need to run setup scripts.');
    }
    
    // Test sample data if tables exist
    if (tablesResult.rows.length > 0) {
      console.log('\n🔍 Testing sample data access...');
      
      // Try to get row counts
      for (const row of tablesResult.rows) {
        try {
          const countResult = await client.query(`SELECT COUNT(*) as count FROM ${row.table_name}`);
          console.log(`📊 ${row.table_name}: ${countResult.rows[0].count} rows`);
        } catch (error) {
          console.log(`⚠️  ${row.table_name}: Cannot access (${error.message})`);
        }
      }
    }
    
    // Release client
    client.release();
    console.log('\n✅ Database test completed successfully!');
    
  } catch (error) {
    console.error('\n❌ Database connection failed:');
    console.error('Error:', error.message);
    console.error('Code:', error.code);
    console.error('Severity:', error.severity);
    
    // Provide troubleshooting tips
    console.log('\n🔧 Troubleshooting:');
    console.log('1. Check if PostgreSQL is running');
    console.log('2. Verify password: Sibo25Mana');
    console.log('3. Check if database "medical_db" exists');
    console.log('4. Verify host and port settings');
    console.log('5. Check firewall/antivirus blocking');
    
    if (error.code === '3D000') {
      console.log('\n💡 Solution: Create database with: CREATE DATABASE medical_db;');
    } else if (error.code === '28P01') {
      console.log('\n💡 Solution: Check password and user credentials');
    } else if (error.code === 'ECONNREFUSED') {
      console.log('\n💡 Solution: Start PostgreSQL service');
    }
  } finally {
    // Close pool
    await pool.end();
    console.log('\n🔌 Database connection closed');
  }
}

// Run test
testDatabaseConnection().catch(console.error);
