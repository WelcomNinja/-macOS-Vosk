import os
import queue
import sys
import sounddevice as sd
import vosk
import json
import argparse

parser = argparse.ArgumentParser(description='Распознавание речи на macOS')
parser.add_argument('--model', type=str, default=os.path.expanduser('~/vosk-models/ru-model'),
                    help='Путь к модели Vosk')
parser.add_argument('--list-devices', action='store_true',
                    help='Показать список аудиоустройств')
args = parser.parse_args()

MODEL_PATH = args.model
SAMPLE_RATE = 16000

if args.list_devices:
    print("Доступные аудиоустройства:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        status = ""
        if device['max_input_channels'] > 0:
            status += " [ввод]"
        if device['max_output_channels'] > 0:
            status += " [вывод]"
        if i == sd.default.device[0]:
            status += " (устройство по умолчанию)"
        print(f"{i}: {device['name']}{status}")
    sys.exit(0)

if not os.path.exists(MODEL_PATH):
    print(f"Ошибка: Модель не найдена по пути {MODEL_PATH}")
    sys.exit(1)

model = vosk.Model(MODEL_PATH)

try:
    devices = sd.query_devices()
    mac_mic_names = ["MacBook Pro Microphone", "MacBook Air Microphone", 
                    "Built-in Microphone", "External Microphone"]
    
    device_id = None
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            if any(name in device['name'] for name in mac_mic_names):
                device_id = i
                break
    
    if device_id is None:
        device_id = sd.default.device[0]
        
    print(f"\nАвтоматически выбрано устройство: {devices[device_id]['name']}")

except Exception as e:
    print(f"Ошибка при выборе устройства: {e}")
    device_id = sd.default.device[0]

print("Нажмите Ctrl+C для остановки записи\n")

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

try:
    with sd.RawInputStream(
        device=device_id,
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        print("Слушаю... Говорите сейчас")
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print("\n✅ Распознано:", result["text"])
            else:
                partial_result = json.loads(rec.PartialResult())
                sys.stdout.write('\r' + ' ' * 80 + '\r')
                sys.stdout.write('\r▶ ' + partial_result["partial"])
                sys.stdout.flush()

except KeyboardInterrupt:
    print("\n\nЗапись остановлена пользователем")
    sys.exit(0)
except Exception as e:
    print(f"\nОшибка: {str(e)}")
    sys.exit(1)