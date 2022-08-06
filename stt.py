import vosk
import sys
import sounddevice as sd
import queue
import json

model = vosk.Model("model-big")  # если подключать большую базу, то поменять на "model-big"
samplerate = 16000  # 8000, 16000
device = 2  # id записывающего устройства (микрофон), должен быть = 1, но почему-то у меня выдаёт ошибку, поэтому 2

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# основной блок
def va_listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
            # else:
            #     print(rec.PartialResult())

# # для автономной работы stt.py закомментировать "основнйо блок"
# with sd.RawInputStream(samplerate=samplerate,
#                        blocksize=8000,
#                        device=device,
#                        dtype='int16',
#                        channels=1,
#                        callback=q_callback
#                        ):
#
#     rec = vosk.KaldiRecognizer(model, samplerate)
#     while True:
#         data = q.get()
#         if rec.AcceptWaveform(data):
#             print(rec.Result())
#         # else:
#         #     print(rec.PartialResult())
