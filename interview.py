from openai import OpenAI           # OpenAI API
import pyttsx3                      # text-to-speech module
import speech_recognition as sr     # speech recognition module
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Text-to-speech setup
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speech speed

# Speech recognition setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    print(f"\nAssistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return listen()
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

def ask_chatgpt(question, answer, iteration):
    prompt = f"""
    You are an intelligent interviewer. The user has answered a question, and you need to analyze it
    and generate a follow-up question that logically continues the conversation.

    Current iteration: {iteration}
    Previous question: {question}
    User's answer: {answer}

    Generate a single follow-up question based on the answer. Keep it relevant and engaging.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4o" if you have billing
        messages=[
            {"role": "system", "content": "You are a smart interviewer who asks thoughtful questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def analyze_user(qa_pairs):
    formatted = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_pairs])
    prompt = f"""
    Based on the following Q&A conversation, provide a short personality summary of the user.
    Focus on communication style, interests, and character traits. Use a warm and friendly tone.

    {formatted}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4o"
        messages=[
            {"role": "system", "content": "You are a friendly assistant providing personality insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def main():
    qa_pairs = []
    question = "What is a topic you are passionate about?"

    for i in range(3):
        speak(f"Question {i+1}: {question}")
        user_answer = listen()
        qa_pairs.append((question, user_answer))
        if i < 2:
            question = ask_chatgpt(question, user_answer, i + 1)

    speak("Thank you for answering all my questions. Let me summarize what I learned about you.")
    final_summary = analyze_user(qa_pairs)
    speak(final_summary)

if __name__ == "__main__":
    main()
