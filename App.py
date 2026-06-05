import tempfile
from time import sleep
from typing import TypedDict

import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from Data import itm_University_Data
from Functions import Tool_Prompt, load_css, system_prompt


# Keywords that route time-sensitive questions through the search-backed prompt.
tool_keywords = [
    "latest",
    "recent",
    "today",
    "news",
    "update",
    "current",
]

USER_AVATAR = "👨‍🎓"
AI_AVATAR = "🎓"

# Browser tab settings for the Streamlit app.
st.set_page_config(
    page_title="ITM Admission Chatbot",
    page_icon="icon.webp",
    layout="centered",
)

# Store imported ITM university data in a short variable.
itm_university = itm_University_Data

# Load custom CSS for the navigation bar, title, buttons, and chat layout.
load_css("style.css")

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


# Convert an assistant response into an MP3 file for Streamlit playback.
def text_to_speech(text):
    tts = gTTS(
        text=text,
        lang="en",
    )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3",
    )
    tts.save(temp_file.name)

    return temp_file.name


# Create the top navigation bar using official university page links.
st.markdown(
    """
<div class="navbar">
            
<a href="https://www.itmuniversity.ac.in/" target="_blank">About</a>

<a href="https://www.itmuniversity.ac.in/admission/onlineapply" target="_blank">Admission</a>

<a href="https://www.itmuniversity.ac.in/programmes/graduate-programs" target="_blank">Undergraduate Courses</a>

<a href="https://www.itmuniversity.ac.in/programmes/pg-programs" target="_blank">Postgraduate Courses</a>

<a href="https://www.itmuniversity.ac.in/admission/whom-to-contact" target="_blank">Contact</a>

</div>

""",
    unsafe_allow_html=True,
)

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Request a name before showing the chatbot conversation interface.
if st.session_state.user_name is None:
    st.markdown(
        """
        <div class="welcome-box">

        <h1 class="title">
        🎓 Welcome To ITM AI Assistant
        </h1>

        <p class="subtitle">
        Please enter your name to continue
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    name = st.text_input("Enter Your Name").strip()

    if st.button("Continue"):
        st.session_state.user_name = name
        st.rerun()
else:
    find_alphabet = all(
        [name.isalpha() for name in st.session_state.user_name.split()]
    )

    if find_alphabet and st.session_state.user_name != "":
        # Show chatbot title and subtitle on the main page.
        st.markdown(
            """
            <div>
                <h1 class="title">🎓 ITM University Admission Chatbot</h1>
                <p class="subtitle">Ask about courses, fees, hostel, placements, scholarships, and admissions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            # Streamlit reruns this script after every interaction.
            # Session state keeps chat history available between reruns.
            if "history" not in st.session_state:
                st.session_state.history = []

            # Load API keys and other secret values from the .env file.
            load_dotenv()

            # This list is currently unused because history is stored in session state.
            chat_history = []

            # OpenAI model used when an answer is not found in local course data.
            model = ChatOpenAI(
                model="gpt-4o",
                temperature=0.7,
                max_completion_tokens=1000,
            )

            # State schema passed between the chatbot workflow steps.
            class ChatState(TypedDict):
                user_input: str
                response: str
                history: list

            # Search local ITM course data before requesting a generated answer.
            def find_course(user_input):
                for course in itm_university["courses"]:
                    if course["name"].lower() in user_input.lower():
                        return course
                return None

            # Answer from local data first, or delegate to the AI model when needed.
            def chatbot_node(state: ChatState) -> dict:
                query = state["user_input"]
                history = state.get("history", [])

                if any(word in query.lower() for word in tool_keywords):
                    prompt = Tool_Prompt(
                        name=st.session_state.user_name,
                        Query=query,
                    )

                    response = model.invoke(prompt)

                    updated_history = history + [
                        HumanMessage(content=query),
                        AIMessage(content=response.content),
                    ]

                    return {
                        "response": response.content,
                        "history": updated_history,
                    }

                else:
                    course = find_course(query)

                    # Return locally stored fees and duration without an API request.
                    if course:
                        response = (
                            f"{course['name']}\nFees: {course['fees']}"
                            f"\nDuration: {course['duration']}"
                        )
                        updated_history = history + [
                            HumanMessage(content=query),
                            AIMessage(content=response),
                        ]

                        # Keep recent messages so the prompt does not become too large.
                        updated_history = updated_history[-10:]

                        return {
                            "response": response,
                            "history": updated_history,
                        }

                    # Give the model its instructions and previous conversation context.
                    message = [
                        SystemMessage(content=system_prompt(st.session_state.user_name))
                    ]
                    message.extend(history)
                    message.append(HumanMessage(content=query))

                    result = model.invoke(message)

                    # Save the latest exchange back into the chat transcript.
                    updated_history = history + [
                        HumanMessage(content=query),
                        result,
                    ]

                    # Keep recent messages so the prompt stays small and fast.
                    updated_history = updated_history[-10:]

                    return {
                        "response": result.content,
                        "history": updated_history,
                    }

            # Build a simple LangGraph workflow with one chatbot node.
            builder = StateGraph(ChatState)
            builder.add_node("chatbot", chatbot_node)
            builder.set_entry_point("chatbot")
            builder.add_edge("chatbot", END)
            graph = builder.compile()

            # Display old chat messages after each Streamlit rerun.
            for i, msg in enumerate(st.session_state.history):
                if isinstance(msg, HumanMessage):
                    st.chat_message("user", avatar=USER_AVATAR).write(msg.content)
                elif isinstance(msg, AIMessage):
                    col_msg, col_speak = st.columns([8, 1])

                    with col_msg:
                        st.chat_message("assistant", avatar=AI_AVATAR).write(msg.content)

                    with col_speak:
                        if st.button("🔊", key=f"speak_{i}"):
                            st.session_state.audio_file = text_to_speech(msg.content)

            # Chat input box shown at the bottom of the page.
            user_input = st.chat_input("Ask about courses, fees, admission, hostel...")

            # Sidebar contains university information and common user actions.
            with st.sidebar:
                st.image("ITM University.png", width=300)
                st.header("ITM University Gwalior")
                st.write("Admission Helpline: 06264865609")
                st.write("Website: https://www.itmuniversity.ac.in")

                chat_clear, logout_but = st.columns(2)

                with chat_clear:
                    if st.button("Clear Chat", use_container_width=True):
                        st.session_state.history = []
                        st.session_state.audio_file = None
                        st.rerun()

                with logout_but:
                    # Reset session values before returning to the welcome screen.
                    if st.button("Logout", use_container_width=True):
                        st.session_state.history = []
                        st.session_state.user_name = None
                        st.session_state.audio_file = None
                        st.rerun()

                st.write("Quick questions:")
                quick_questions = {
                    "MBA Fees": "What is MBA fee?",
                    "B.Tech Fee": "What is B.tech fee?",
                    "Placements": "What are the placements?",
                    "admission process": "What Is The admission process?",
                    "Courses": "How Many Courses in ITM Collage? Fees and Duration",
                }
                for title, question in quick_questions.items():
                    if st.button(title, use_container_width=True):
                        user_input = question

                with st.expander("What courses are available?"):
                    st.write(
                        "BTech, MBA, BCA, BBA, BSc Nursing, BPharm, DPharm, "
                        "BPT, LLB and more."
                    )

                with st.expander("What is the address?"):
                    st.write(
                        "NH-44, Bypass Turari, Jhansi Road, Gwalior (M.P.) 475001"
                    )

            # Run the chatbot when the user types a question or clicks a quick question.
            if user_input:
                st.chat_message("user", avatar=USER_AVATAR).write(user_input)

                # Send current input and previous history into the LangGraph workflow.
                with st.spinner("In Progress..."):
                    result = graph.invoke(
                        {
                            "user_input": user_input,
                            "response": "",
                            "history": st.session_state.history,
                        }
                    )

                # Save updated history and show the assistant response on the page.
                st.session_state.history = result["history"]

                col3, col4 = st.columns([8, 1])

                with col3:
                    st.chat_message("assistant", avatar=AI_AVATAR).write(
                        result["response"]
                    )
                with col4:
                    if st.button("🔊", key=f"speak_{len(st.session_state.history)}"):
                        st.session_state.audio_file = text_to_speech(result["response"])

            # Play generated speech after the user selects the speaker button.
            if st.session_state.audio_file:
                st.audio(st.session_state.audio_file)

            # Bottom action buttons for clearing the conversation.
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear Chat", use_container_width=True):
                    st.session_state.history = []
                    st.session_state.audio_file = None
                    st.rerun()
            with col2:
                if st.button("Delete History", use_container_width=True):
                    st.session_state.history = []
                    st.session_state.audio_file = None
                    st.success("Chat history cleared.")
                    st.stop()
        except Exception as e:
            # Show a friendly message instead of exposing only technical errors.
            st.warning(
                "Sorry, the chatbot service is temporarily unavailable. "
                "Please try again later."
            )
            st.error(str(e))
    else:
        st.error("Please Enter Valid Name")
        st.write("Use Only Alphabet [A to Z]")
        st.session_state.user_name = None
        sleep(3)
        st.rerun()
