import React, { useState } from 'react';
import axios from 'axios';

const UserForm = ({ onUserAdded }) => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        bio: ''
    });
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            console.log('Отправка данных:', formData);

            const response = await axios.post('http://localhost:8000/users/', formData, {
                timeout: 5000,
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            console.log('Ответ от сервера:', response.data);

            setMessage('✅ Пользователь успешно добавлен!');
            setFormData({ name: '', email: '', bio: '' });

            if (onUserAdded) {
                onUserAdded(response.data);
            }
        } catch (error) {
            console.error('Полная ошибка:', error);

            if (error.response) {
                // Сервер ответил с ошибкой
                if (error.response.status === 400) {
                    setMessage('❌ Ошибка: Пользователь с таким email уже существует');
                } else {
                    setMessage(`❌ Ошибка сервера: ${error.response.status} - ${error.response.data.detail}`);
                }
            } else if (error.request) {
                // Запрос был сделан, но ответа нет
                setMessage('❌ Ошибка: Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд на порту 8000');
            } else {
                // Другие ошибки
                setMessage('❌ Ошибка: ' + error.message);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="user-form">
            <h2>Добавить нового пользователя</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="name">Имя *</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        required
                        disabled={loading}
                        placeholder="Введите имя"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="email">Email *</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                        disabled={loading}
                        placeholder="Введите email"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="bio">Биография</label>
                    <textarea
                        id="bio"
                        name="bio"
                        value={formData.bio}
                        onChange={handleChange}
                        rows="4"
                        disabled={loading}
                        placeholder="Расскажите о себе..."
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? 'Добавление...' : 'Добавить пользователя'}
                </button>
            </form>

            {message && (
                <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
                    {message}
                </div>
            )}
        </div>
    );
};

export default UserForm;
