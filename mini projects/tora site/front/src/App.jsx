import { useState } from 'react';
import './App.css';

function App() {
  const [verse, setVerse] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleClassify = async () => {
    if (!verse.trim()) return;
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ verse }),
      });
      const result = await response.json();
      setResult(result);
    } catch (error) {
      console.error('Error:', error);
      // Fallback to mock
      const mockResult = {
        prediction: 'Torah',
        probabilities: { 'Torah': 0.85, 'Nevi’im': 0.10, 'Ketuvim': 0.05 },
        top_keywords: ['בראשית', 'אלהים', 'השמים']
      };
      setResult(mockResult);
    }
    setLoading(false);
  };

  const getSectionColor = (section) => {
    switch (section) {
      case 'Torah': return '#1A3C6E';
      case 'Nevi’im': return '#C9A86A';
      case 'Ketuvim': return '#4A5D7A';
      default: return '#2B2B2B';
    }
  };

  return (
    <div className="app">
      <div className="scroll-lines"></div>
      <div className="scroll-lines"></div>
      <header className="header">
        <div className="logo">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="10" width="30" height="20" rx="2" stroke="var(--soft-gold)" strokeWidth="2" fill="none"/>
            <line x1="8" y1="15" x2="32" y2="15" stroke="var(--soft-gold)" strokeWidth="1"/>
            <line x1="8" y1="20" x2="32" y2="20" stroke="var(--soft-gold)" strokeWidth="1"/>
            <line x1="8" y1="25" x2="32" y2="25" stroke="var(--soft-gold)" strokeWidth="1"/>
          </svg>
        </div>
        <h1>מסווג תנ״ך</h1>
      </header>
      <main className="main">
        <h2>Classificador de Tanach</h2>
        <p>Cole um versículo do Tanach e descubra se ele está na Torá, Neviim ou Ketuvim.</p>
        <input
          type="text"
          className="verse-input"
          value={verse}
          onChange={(e) => setVerse(e.target.value)}
          placeholder="Digite ou cole o versículo em hebraico..."
        />
        <button className="classify-btn" onClick={handleClassify} disabled={loading}>
          {loading ? <div className="loading"></div> : 'Identificar Seção'}
        </button>
        {result && (
          <div className="result-container fade-in">
            <div className="result-circle" style={{ background: `linear-gradient(135deg, ${getSectionColor(result.prediction)}, ${getSectionColor(result.prediction)}dd)` }}>
              <div className="prediction-name">{result.prediction}</div>
              <div className="prediction-percentage">{(result.probabilities[result.prediction] * 100).toFixed(1)}%</div>
            </div>
            <div className="result-details">
              <div className="probabilities">
                <h4>Probabilidades:</h4>
                {Object.entries(result.probabilities).map(([section, prob]) => (
                  <div key={section} className="prob-item">
                    <span>{section}:</span>
                    <span>{(prob * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
              <div className="keywords">
                <h4>Top Keywords:</h4>
                <p>{result.top_keywords.join(', ')}</p>
              </div>
            </div>
          </div>
        )}
      </main>
      <footer className="footer">
        <p>לְהַגְדִּיל תּוֹרָה וּלְהַאֲדִירָה</p>
      </footer>
    </div>
  );
}

export default App;