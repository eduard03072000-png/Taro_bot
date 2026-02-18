import React, { useState, useEffect } from 'react';
import MatrixForm from './components/MatrixForm';
import MatrixResult from './components/MatrixResult';
import './App.css';

function App() {
  const [tg, setTg] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const app = window.Telegram?.WebApp;
    if (app) {
      app.ready();
      app.expand();
      app.setHeaderColor('#080616');
      setTg(app);
    }
  }, []);

  async function handleSubmit(birthDate) {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await fetch('/api/matrix', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'ngrok-skip-browser-warning': '1',
        },
        body: JSON.stringify({ birth_date: birthDate }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Ошибка сервера');
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setResult(null);
    setError('');
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-icon">🔮</div>
        <h1>Матрица Судьбы</h1>
        <p className="header-sub">Расшифровка кармической карты</p>
      </header>

      <main className="app-main">
        {!result ? (
          <MatrixForm onSubmit={handleSubmit} loading={loading} error={error} />
        ) : (
          <MatrixResult data={result} onReset={handleReset} tg={tg} />
        )}
      </main>
    </div>
  );
}

export default App;
