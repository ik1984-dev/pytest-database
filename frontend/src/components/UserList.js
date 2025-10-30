import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserList = ({ newUser }) => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchUsers = async () => {
        try {
            setLoading(true);
            const response = await axios.get('http://localhost:8000/users/');
            setUsers(response.data);
            setError('');
        } catch (error) {
            console.error('Error fetching users:', error);
            setError('Не удалось загрузить пользователей');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    // Обновляем список при добавлении нового пользователя
    useEffect(() => {
        if (newUser) {
            setUsers(prevUsers => [newUser, ...prevUsers]);
        }
    }, [newUser]);

    if (loading) {
        return (
            <div className="user-list">
                <h2>Список пользователей</h2>
                <div className="loading">Загрузка пользователей...</div>
            </div>
        );
    }

    return (
        <div className="user-list">
            <div className="user-list-header">
                <h2>Список пользователей</h2>
                <button onClick={fetchUsers} className="refresh-btn">
                    Обновить
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            {users.length === 0 ? (
                <div className="empty-state">
                    📝 Пользователи не найдены. Добавьте первого пользователя!
                </div>
            ) : (
                <>
                    <div className="users-count">Всего пользователей: {users.length}</div>
                    <div className="users-grid">
                        {users.map(user => (
                            <div key={user.id} className="user-card">
                                <div className="user-header">
                                    <h3>{user.name}</h3>
                                    <span className="user-id">ID: {user.id}</span>
                                </div>
                                <p className="user-email">
                                    <strong>📧 Email:</strong> {user.email}
                                </p>
                                {user.bio && (
                                    <p className="user-bio">
                                        <strong>📝 Биография:</strong> {user.bio}
                                    </p>
                                )}
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

export default UserList;
