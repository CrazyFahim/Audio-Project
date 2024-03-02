import pyaudio
import wave
import threading
import tkinter as tk
import speech_recognition as sr

filename = "recorded.wav"
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100
p = pyaudio.PyAudio()
is_recording = False

def start_recording():
    global is_recording
    stream = p.open(format=FORMAT, channels=channels, rate=sample_rate, input=True, output=True, frames_per_buffer=chunk)
    frames = []
    is_recording = True
    print("Recording...")
    while is_recording:
        data = stream.read(chunk)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        text_area.insert(tk.END, text)

def stop_recording():
    global is_recording
    is_recording = False

def create_gui():
    global text_area
    root = tk.Tk()
    root.geometry('800x600')
    start_button = tk.Button(root, text='Start', command=lambda: threading.Thread(target=start_recording).start())
    stop_button = tk.Button(root, text='Stop', command=stop_recording)
    start_button.pack()
    stop_button.pack()
    text_area = tk.Text(root)
    text_area.pack()
    root.mainloop()


if __name__ == "__main__":
    create_gui()
    p.terminate()