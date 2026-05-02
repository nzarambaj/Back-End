// Test PostgreSQL 18 connection with correct password: Sibo25mana

const { Pool } = require('pg');

// Use the CORRECT password
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'medical_db',
  password: 'Sibo25mana',  // CORRECT PASSWORD (lowercase 'm')
  port: 5432,
  ssl: false,
  connectionTimeoutMillis: 3000,
});

async function testCorrectPassword() {
  console.log('🔍 Testing PostgreSQL 18 with CORRECT password...');
  console.log('📋 Configuration:');
  console.log(`   Host: ${pool.options.host}`);
  console.log(`   Database: ${pool.options.database}`);
  console.log(`   User: ${pool.options.user}`);
  console.log(`   Port: ${pool.options.port}`);
  console.log(`   Password: ${pool.options.password ? '✓ Set (Sibo25mana)' : '✗ Missing'}`);
  
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
      
      // Get row counts
      console.log('\n📊 Table Statistics:');
      for (const row of tablesResult.rows) {
        try {
          const countResult = await client.query(`SELECT COUNT(*) as count FROM ${row.table_name}`);
          console.log(`   ${row.table_name}: ${countResult.rows[0].count} rows`);
        } catch (error) {
          console.log(`   ${row.table_name}: Cannot access`);
        }
      }
    } else {
      console.log('⚠️  No tables found. Database may need setup.');
    }
    
    client.release();
    console.log('\n🎉 SUCCESS! PostgreSQL 18 is working with correct password!');
    console.log('📋 Status:');
    console.log('   ✅ Database: medical_db');
    console.log('   ✅ Password: Sibo25mana (CORRECT)');
    console.log('   ✅ Backend can now connect');
    console.log('   ✅ Ready for production');
    
  } catch (error) {
    console.error('\n❌ Connection failed:');
    console.error('Error:', error.message);
    console.error('Code:', error.code);
    
    if (error.code === '28P01') {
      console.log('\n❌ Password authentication still failing');
      console.log('🔧 Double-check password is exactly: Sibo25mana');
    }
    
  } finally {
    await pool.end();
    console.log('\n🔌 Connection closed');
  }
}

// Test with correct password
testCorrectPassword().catch(console.error);
