import asyncio
import edge_tts
import speech_recognition as sr
import pygame
import json
import os
import time
import datetime
from faster_whisper import WhisperModel
from gemini import generate_response

# Wake word to listen for
WAKE_WORD = "splash"
DEVICE_INDEX = 1
LANGUAGE = "en"
WAKE_WORD_LANGUAGE = "en"

# Load the Whisper model
model_size = "base"  # Adjust this to your preferred model size (tiny, base, small, medium, large)
whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8") # Whisper Speech to Text model

pygame.mixer.init() # Initialize the mixer

async def speak_text(text, output_file="response.mp3", voice="en-GB-SoniaNeural"):
    """Save the text-to-speech audio and play it."""
    # Generate the audio file
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    # Play the saved audio
    playaudio(output_file)
    os.remove(output_file)


def playaudio(audio_file, wait=True):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() and wait:
        continue
    # Clean up
    if wait:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

def listen_for_wake_word():
    """Listen for the wake word and return True if it's detected."""
    print("Listening for wake word...")
    with sr.Microphone(device_index=DEVICE_INDEX) as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source, timeout=25, phrase_time_limit=5)
        try:
            temp_audio_file = "temp_audio.wav"
            with open(temp_audio_file, "wb") as f:
                f.write(audio.get_wav_data())
            
            transcription = transcribe_with_whisper(temp_audio_file, language=WAKE_WORD_LANGUAGE).lower()
            os.remove(temp_audio_file)
            print(f"You said: {transcription}")
            if WAKE_WORD in transcription:
                print("Wake word detected!")
                return True
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        return False

def transcribe_with_whisper(audio_file, language=None):
    """Transcribe an audio file using Faster Whisper."""
    segments, info = whisper_model.transcribe(audio_file, beam_size=5, language=language)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    transcription = ""
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        transcription += segment.text + " "
    return transcription.strip()

def add_to_conversation(message, author, time: float = 5.0):
    """Add a message to the conversation."""
    # Load the existing data
    try:
        with open("conversation.json", "r") as f:
            conversation = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        conversation = []  # Start with an empty list if the file doesn't exist or is invalid

    # Append the new message
    timestamp = int(datetime.datetime.now().timestamp())
    conversation.append({"message": message, "author": author, "timestamp": timestamp, "color": "white", "time": time})

    # Save the updated conversation back to the file
    with open("conversation.json", "w") as f:
        json.dump(conversation, f, indent=4)  # Write back with pretty formatting

def transcribe_speech():
    """Start transcribing speech using the Whisper model."""
    playaudio("audio/listening.mp3")
    print("Transcribing... (say 'stop' to end)")
    with sr.Microphone(device_index=DEVICE_INDEX) as source:
        recognizer = sr.Recognizer()
        while True:
            try:
                audio = recognizer.listen(source, timeout=25, phrase_time_limit=25)
                temp_audio_file = "temp/temp_audio.wav"
                with open(temp_audio_file, "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Transcribe the recorded audio
                transcription = transcribe_with_whisper(temp_audio_file, language=LANGUAGE).lower()
                os.remove(temp_audio_file)
                print(f"You said: {transcription}")

                # Check if the user wants splash to stop listening
                if "stop" in transcription.strip(".").split(" "):
                    asyncio.run(speak_text("I think that's enough for now."))
                    playaudio("audio/timeout.mp3", wait=False)
                    print("Stopping transcription.")
                    break
                if not transcription:
                    continue

                # Generate a response from Gemini
                response = generate_response(transcription)

                # Add the response to the conversation file
                add_to_conversation(response, "Ai")
                add_to_conversation(transcription, "User")
                print(f"AI Response: {response}")

                # Save and play the response using Edge TTS
                asyncio.run(speak_text(response))
            except sr.UnknownValueError:
                print("Could not understand audio.")
                continue
            except sr.exceptions.WaitTimeoutError:
                asyncio.run(speak_text("Are you still here? Hello?"))
                playaudio("audio/timeout.mp3", wait=False)
                print("No speech detected within the timeout, listening the wake word again...")
                continue
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")

if __name__ == "__main__":
    while True:
        if listen_for_wake_word():
            command = transcribe_speech()
