# Splash - Your Voice Assistant

**Splash** is a Python-based voice assistant that listens for a wake word, processes voice commands, and responds with AI-generated answers. Designed for seamless interaction, Splash uses advanced speech recognition and natural-sounding text-to-speech (TTS) to bring conversations to life.

---

## Additional Requirements

### Python Libraries

```bash
pip install -r requirements.txt
```

### Other Requirements

- [Microsoft Edge TTS](https://github.com/Microsoft/edge-tts): For high-quality text-to-speech synthesis.  
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper): A fast and efficient library for transcribing speech using OpenAI's Whisper model.

---

## How to Use

1. **Run Splash**  
   Execute the script, and Splash will actively listen for the wake word. The default wake word is `hello`.

2. **Give Commands**  
   After detecting the wake word, Splash will start transcribing speech and respond based on your input.

3. **Manage Conversations**  
   Conversations are logged in a JSON file (`conversation.json`) for review or reuse.

---

## Features

- **Wake Word Activation**: Listens for a customizable wake word to activate.  
- **Speech-to-Text**: Converts your speech to text using Faster Whisper.  
- **AI-Generated Responses**: Interacts with you using the Gemini AI-powered response system.  
- **Text-to-Speech**: Responds audibly using Edge TTS.  
- **Command Recognition**: Splash can recognize predefined commands (e.g., `remove`).  
- **Conversation Logging**: Saves conversations to a JSON file for future use.

---

## Customization

You can customize Splash by modifying the following:

- **Wake Word**: Change the `WAKE_WORD` variable in the script.  
- **Input Device**: Adjust `DEVICE_INDEX` to use a specific audio input.  
- **TTS Voice**: Modify the voice in the `speak_text` function (e.g., `en-GB-SoniaNeural`).  
- **Commands**: Add more commands to the `commands` list.

---

## Troubleshooting

- **Microphone Issues**: Ensure the correct `DEVICE_INDEX` is set for your input device.  
- **No Output Audio**: Verify your speakers or headphones are selected as the output device.  
- **Wake Word Not Detected**: Speak clearly and ensure the wake word matches what is set in the code.  
- **Dependencies Missing**: Make sure all required libraries are installed.

---

## License

Splash is open-source and licensed under the MIT License.
