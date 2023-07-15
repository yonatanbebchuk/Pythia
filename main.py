import openai
import streamlit
import streamlit.components.v1 as components

from chat import ChatRecord
from chat.chats import OpenAIChat

openai.api_key = streamlit.secrets["OPENAI_API_KEY"]


def display_header():
    streamlit.set_page_config(
        page_title="ChatBot",
        page_icon="logo.png",
        layout="centered",
    )
    streamlit.image("logo.png", width=150)
    streamlit.title("Chat GUI")


def initialize_session_state():
    streamlit.session_state.setdefault("message_history", list())


def clear_chat():
    streamlit.session_state["message_history"] = list()


def get_prompt():
    return streamlit.text_input(
        label="Insert prompt here...",
        key="input",
        on_change=submit_prompt,
    )


def submit_prompt():
    streamlit.session_state.input = str()


def main():
    display_header()
    initialize_session_state()

    # Initialize Chat
    chat_record = ChatRecord(streamlit.session_state.message_history)
    chatbot = OpenAIChat(
        name="wittgenstein",
        purpose="You are Ludwig Wittgenstein mixed with snoop dogg.",
        historic=True,
        history=chat_record,
    )

    # Display Chat
    chat_record.display()
    scroll_to_the_bottom = """
    <script>
        window.scrollTo(0, document.body.scrollHeight);
    </script>
    """
    components.html(scroll_to_the_bottom)

    # Prompt Bar
    if prompt := get_prompt():
        response = chatbot.query(prompt)
        streamlit.session_state.message_history = response.messages

    streamlit.button("Clear", on_click=clear_chat)


if __name__ == '__main__':
    main()
