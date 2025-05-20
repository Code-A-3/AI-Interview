# Voice-Based AI Interviewer
This project is a fully voice-enabled AI app that simulates an intelligent interviewer.
- Asks a series of questions vocally
- Listens to your spoken responses
- Sends your answers to OpenAI's ChatGPT to analyze and generate meaningful follow-up questions
- After the conversation, it provides a friendly summary about your personality

---

## How It Works
1. The app starts by asking a predefined first question using text-to-speech (TTS).
2. Your voice response is captured and transcribed using Google's speech recognition engine.
3. The response is sent to OpenAI's GPT-3.5 (or GPT-4o) to generate the next question.
4. This continues for 3 questions (or 10 if extended), after which the system provides a personality summary based on your responses.

---

## Technologies Used

- `pyttsx3` — Offline text-to-speech
- `SpeechRecognition` — Speech-to-text (using Google Web Speech API)
- `openai` — For dynamic question generation and analysis
- `python-dotenv` — Securely loads your API key

---


## How to Run
1. Clone the repository
2. Install dependencies via requirements.txt
3. Set your `.env` and API Key:
    - Create a `.env` file in the root of the project (same folder as `interview.py`).
    - Add your OpenAI API key like this:
    ```
    OPENAI_API_KEY=your-openai-api-key-here
    ```
    > **Do not commit this `.env` file**. It contains sensitive credentials and is excluded using `.gitignore`.
4. Run the script `interview.py`. Make sure your mic is connected and working.

## Notes:
- For GPT-4o support, you must have an active OpenAI API billing account.
- You can modify the number of questions in main() by changing the range(3) to range(10).
- Audio output (via pyttsx3) works offline and requires no additional API.