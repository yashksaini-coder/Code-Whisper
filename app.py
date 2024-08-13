import os
from groq import Groq

# Set the environment variable
os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

while True:
    user_input = input("Enter your message (or type 'exit' to quit): ")

    if user_input.lower() == "exit":
        break

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)