import streamlit as st
from groq import Groq

# Function to get completions from Groq
def groq_completions(user_content, model, api_key):
    client = Groq(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI-powered coding assistant here to help with programming challenges. \nYou can assist with various tasks, including:\n\n- **Debugging Code:** Identify and fix errors in code shared by the user.\n- **Explaining Concepts:** Provide detailed explanations of programming concepts.\n- **Code Suggestions:** Offer code snippets and suggest approaches to implement features.\n- **Optimization Tips:** Advise on improving code performance.\n- **Learning Resources:** Recommend tutorials, articles, and other resources to help the user learn something new."
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            temperature=0.5,
            max_tokens=5640,
            top_p=1,
            stream=True,
            stop=None,
        )

        result = ""
        for chunk in completion:
            result += chunk.choices[0].delta.content or ""

        return result

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Streamlit interface
def main():
    st.title("AI Coding Assistant")

    # Sidebar for API key input
    with st.sidebar:
        st.header("API Key Setup")
        api_key = st.text_input("Enter your GROQ API Key", type="password")
        if api_key:
            try:
                # Test the API key by creating a simple completion request
                client = Groq(api_key=api_key)
                completion = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[{"role": "system", "content": "Test"}],
                    temperature=0.5,
                    max_tokens=5,
                    top_p=1,
                    stream=True,
                    stop=None,
                )
                
                result = ""
                for chunk in completion:
                  result += chunk.choices[0].delta.content or ""
        
                # Display success message if API key is valid
                st.sidebar.success("API Key is valid!")
            except Exception as e:
                st.sidebar.error(f"Invalid API Key: {e}")

    # Dropdown for model selection
    model_options = [
        "mixtral-8x7b-32768",
        "llama3-8b-8192",
        "llama3-70b-8192",
        "llama-guard-3-8b"
    ]
    selected_model = st.selectbox("Select Model", model_options)

    # Text input for user query
    user_content = st.text_input("How can I help you today?")

    if st.button("Submit"):
        if not user_content:
            st.warning("Please enter your query to proceed.")
            return

        if not api_key:
            st.warning("Please enter and validate your API Key in the sidebar.")
            return

        st.info("Generating answers... Please wait.")
        answer = groq_completions(user_content, selected_model, api_key)
        st.success("Response generated successfully!")

        st.markdown("### Response:")
        st.text_area("", value=answer, height=min(len(answer) * 20, 500), max_chars=None, key=None)

if __name__ == "__main__":
    main()
