1. Клонировать репозиторий
git clone https://github.com/ik1984-dev/pytest-database
cd pytest-database

2. Установить backend зависимости
cd backend
pip install -r requirements.txt
cd ..

3. Установить frontend зависимости
cd frontend
npm install
cd ..

4. Запустить проект
cd backend
python backend/run.py

cd frontend
npm start
