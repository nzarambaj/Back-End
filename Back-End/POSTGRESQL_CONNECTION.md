# PostgreSQL Connection Setup

## 🐘 Quick Setup for Windows

You have PostgreSQL installed! Here's how to connect it to your Node.js backend:

### **Step 1: Add PostgreSQL to PATH**

Open Command Prompt and run:
```cmd
set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin
```

*Note: Adjust the path if you installed PostgreSQL to a different location*

### **Step 2: Create Database**

```cmd
psql -U postgres -c "CREATE DATABASE medical_imaging;"
```

If it asks for a password, enter the PostgreSQL password you set during installation.

### **Step 3: Create .env File**

Create a `.env` file in your `Back-End` folder with:

```env
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_imaging
DB_USER=postgres
DB_PASSWORD=your_postgresql_password

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_here_change_in_production
JWT_EXPIRES_IN=24h

# Server Configuration
PORT=5000
NODE_ENV=development

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

**Important:** Replace `your_postgresql_password` with your actual PostgreSQL password.

### **Step 4: Test Connection**

Run the setup script:
```cmd
setup_postgresql.bat
```

### **Step 5: Start Your Application**

```cmd
# Install dependencies
npm install

# Start development server
npm run dev
```

### **Step 6: Verify Connection**

Visit: `http://localhost:5000/api/health`

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2024-03-21T...",
  "version": "1.0.0",
  "database": "PostgreSQL",
  "environment": "development"
}
```

## 🔧 Troubleshooting

### **"psql not recognized" Error**
Add PostgreSQL to PATH permanently:
1. Search for "Environment Variables" in Windows
2. Click "Edit the system environment variables"
3. Click "Environment Variables"
4. Under "System variables", find "Path" and click "Edit"
5. Click "New" and add: `C:\Program Files\PostgreSQL\15\bin`
6. Click OK on all windows

### **Connection Failed**
1. Make sure PostgreSQL service is running
2. Check Windows Services for "postgresql-x64-15"
3. Verify your password in .env file

### **Database Already Exists**
That's fine! The application will use the existing database.

## 🚀 Alternative: Use pgAdmin

If you prefer a GUI:
1. Open pgAdmin (installed with PostgreSQL)
2. Connect to your PostgreSQL server
3. Right-click "Databases" → "Create" → "Database"
4. Name it: `medical_imaging`

## 📊 What Happens Next

When you start your Node.js application:
- ✅ It will automatically connect to PostgreSQL
- ✅ Create all necessary tables (patients, doctors, studies, images, users)
- ✅ Set up relationships between tables
- ✅ Be ready for API requests

**Your medical imaging backend will be fully operational with PostgreSQL!** 🎉
