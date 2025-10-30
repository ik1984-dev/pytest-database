import React, { useState } from 'react';
import UserForm from './components/UserForm';
import UserList from './components/UserList';
import './App.css';

function App() {
    const [newUser, setNewUser] = useState(null);

    const handleUserAdded = (user) => {
        setNewUser(user);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>🚀 Система управления пользователями</h1>
                <p>FastAPI + React + PostgreSQL</p>
            </header>

            <main className="App-main">
                <div className="container">
                    <section className="form-section">
                        <UserForm onUserAdded={handleUserAdded} />
                    </section>

                    <section className="list-section">
                        <UserList newUser={newUser} />
                    </section>
                </div>
            </main>

            <footer className="App-footer">
                <p>© 2024 User Management System</p>
            </footer>
        </div>
    );
}

export default App;