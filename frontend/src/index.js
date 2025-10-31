// Импорт необходимых библиотек React
import React from 'react';
import ReactDOM from 'react-dom/client';  // ReactDOM для рендеринга в DOM (React 18+)
import './index.css';                     // Глобальные CSS стили
import App from './App';                  // Главный компонент приложения
import reportWebVitals from './reportWebVitals';  // Инструменты для измерения производительности

// 🎯 СОЗДАНИЕ КОРНЕВОГО ЭЛЕМЕНТА ДЛЯ RENDER
// ReactDOM.createRoot() - современный метод рендеринга (React 18+)
// document.getElementById('root') - находит DOM элемент с id "root" в index.html
const root = ReactDOM.createRoot(document.getElementById('root'));

// 🚀 РЕНДЕРИНГ ПРИЛОЖЕНИЯ В DOM
root.render(
  // 🔍 СТРОГИЙ РЕЖИМ REACT (ТОЛЬКО ДЛЯ РАЗРАБОТКИ)
  // Помогает выявить потенциальные проблемы в приложении:
  // - Обнаруживает устаревшие методы жизненного цикла
  // - Предупреждает об использовании устаревшего API
  // - Выявляет неожиданные побочные эффекты
  <React.StrictMode>
    {/* 📦 ГЛАВНЫЙ КОМПОНЕНТ ПРИЛОЖЕНИЯ */}
    <App />
  </React.StrictMode>
);

// 📊 ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ПРИЛОЖЕНИЯ
// reportWebVitals() - собирает метрики производительности:
// - Core Web Vitals (LCP, FID, CLS)
// - Время загрузки компонентов
// - Производительность рендеринга

// Варианты использования:
// reportWebVitals(console.log) - вывод в консоль браузера
// reportWebVitals(sendToAnalytics) - отправка в аналитику
// По умолчанию: выводит в консоль в development режиме

// Подробнее: https://bit.ly/CRA-vitals
reportWebVitals();