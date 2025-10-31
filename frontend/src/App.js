import React, { useState } from 'react';
import UserForm from './components/UserForm';
import UserList from './components/UserList';
import './App.css';

// 🚀 ГЛАВНЫЙ КОМПОНЕНТ ПРИЛОЖЕНИЯ
function App() {
    // 🎯 СОСТОЯНИЕ ДЛЯ ОТСЛЕЖИВАНИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ
    // newUser - хранит данные нового пользователя или null
    const [newUser, setNewUser] = useState(null);

    // 📨 ОБРАБОТЧИК УСПЕШНОГО ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ
    // Вызывается когда UserForm успешно создает пользователя
    const handleUserAdded = (user) => {
        setNewUser(user); // Обновляем состояние с новым пользователем
    };

    // 🎨 РЕНДЕРИНГ ИНТЕРФЕЙСА ПРИЛОЖЕНИЯ
    return (
        <div className="App">
            {/* 🏁 ШАПКА ПРИЛОЖЕНИЯ */}
            <header className="App-header">
                <h1>🚀 Система управления пользователями</h1>
                <p>FastAPI + React + PostgreSQL</p>
            </header>

            {/* 📦 ОСНОВНОЕ СОДЕРЖИМОЕ */}
            <main className="App-main">
                <div className="container">
                    {/* 📝 СЕКЦИЯ ФОРМЫ ДЛЯ СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ */}
                    <section className="form-section">
                        {/*
                          Передаем колбэк в UserForm
                          Когда пользователь создан, вызывается handleUserAdded
                        */}
                        <UserForm onUserAdded={handleUserAdded} />
                    </section>

                    {/* 📋 СЕКЦИЯ СПИСКА ПОЛЬЗОВАТЕЛЕЙ */}
                    <section className="list-section">
                        {/*
                          Передаем нового пользователя в UserList
                          Когда newUser меняется, UserList обновляет список
                        */}
                        <UserList newUser={newUser} />
                    </section>
                </div>
            </main>

            {/* 🦶 ПОДВАЛ ПРИЛОЖЕНИЯ */}
            <footer className="App-footer">
                <p>© 2024 User Management System</p>
            </footer>
        </div>
    );
}

export default App;