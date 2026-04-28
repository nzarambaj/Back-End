# PostgreSQL Installation Guide for Medical Imaging Backend

## 🐘 PostgreSQL Installation

### **Option 1: Windows (Recommended)**

#### **Method A: Download Installer**
1. Go to [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Download PostgreSQL 15+ (latest stable version)
3. Run the installer with these settings:
   - **Password**: Set a memorable password (you'll need it for .env)
   - **Port**: 5432 (default)
   - **Components**: Include pgAdmin 4 (GUI tool)
   - **Stack Builder**: Uncheck (not needed)

#### **Method B: Chocolatey Package Manager**
```bash
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install PostgreSQL
choco install postgresql --params '/Password:your_password'
```

### **Option 2: macOS**

#### **Method A: Homebrew**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Create database user
createuser -s postgres
```

#### **Method B: Postgres.app**
1. Download from [https://postgresapp.com/](https://postgresapp.com/)
2. Install and start PostgreSQL
3. Initialize database cluster

### **Option 3: Linux (Ubuntu/Debian)**
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Set password for postgres user
sudo -u postgres psql
\password postgres
```

## 🗄️ Database Setup

### **1. Create Medical Imaging Database**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE medical_imaging;

# Create dedicated user (optional but recommended)
CREATE USER medical_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE medical_imaging TO medical_user;

# Exit
\q
```

### **2. Verify Connection**
```bash
# Test connection to your new database
psql -h localhost -p 5432 -U medical_user -d medical_imaging
```

## ⚙️ Environment Configuration

### **1. Copy Environment Template**
```bash
cd Back-End
cp .env.example .env
```

### **2. Update .env File**
```env
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_imaging
DB_USER=medical_user
DB_PASSWORD=your_secure_password

# Alternative: Full connection string
# DATABASE_URL=postgresql://medical_user:your_secure_password@localhost:5432/medical_imaging
```

## 🚀 Start the Application

### **1. Install Dependencies**
```bash
cd Back-End
npm install
```

### **2. Start the Server**
```bash
# Development
npm run dev

# Production
npm start
```

### **3. Verify Installation**
Visit: `http://localhost:5000/api/health`

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-03-21T10:30:00.000Z",
  "version": "1.0.0",
  "database": "PostgreSQL",
  "environment": "development"
}
```

## 🛠️ Database Management Tools

### **GUI Tools (Recommended)**
- **pgAdmin 4** (included with Windows installer)
- **DBeaver** (cross-platform, free)
- **DataGrip** (JetBrains, paid)
- **TablePlus** (macOS, paid)

### **Command Line**
```bash
# Connect to database
psql -h localhost -U medical_user -d medical_imaging

# View tables
\dt

# View table structure
\d patients

# Exit
\q
```

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Connection Refused**
```bash
# Check if PostgreSQL is running
# Windows: Services > PostgreSQL
# macOS/Linux: sudo systemctl status postgresql

# Start PostgreSQL if not running
# Windows: net start postgresql-x64-15
# macOS/Linux: brew services start postgresql@15
```

#### **2. Authentication Failed**
```bash
# Reset password (Windows)
psql -U postgres
ALTER USER postgres PASSWORD 'new_password';

# Reset password (Linux/macOS)
sudo -u postgres psql
ALTER USER postgres PASSWORD 'new_password';
```

#### **3. Database Doesn't Exist**
```bash
# List databases
psql -U postgres -l

# Create database
CREATE DATABASE medical_imaging;
```

#### **4. Port Already in Use**
```bash
# Check what's using port 5432
netstat -an | findstr :5432

# Change PostgreSQL port in postgresql.conf
# Location varies by OS
```

## 📊 Database Schema

The application will automatically create these tables:
- `patients` - Patient information
- `doctors` - Doctor/staff information  
- `studies` - Medical studies
- `images` - DICOM images
- `users` - User accounts and authentication

## 🎯 Next Steps

1. ✅ Install PostgreSQL
2. ✅ Create database and user
3. ✅ Configure environment
4. ✅ Start the application
5. ✅ Test API endpoints

Your medical imaging backend is now ready with PostgreSQL! 🚀
