# 🚀 Deploy Your Medical Imaging Application

## Option 1: Render (Recommended - Free)

### Step 1: Prepare for Deployment
1. **Exit Python environment**:
   ```cmd
   deactivate
   ```

2. **Go to Back-End folder**:
   ```cmd
   cd Back-End
   ```

3. **Create .env file**:
   ```cmd
   copy .env.example .env
   ```
   Edit .env and replace `your_postgresql_password` with your actual password

### Step 2: Deploy to Render
1. **Go to render.com**
2. **Sign up/login with GitHub**
3. **Create New Web Service**
4. **Connect your GitHub repository**
5. **Configure**:
   - **Name**: medical-imaging-api
   - **Environment**: Node
   - **Build Command**: npm install
   - **Start Command**: npm start
   - **Instance Type**: Free

### Step 3: Set Environment Variables
In Render dashboard, add these environment variables:
- `NODE_ENV=production`
- `DB_HOST=localhost`
- `DB_PORT=5432`
- `DB_NAME=medical_imaging`
- `DB_USER=postgres`
- `DB_PASSWORD=your_postgresql_password`
- `JWT_SECRET=your_super_secret_jwt_key_here_change_in_production`

## Option 2: Railway (Alternative)

1. **Go to railway.app**
2. **Connect GitHub**
3. **Import your repository**
4. **Set environment variables**
5. **Deploy**

## Option 3: Local Deployment

### Step 1: Setup Database
```cmd
create_database.bat
```

### Step 2: Start Server
```cmd
cd Back-End
npm install
npm start
```

### Step 3: Access API
- **Local**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 🎯 Deployment Checklist

- [ ] Exit Python virtual environment
- [ ] Create .env file with database credentials
- [ ] Test locally: `npm run dev`
- [ ] Push to GitHub
- [ ] Deploy to Render/Railway
- [ ] Set environment variables
- [ ] Test deployed API

## 📊 API Endpoints After Deployment

**Base URL**: `https://your-app-name.onrender.com`

- Health: `/api/health`
- Auth: `/api/auth/login`, `/api/auth/register`
- Patients: `/api/patients`
- Doctors: `/api/doctors`
- Studies: `/api/studies`
- Images: `/api/images`

## 🔧 Troubleshooting

### Database Connection Issues
1. Check PostgreSQL service is running
2. Verify database exists: `psql -U postgres -l`
3. Test connection: `psql -U postgres -d medical_imaging`

### Deployment Issues
1. Check logs in Render dashboard
2. Verify environment variables
3. Ensure package.json has correct start script

## 🎉 Success Indicators

✅ **Health Check Returns**:
```json
{
  "status": "healthy",
  "database": "PostgreSQL",
  "environment": "production"
}
```

✅ **API Endpoints Respond**:
- Test: `curl https://your-app-name.onrender.com/api/health`

**Your medical imaging API will be live and accessible!** 🚀
