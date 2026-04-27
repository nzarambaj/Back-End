@echo off
echo Connecting to PostgreSQL and creating medical_imaging database...
echo.

REM Add PostgreSQL to PATH (adjust path if needed)
set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin

REM Try to create database
psql -U postgres -c "CREATE DATABASE imagingdb;" 2>nul

if %ERRORLEVEL% EQU 0 (
    echo ✅ Database 'imagingdb' created successfully!
) else (
    echo ⚠️  Database might already exist or connection failed
    echo Let's test the connection...
)

REM Test connection
psql -U postgres -d imagingdb -c "SELECT version();" >nul 2>nul

if %ERRORLEVEL% EQU 0 (
    echo ✅ Connection successful!
) else (
    echo ❌ Connection failed. Check your PostgreSQL password.
    echo Make sure PostgreSQL service is running.
)

echo.
echo Next: Update your .env file with your PostgreSQL password
echo.
pause
