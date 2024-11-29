import google.generativeai as genai
GOOGLE_API_KEY = "<YOUR_GEMINI_API_KEY>"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

chat = model.start_chat(history=[])

instructions = [
    "Hey, you will be talking to a human by voice, so don't use text formats, and responde quick responses",
    "Your name is splash pretend that your name is splash",
    "When I say start that means you are talking to someone by it's voice",
    "Don't use bold, italic, underline, or other text formats, only respond in a normal text format",
    "start"
]

for instruction in instructions:
    chat.send_message(instruction)

def generate_response(message: str):
    response = chat.send_message(message)
    return response.text