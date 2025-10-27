import { useState, useEffect } from 'react';
import { api } from './services/api';
import './App.css';

interface HealthStatus {
  status: string;
  service: string;
  environment: {
    llm_provider: string;
    has_api_key: boolean;
  };
}

interface Config {
  llm_provider: string;
  model: string;
  features: {
    intent_extraction: boolean;
    destination_validation: boolean;
    itinerary_generation: boolean;
  };
}

function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [config, setConfig] = useState<Config | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    setLoading(true);
    setError(null);

    try {
      // Test health endpoint
      const healthData = await api.healthCheck();
      setHealth(healthData);

      // Test config endpoint
      const configData = await api.getConfig();
      setConfig(configData);

      console.log('✅ Server connection successful!');
    } catch (err: any) {
      console.error('❌ Server connection failed:', err);
      setError(err.message || 'Failed to connect to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🤖 AI Travel Planner
          </h1>
          <p className="text-gray-600">Server Connection Test - Stage 2</p>
        </div>

        {loading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Connecting to server...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <h3 className="text-red-800 font-semibold mb-2">❌ Connection Error</h3>
            <p className="text-red-600 text-sm">{error}</p>
            <p className="text-red-500 text-xs mt-2">
              Make sure the server is running: <code>cd server && uvicorn app.main:app --reload</code>
            </p>
          </div>
        )}

        {!loading && !error && health && config && (
          <>
            {/* Health Status */}
            <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-green-800 font-semibold mb-2 flex items-center">
                <span className="mr-2">✅</span>
                Server Health
              </h3>
              <div className="space-y-1 text-sm">
                <p><span className="font-medium">Status:</span> {health.status}</p>
                <p><span className="font-medium">Service:</span> {health.service}</p>
                <p><span className="font-medium">LLM Provider:</span> {health.environment.llm_provider}</p>
                <p>
                  <span className="font-medium">API Key Configured:</span>{' '}
                  {health.environment.has_api_key ? (
                    <span className="text-green-600">✓ Yes</span>
                  ) : (
                    <span className="text-red-600">✗ No</span>
                  )}
                </p>
              </div>
            </div>

            {/* Configuration */}
            <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-blue-800 font-semibold mb-2 flex items-center">
                <span className="mr-2">⚙️</span>
                Configuration
              </h3>
              <div className="space-y-1 text-sm">
                <p><span className="font-medium">Provider:</span> {config.llm_provider}</p>
                <p><span className="font-medium">Model:</span> {config.model}</p>
                <div className="mt-2">
                  <p className="font-medium mb-1">Available Features:</p>
                  <ul className="ml-4 space-y-1">
                    <li>✓ Intent Extraction</li>
                    <li>✓ Destination Validation</li>
                    <li>✓ Itinerary Generation</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Success Message */}
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center">
              <p className="text-gray-700 mb-2">
                🎉 <strong>Stage 2 Complete!</strong>
              </p>
              <p className="text-sm text-gray-600">
                Server is running and communicating with the client successfully.
              </p>
            </div>

            {/* Test Again Button */}
            <div className="mt-6 text-center">
              <button
                onClick={testConnection}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                🔄 Test Connection Again
              </button>
            </div>
          </>
        )}

        {/* API Documentation Link */}
        <div className="mt-8 text-center">
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 text-sm underline"
          >
            📚 View Interactive API Docs
          </a>
        </div>
      </div>
    </div>
  );
}

export default App;