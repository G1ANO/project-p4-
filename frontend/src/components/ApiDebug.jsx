import { useState } from 'react';
import { API_BASE_URL, API_ENDPOINTS, apiCall } from '../config';

export default function ApiDebug() {
  const [testResults, setTestResults] = useState({});
  const [testing, setTesting] = useState(false);

  const testEndpoint = async (name, url) => {
    try {
      setTestResults(prev => ({ ...prev, [name]: 'Testing...' }));
      
      const startTime = Date.now();
      const response = await fetch(url);
      const endTime = Date.now();
      
      const contentType = response.headers.get('content-type');
      const status = response.status;
      const time = endTime - startTime;
      
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
        setTestResults(prev => ({ 
          ...prev, 
          [name]: `✅ ${status} (${time}ms) - JSON response` 
        }));
      } else {
        const text = await response.text();
        setTestResults(prev => ({ 
          ...prev, 
          [name]: `❌ ${status} (${time}ms) - Got ${contentType || 'unknown'} instead of JSON` 
        }));
      }
    } catch (error) {
      setTestResults(prev => ({ 
        ...prev, 
        [name]: `🚨 Error: ${error.message}` 
      }));
    }
  };

  const runAllTests = async () => {
    setTesting(true);
    setTestResults({});
    
    const tests = [
      ['Backend Root', API_BASE_URL],
      ['Plans Endpoint', API_ENDPOINTS.PLANS],
      ['Login Endpoint', API_ENDPOINTS.LOGIN],
      ['Register Endpoint', API_ENDPOINTS.REGISTER],
    ];

    for (const [name, url] of tests) {
      await testEndpoint(name, url);
    }
    
    setTesting(false);
  };

  return (
    <div style={{ 
      position: 'fixed', 
      top: '10px', 
      right: '10px', 
      background: 'white', 
      border: '2px solid #ccc', 
      padding: '15px', 
      borderRadius: '8px',
      maxWidth: '400px',
      fontSize: '12px',
      zIndex: 9999
    }}>
      <h3>🔧 API Debug Panel</h3>
      
      <div style={{ marginBottom: '10px' }}>
        <strong>API Base URL:</strong> {API_BASE_URL}
      </div>
      
      <button 
        onClick={runAllTests} 
        disabled={testing}
        style={{
          background: '#1e40af',
          color: 'white',
          border: 'none',
          padding: '8px 16px',
          borderRadius: '4px',
          cursor: testing ? 'not-allowed' : 'pointer'
        }}
      >
        {testing ? 'Testing...' : 'Test API Endpoints'}
      </button>
      
      <div style={{ marginTop: '10px' }}>
        {Object.entries(testResults).map(([name, result]) => (
          <div key={name} style={{ margin: '5px 0' }}>
            <strong>{name}:</strong> {result}
          </div>
        ))}
      </div>
      
      <div style={{ marginTop: '10px', fontSize: '10px', color: '#666' }}>
        Open browser console for detailed logs
      </div>
    </div>
  );
}
