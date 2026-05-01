
// Frontend API Configuration for 100% System Readiness
const API_BASE_URL = 'http://localhost:5000/api';

// Health check
export const checkBackendHealth = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return await response.json();
    } catch (error) {
        console.error('Backend health check failed:', error);
        return { status: 'error', message: 'Backend not accessible' };
    }
};

// Public endpoints (no authentication required)
export const getPublicDoctors = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/public/doctors`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch doctors:', error);
        return { doctors: [], error: 'Failed to fetch doctors' };
    }
};

export const getPublicPatients = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/public/patients`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch patients:', error);
        return { patients: [], error: 'Failed to fetch patients' };
    }
};

export const getPublicStudies = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/public/studies`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch studies:', error);
        return { studies: [], error: 'Failed to fetch studies' };
    }
};

// Database status
export const getDatabaseStatus = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/database/status`);
        return await response.json();
    } catch (error) {
        console.error('Database status check failed:', error);
        return { status: 'error', message: 'Database not accessible' };
    }
};

// System integration test
export const runSystemIntegrationTest = async () => {
    const results = {};
    
    try {
        // Test backend health
        results.backend = await checkBackendHealth();
        
        // Test data endpoints
        results.doctors = await getPublicDoctors();
        results.patients = await getPublicPatients();
        results.studies = await getPublicStudies();
        
        // Test database
        results.database = await getDatabaseStatus();
        
        // Test Calculus API
        const calculusResponse = await fetch('http://localhost:5001/api/health');
        results.calculus = await calculusResponse.json();
        
        results.overall = {
            status: 'success',
            timestamp: new Date().toISOString(),
            components_working: Object.keys(results).filter(key => 
                results[key] && !results[key].error
            ).length
        };
        
    } catch (error) {
        results.overall = {
            status: 'error',
            message: error.message,
            timestamp: new Date().toISOString()
        };
    }
    
    return results;
};
