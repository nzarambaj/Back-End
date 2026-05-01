# Deployment Start Command Fix

## Issue Identified
The deployment is failing because the start command is set to `config/` which is a directory, not an executable command.

**Error Message:**
```
==> Running 'config/'
bash: line 1: config/: Is a directory
==> Exited with status 126
```

## Root Cause
The deployment service is trying to execute the `config/` directory as a command instead of running the actual backend server.

## Solution: Update Start Command

### Correct Start Command Options

**Option 1: Direct Node.js Start (Recommended)**
```
node 01_api/routes/medical_db_backend.js
```

**Option 2: Using npm script**
```
npm start
```
*(Requires adding start script to package.json)*

**Option 3: Using package.json scripts**
```
npm run start:backend
```
*(Requires updating package.json)*

## Deployment Configuration Updates

### For Render.com or similar services:

**Build Command:**
```
npm install
```

**Start Command:**
```
node 01_api/routes/medical_db_backend.js
```

**Environment Variables:**
```
PORT=5000
NODE_ENV=production
```

## Package.json Update (if using npm start)

Add to `package.json`:
```json
{
  "scripts": {
    "start": "node 01_api/routes/medical_db_backend.js",
    "dev": "node 01_api/routes/medical_db_backend.js"
  }
}
```

## File Structure Reference

The backend server is located at:
```
01_api/routes/medical_db_backend.js
```

Configuration files are in:
```
01_api/config/package.json
04_deployment/config/.env
```

## Verification Steps

1. **Update deployment service settings**
2. **Set correct start command**: `node 01_api/routes/medical_db_backend.js`
3. **Ensure port 5000 is configured**
4. **Deploy again**

## Expected Success Message

After fixing, you should see:
```
==> Running 'node 01_api/routes/medical_db_backend.js'
Medical Database Backend running on port 5000
Database: PostgreSQL 18 - medical_db
Flask API: http://localhost:5001
Health check: http://localhost:5000/api/health
```

## Troubleshooting

If still failing:
1. Check file paths are correct
2. Verify Node.js version compatibility
3. Ensure all dependencies are installed
4. Check environment variables are set
