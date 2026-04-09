import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || '/api'

type Direction = 'formal_to_informal' | 'informal_to_formal'

function App() {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [direction, setDirection] = useState<Direction>('formal_to_informal')

  const handleTranslate = async () => {
    if (!inputText.trim()) return

    setLoading(true)
    setError('')
    setOutputText('')

    try {
      const response = await fetch(`${API_URL}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText, direction }),
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

  const toggleDirection = () => {
    setDirection(prev => prev === 'formal_to_informal' ? 'informal_to_formal' : 'formal_to_informal')
    setInputText('')
    setOutputText('')
  }

  const formalExamples = [
    "I would like to inquire about the status of my order.",
    "Please be advised that the meeting has been rescheduled.",
    "I am writing to express my sincere gratitude for your assistance.",
    "We regret to inform you that your application has been unsuccessful.",
    "Kindly find the attached document for your perusal.",
  ]

  const informalExamples = [
    "Hey, what's up with my order?",
    "Just letting you know, the meeting got moved to a different time.",
    "Thanks a ton for helping me out!",
    "Sorry, but your application didn't work out.",
    "Here's that doc you asked for, check it out.",
  ]

  const examples = direction === 'formal_to_informal' ? formalExamples : informalExamples
  const inputLabel = direction === 'formal_to_informal' ? '📝 Formal Text' : '💬 Informal Text'
  const outputLabel = direction === 'formal_to_informal' ? '💬 Informal Text' : '📝 Formal Text'
  const inputPlaceholder = direction === 'formal_to_informal' ? 'Enter formal text here...' : 'Enter casual text here...'
  const buttonLabel = direction === 'formal_to_informal' ? 'Make Informal →' : 'Make Formal →'

  return (
    <div className="min-vh-100 bg-light">
      {/* Header */}
      <header className="bg-primary text-white py-4">
        <div className="container">
          <h1 className="mb-1">🔄 Formalator</h1>
          <p className="mb-0 opacity-75">Transform text between formal and informal styles</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-4">
        {/* Direction Toggle */}
        <div className="row mb-4">
          <div className="col-12">
            <div className="card shadow-sm">
              <div className="card-body text-center">
                <div className="btn-group" role="group">
                  <button
                    className={`btn ${direction === 'formal_to_informal' ? 'btn-primary' : 'btn-outline-primary'}`}
                    onClick={() => direction !== 'formal_to_informal' && toggleDirection()}
                  >
                    Formal → Informal
                  </button>
                  <button
                    className={`btn ${direction === 'informal_to_formal' ? 'btn-primary' : 'btn-outline-primary'}`}
                    onClick={() => direction !== 'informal_to_formal' && toggleDirection()}
                  >
                    Informal → Formal
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row g-4">
          {/* Input Panel */}
          <div className="col-lg-6">
            <div className="card h-100 shadow-sm">
              <div className="card-header bg-white">
                <h5 className="mb-0">{inputLabel}</h5>
              </div>
              <div className="card-body">
                <textarea
                  className="form-control mb-3"
                  rows={6}
                  placeholder={inputPlaceholder}
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
                      buttonLabel
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
                <h5 className="mb-0">{outputLabel}</h5>
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
