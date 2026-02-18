import React, { useState } from 'react';
import './MatrixForm.css';

export default function MatrixForm({ onSubmit, loading, error }) {
  const [date, setDate] = useState('');

  function handleInput(e) {
    let val = e.target.value.replace(/\D/g, '');
    if (val.length > 2) val = val.slice(0,2) + '.' + val.slice(2);
    if (val.length > 5) val = val.slice(0,5) + '.' + val.slice(5);
    if (val.length > 10) val = val.slice(0,10);
    setDate(val);
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (date.length === 10) onSubmit(date);
  }

  return (
    <div className="form-wrap">
      <div className="form-card">
        <div className="form-icon">✨</div>
        <h2>Введите дату рождения</h2>
        <p className="form-hint">Мы рассчитаем вашу кармическую карту</p>
        
        <div className="form-info">
          <div className="info-title">🔮 Что вы узнаете:</div>
          <ul className="info-list">
            <li>⭐ Ваше главное предназначение в жизни</li>
            <li>🎯 Сильные стороны и таланты</li>
            <li>⚠️ Слабые стороны и зоны роста</li>
            <li>💡 Практические советы по каждому аспекту</li>
            <li>🕰 Жизненные этапы (40, 60+ лет)</li>
          </ul>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-wrap">
            <input
              type="text"
              className="date-input"
              value={date}
              onChange={handleInput}
              placeholder="ДД.ММ.ГГГГ"
              maxLength={10}
              inputMode="numeric"
              autoFocus
            />
          </div>

          {error && <div className="form-error">⚠️ {error}</div>}

          <button
            type="submit"
            className="btn-primary"
            disabled={date.length < 10 || loading}
          >
            {loading ? <span className="spinner" /> : '🔮 Рассчитать матрицу'}
          </button>
        </form>

        <div className="form-examples">
          <span>Например:</span>
          {['15.03.1990', '07.11.1985', '22.06.2000'].map(d => (
            <button key={d} className="btn-example" onClick={() => setDate(d)}>
              {d}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
