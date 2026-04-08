import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleTranslate = async () => {
    if (!inputText.trim()) return

    setLoading(true)
    setError('')
    setOutputText('')

    try {
      const response = await fetch(`${API_URL}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setOutputText(data.translated)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setInputText('')
    setOutputText('')
    setError('')
  }

  const examples = [
    "I would like to inquire about the status of my order.",
    "Please be advised that the meeting has been rescheduled.",
    "I am writing to express my sincere gratitude for your assistance.",
    "We regret to inform you that your application has been unsuccessful.",
    "Kindly find the attached document for your perusal.",
  ]

  return (
    <div className="min-vh-100 bg-light">
      {/* Header */}
      <header className="bg-primary text-white py-4">
        <div className="container">
          <h1 className="mb-1">🔄 Formalator</h1>
          <p className="mb-0 opacity-75">Transform formal text into casual, conversational English</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-4">
        <div className="row g-4">
          {/* Input Panel */}
          <div className="col-lg-6">
            <div className="card h-100 shadow-sm">
              <div className="card-header bg-white">
                <h5 className="mb-0">📝 Formal Text</h5>
              </div>
              <div className="card-body">
                <textarea
                  className="form-control mb-3"
                  rows={6}
                  placeholder="Enter formal text here..."
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                />
                <div className="d-flex gap-2">
                  <button
                    className="btn btn-primary"
                    onClick={handleTranslate}
                    disabled={loading || !inputText.trim()}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" />
                        Translating...
                      </>
                    ) : (
                      'Translate →'
                    )}
                  </button>
                  <button
                    className="btn btn-outline-secondary"
                    onClick={handleClear}
                    disabled={!inputText && !outputText}
                  >
                    Clear
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Output Panel */}
          <div className="col-lg-6">
            <div className="card h-100 shadow-sm">
              <div className="card-header bg-white">
                <h5 className="mb-0">💬 Informal Text</h5>
              </div>
              <div className="card-body">
                {error && (
                  <div className="alert alert-danger" role="alert">
                    {error}
                  </div>
                )}
                <div
                  className="form-control mb-3 bg-light"
                  style={{ minHeight: '150px', whiteSpace: 'pre-wrap' }}
                >
                  {outputText || (
                    <span className="text-muted">Translation will appear here...</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Examples */}
        <div className="card mt-4 shadow-sm">
          <div className="card-header bg-white">
            <h5 className="mb-0">💡 Try these examples</h5>
          </div>
          <div className="card-body">
            <div className="list-group">
              {examples.map((example, index) => (
                <button
                  key={index}
                  className="list-group-item list-group-item-action"
                  onClick={() => setInputText(example)}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-top py-3 mt-4">
        <div className="container text-center text-muted">
          <small>Powered by LLM • Built with React + FastAPI + aiogram</small>
        </div>
      </footer>
    </div>
  )
}

export default App
