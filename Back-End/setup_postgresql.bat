@echo off
echo Setting up PostgreSQL for Medical Imaging Backend...
echo.

REM Check if PostgreSQL is installed
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PostgreSQL psql command not found in PATH
    echo Please add PostgreSQL bin directory to your PATH
    echo Typical location: C:\Program Files\PostgreSQL\15\bin
    echo.
    echo You can add it temporarily with:
    echo set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin
    echo.
    pause
    exit /b 1
)

echo PostgreSQL found! Creating database...
psql -U postgres -c "CREATE DATABASE medical_imaging;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Database 'medical_imaging' created successfully!
) else (
    echo Database might already exist or connection failed
    echo Let's try to connect to verify...
)

echo.
echo Testing connection to database...
psql -U postgres -d medical_imaging -c "SELECT version();" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Connection successful! Database is ready.
) else (
    echo Connection failed. Please check your PostgreSQL installation.
    echo Make sure PostgreSQL service is running.
)

echo.
echo Next steps:
echo 1. Update your .env file with your PostgreSQL password
echo 2. Run: npm install
echo 3. Run: npm run dev
echo.
pause
