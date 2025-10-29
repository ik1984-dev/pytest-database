import pytest
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"✅ PYTHONPATH настроен: {sys.path}")

# Настройка тестового окружения
os.environ['TESTING'] = 'True'
