import React, { useState } from 'react';
import './MatrixResult.css';

const SECTIONS = [
  { key: 'center',    label: 'Предназначение',      icon: '⭐', desc: 'Суть кармической задачи воплощения. Главная цель души в этой жизни. Рассчитывается как сумма Неба, Земли, Женского и Мужского.', color: '#b71c1c' },
  { key: 'top',       label: 'Небо (день)',          icon: '🌌', desc: 'Духовный потенциал и связь с высшим. Рассчитывается по дню рождения. Показывает вашу духовную миссию и способности к самопознанию.', color: '#1565c0' },
  { key: 'bottom',    label: 'Земля (д+м+г)',        icon: '🌿', desc: 'Материальный путь и земное воплощение. Сумма дня, месяца и года рождения. Отвечает за реализацию в материальном мире, карьеру и финансы.', color: '#1b5e20' },
  { key: 'left',      label: 'Женское (месяц)',      icon: '🌸', desc: 'Женская энергия, эмоции и интуиция. Рассчитывается по месяцу рождения. Отвечает за отношения, чувства и внутренний мир.', color: '#880e4f' },
  { key: 'right',     label: 'Мужское (год)',        icon: '⚡', desc: 'Мужская энергия, воля и действие. Рассчитывается по году рождения. Отвечает за способность принимать решения, достигать целей и брать ответственность.', color: '#1a237e' },
  { key: 'tl',        label: 'Таланты',              icon: '✨', desc: 'Природные способности и дарования. Сумма Неба и Женского. Указывает на врождённые таланты, которые нужно развивать.', color: '#4a148c' },
  { key: 'rt',        label: 'Характер',             icon: '👤', desc: 'Личные качества и темперамент. Сумма Неба и Мужского. Показывает, как вы проявляете себя в мире, ваши основные черты.', color: '#4a148c' },
  { key: 'lb',        label: 'Задачи до 40',         icon: '⏳', desc: 'Вектор первой половины жизни. Сумма Женского и Земли. Основные задачи и уроки до 40 лет, которые нужно проработать.', color: '#4a148c' },
  { key: 'br',        label: 'Проработка',           icon: '🎯', desc: 'Главный урок воплощения. Сумма Земли и Мужского. Главная кармическая задача, которую нужно проработать для духовного роста.', color: '#4a148c' },
  { key: 'personal',  label: 'Личное предназначение',icon: '🌱', desc: 'Первый этап предназначения (до 40 лет). Сумма Земли и Неба. Работа над собой, самопознание, формирование личности.', color: '#1b5e20' },
  { key: 'social',    label: 'Социальное',           icon: '🤝', desc: 'Второй этап предназначения (до 60 лет). Сумма Женского и Мужского. Взаимодействие с обществом, реализация в социуме, вклад в мир.', color: '#0d47a1' },
  { key: 'spiritual', label: 'Духовное',             icon: '🔮', desc: 'Третий этап предназначения (после 60). Сумма Личного и Социального. Духовная миссия, передача мудрости, служение высшим целям.', color: '#4a148c' },
];

function ArcanaCard({ point, section }) {
  const [open, setOpen] = useState(false);
  if (!point) return null;
  return (
    <div className="arcana-card" style={{ '--accent': section.color }} onClick={() => setOpen(o => !o)}>
      <div className="arcana-card-header">
        <div className="arcana-badge" style={{ background: section.color }}>
          <span className="arcana-symbol">{point.symbol || '🔮'}</span>
          <span className="arcana-num">{point.num}</span>
        </div>
        <div className="arcana-info">
          <div className="section-label">{section.icon} {section.label}</div>
          <div className="arcana-name">{point.name}</div>
          <div className="arcana-keywords">{point.keywords}</div>
        </div>
        <div className={`chevron ${open ? 'open' : ''}`}>▼</div>
      </div>
      {open && (
        <div className="arcana-body">
          <p className="section-desc">{section.desc}</p>
          {point.plus && (
            <div className="arcana-plus">
              <span className="tag plus">✅ В плюсе</span>
              <p>{point.plus}</p>
            </div>
          )}
          {point.minus && (
            <div className="arcana-minus">
              <span className="tag minus">❌ В минусе</span>
              <p>{point.minus}</p>
            </div>
          )}
          {point.advice && (
            <div className="arcana-advice">
              <span className="tag advice">💡 Совет</span>
              <p>{point.advice}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function MatrixResult({ data, onReset, tg }) {
  const { points } = data;

  function handleShare() {
    if (tg) {
      tg.sendData(JSON.stringify({ action: 'matrix_result', date: data.date }));
    }
  }

  return (
    <div className="result-wrap">
      <div className="result-header">
        <div className="result-date">📅 {data.date}</div>
        <div className="result-center">
          <div className="center-badge">
            <span>{points.center?.symbol}</span>
            <strong>{points.center?.num}</strong>
          </div>
          <div>
            <div className="center-label">Предназначение</div>
            <div className="center-name">{points.center?.name}</div>
          </div>
        </div>
      </div>

      <div className="cards-list">
        {SECTIONS.map(sec => (
          <ArcanaCard key={sec.key} point={points[sec.key]} section={sec} />
        ))}
      </div>

      <div className="result-actions">
        {tg && (
          <button className="btn-share" onClick={handleShare}>
            📤 Поделиться в боте
          </button>
        )}
        <button className="btn-back" onClick={onReset}>
          ← Новый расчёт
        </button>
      </div>
    </div>
  );
}
