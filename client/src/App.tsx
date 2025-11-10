import { useState, useRef } from 'react';
import { Plane, Sparkles } from 'lucide-react';
import { api } from './services/api';

interface Result {
  response: string;
  session_id?: string;
}

function App() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handlePlan = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setLoading(true);

    try {
      const response = await api.sendMessage(userMessage, sessionId || undefined);
      setResult(response);
      console.log(response)
      if (response.session_id) {
        setSessionId(response.session_id);
      }
    } catch (error: any) {
      console.error('Error:', error);
      setResult({
        response: '❌ Sorry, there was an error. Please make sure the server is running.'
      });
    } finally {
      setLoading(false);
      setInput('')
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handlePlan();
    }
  };

  const handleReset = () => {
    setInput('');
    setResult(null);
    setSessionId(null);
    textareaRef.current?.focus();
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>✈️ AI Travel Planner</h1>
          <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '8px' }}>
            Plan your Canadian adventure with AI 🍁
          </p>
        </header>

        <div className="planner-container">
          {!result && (
            <div className="prompt-examples">
              <p style={{ marginBottom: '12px', color: 'var(--text-secondary)' }}>
                Try something like:
              </p>
              <div className="examples">
                <button
                  className="example-button"
                  onClick={() => setInput("5-day cultural trip to Montreal on a budget")}
                >
                  5-day cultural trip to Montreal on a budget
                </button>
                <button
                  className="example-button"
                  onClick={() => setInput("Family vacation to Victoria, love beaches and adventure")}
                >
                  Family vacation to Victoria, love beaches
                </button>
                <button
                  className="example-button"
                  onClick={() => setInput("Romantic week in Banff with food and culture")}
                >
                  Romantic week in Banff
                </button>
              </div>
            </div>
          )}

          {result && (
            <div className="result-section">
              <div className="result-content">
                <pre>{result.response}</pre>
              </div>
            </div>
          )}

          {/* Input always visible */}
          <div className="input-area">
            {sessionId && (
              <div className="refine-hint">
                💡 Refine your plan - adjust duration, budget, or add activities
              </div>
            )}
            <div className="input-wrapper">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={sessionId
                  ? "Refine your plan (e.g., 'make it 5 days' or 'add more food activities')"
                  : "Describe your ideal Canadian trip..."}
                rows={3}
                disabled={loading}
                autoFocus
              />
            </div>
            <div className="action-bar">
              <button
                className="primary-action-button"
                onClick={handlePlan}
                disabled={!input.trim() || loading}
              >
                {loading ? (
                  <>
                    <div className="spinner"></div>
                    Planning...
                  </>
                ) : (
                  <>
                    <Sparkles size={20} />
                    {sessionId ? 'Update Plan' : 'Plan My Trip'}
                  </>
                )}
              </button>
              {sessionId && (
                <button className="secondary-action-button" onClick={handleReset}>
                  <Plane size={16} />
                  <span>New Trip</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;