import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox, ttk
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import threading

# Supported languages dictionary
LANG_DICT = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-CN",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml"
}

# Function to capture voice input
def capture_speech(lang_code):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            print(f"Recording in language: {lang_code}...")
            audio = recognizer.listen(mic, timeout=5, phrase_time_limit=10)
            spoken_text = recognizer.recognize_google(audio, language=lang_code)
            print(f"Recognized ({lang_code}): {spoken_text}")
            return spoken_text
    except sr.WaitTimeoutError:
        messagebox.showwarning("Timeout", "No speech detected in time limit.")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Speech was unclear.")
    except sr.RequestError:
        messagebox.showerror("Error", "Speech recognition service not available.")
    return ""

# Function to translate given text
def perform_translation(text, target_code):
    try:
        translator = GoogleTranslator(source="auto", target=target_code)
        translated = translator.translate(text)
        print(f"Translation ({target_code}): {translated}")
        return translated
    except Exception as e:
        messagebox.showerror("Translation Failed", str(e))
        return ""

# Function to play text as audio
def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("speech_output.mp3")
        os.system("start speech_output.mp3")  # Works on Windows
    except Exception as e:
        messagebox.showerror("Audio Error", str(e))

# Speech translation process
def handle_speech_translation():
    input_code = LANG_DICT[input_language.get()]
    output_code = LANG_DICT[output_language.get()]
    voice_text = capture_speech(input_code)
    if voice_text:
        translated = perform_translation(voice_text, output_code)
        play_audio(translated, output_code)
        output_box.delete(0, tk.END)
        output_box.insert(0, translated)

# Text translation process
def handle_text_translation():
    given_text = input_text.get()
    if not given_text.strip():
        messagebox.showwarning("Empty Field", "Please enter text first.")
        return
    target_code = LANG_DICT[output_language.get()]
    translated = perform_translation(given_text, target_code)
    play_audio(translated, target_code)
    output_box.delete(0, tk.END)
    output_box.insert(0, translated)

# Run speech translation in a separate thread
def speech_button_action():
    threading.Thread(target=handle_speech_translation, daemon=True).start()

# Run text translation in a separate thread
def text_button_action():
    threading.Thread(target=handle_text_translation, daemon=True).start()

# Build the app UI
def launch_app():
    global input_language, output_language, input_text, output_box

    app = tk.Tk()
    app.title("Voice & Text Language Converter")

    tk.Label(app, text="Choose Input Language:").pack()
    input_language = ttk.Combobox(app, values=list(LANG_DICT.keys()))
    input_language.set("English")
    input_language.pack()

    tk.Label(app, text="Choose Output Language:").pack()
    output_language = ttk.Combobox(app, values=list(LANG_DICT.keys()))
    output_language.set("Hindi")
    output_language.pack()

    tk.Label(app, text="Enter Text to Convert (Optional):").pack()
    input_text = tk.Entry(app, width=50)
    input_text.pack(pady=5)

    tk.Button(app, text="Convert Typed Text", command=text_button_action, padx=20, pady=10).pack(pady=5)
    tk.Button(app, text="Convert Speech", command=speech_button_action, padx=20, pady=10).pack(pady=5)

    tk.Label(app, text="Converted Result:").pack()
    output_box = tk.Entry(app, width=50)
    output_box.pack(pady=5)

    tk.Button(app, text="Exit", command=app.quit, padx=20, pady=10).pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    launch_app()
