
import os
import gradio as gr
from groq import Groq

SYSTEM_PROMPT = """
You are an expert Python programming tutor.

Teach Python to beginners.

1. Explain in simple English.
2. Support Roman Urdu.
3. Explain concepts step by step.
4. Generate working Python code.
5. Explain code line by line.
6. Help students fix errors.
7. Give practice questions and quizzes.
"""

def python_tutor(message, history):

    try:
        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            return "GROQ_API_KEY is missing. Please configure it in Render."

        client = Groq(api_key=api_key)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        for item in history:
            if isinstance(item, dict):
                role = item.get("role")
                content = item.get("content")

                if role in ["user", "assistant"] and isinstance(content, str):
                    messages.append({
                        "role": role,
                        "content": content
                    })

        messages.append({
            "role": "user",
            "content": message
        })

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.5,
            max_completion_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.ChatInterface(
    fn=python_tutor,
    title="🐍 My Python AI Tutor",
    description="Learn Python with your personal AI teacher. English and Roman Urdu supported!",
    examples=[
        "What is Python?",
        "Explain variables",
        "Explain loops in Roman Urdu",
        "Write a Python calculator",
        "Give me 5 Python exercises",
        "Explain Python functions"
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
