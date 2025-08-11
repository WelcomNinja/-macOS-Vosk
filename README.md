# -macOS-Vosk


# 🎤 Распознавание речи на macOS с Vosk


Проект для распознавания русской речи в реальном времени с использованием микрофона вашего Mac. Основан на технологии Vosk с открытым исходным кодом.

## ✨ Особенности
- 🚀 Распознавание речи в реальном времени
- 🇷🇺 Поддержка русского языка
- 🔍 Автоматическое определение микрофона
- 📝 Вывод частичных результатов по мере распознавания
- ⚙️ Простая настройка через терминал
- 🆓 Полностью открытый исходный код

## ⚙️ Установка

### 1. Установите зависимости
```bash
# Установка Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Настройка окружения
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
# Установка Python и библиотек
brew install python portaudio
pip3 install vosk sounddevice
```

### 2. Загрузите модель распознавания речи
```bash
mkdir -p ~/vosk-models
curl -L https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip -o vosk-model-ru.zip
unzip vosk-model-ru.zip -d ~/vosk-models/
mv ~/vosk-models/vosk-model-ru-0.42 ~/vosk-models/ru-model
```

### 3. Клонируйте репозиторий
```bash
git clone https://github.com/ваш-username/ваш-репозиторий.git
cd ваш-репозиторий
```

## 🚀 Использование

### Базовый запуск
```bash
python3 speech_recognition.py
```

### Просмотр аудиоустройств
```bash
python3 speech_recognition.py --list-devices
```

### Использование другой модели
```bash
python3 speech_recognition.py --model ~/path/to/your/model
```

## 🛠️ Устранение проблем

| Проблема | Решение |
|---------|---------|
| zsh: command not found: brew | Выполните команды установщика Homebrew |
| Нет доступа к микрофону | Разрешите доступ в Системных настройках → Безопасность → Конфиденциальность → Микрофон |
| Ошибка: Модель не найдена | Проверьте путь: ls ~/vosk-models/ru-model |
| Плохое качество распознавания | Используйте полную модель: vosk-model-ru-0.22 |

## 📚 Рекомендации

Для лучшего качества:
- Используйте внешний микрофон
- Скачайте полную модель:
```bash
curl -L https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip -o vosk-model-ru-full.zip
unzip vosk-model-ru-full.zip -d ~/vosk-models/
```
- Запустите с параметром:
```bash
python3 speech_recognition.py --model ~/vosk-models/vosk-model-ru-0.22
```

## 📜 Лицензия

Этот проект использует:
- [Vosk](https://github.com/alphacep/vosk-api) (Apache 2.0)
- [SoundDevice](https://github.com/spatialaudio/python-sounddevice) (MIT)
