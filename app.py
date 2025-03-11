# app.py - Main Streamlit application

import streamlit as st
import time
from agent.llm_service import LLMService
from config import APP_TITLE, DEBUG_MODE

# Initialize the AI service
ai_service = LLMService()

# Set page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🍽️",
    layout="wide"
)

# Application title and description
st.title(f"🍽️ {APP_TITLE}")
st.markdown("""
Welcome to FoodieSpot Restaurant Reservations! I can help you find restaurants and make reservations.

This application is powered by a custom AI model that understands natural language queries.
            
How to use this:
            Use keywords like: "List down cuisines", "List down locations" or "List down features" to find the available cuisines, locations and features.

            Search restaurants by choose cuisines, locations and features. If required option not available, it will provide a recommended option.

            Check availablity of restaurant by choosing the restaurant, "date(any format)", time and "seat count" with "availability" keyword in the query.
            
            And Finally, proceed with the reservation by mentioning ur "Name". e.g. - Make the reservation for Smith.
""")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("How can I help you today?")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display assistant response with a spinner
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Process the query
        response = ai_service.process_query(user_input)
        
        # Display debug information if in debug mode
        if DEBUG_MODE and response.get("tool_calls"):
            with st.expander("Debug Information"):
                st.json({
                    "tool_name": response.get("debug_info", {}).get("tool_name"),
                    "tool_args": response.get("debug_info", {}).get("tool_args"),
                    "tool_response": response.get("debug_info", {}).get("tool_response")
                })
        
        # Update the message placeholder with the actual response
        message_placeholder.markdown(response["response"])
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["response"]})

# Sidebar with options
with st.sidebar:
    st.header("Options")
    
    if st.button("New Conversation"):
        # Reset the conversation
        st.session_state.messages = []
        ai_service.reset_conversation()
        st.rerun()
    
    st.divider()
    
    # Debug mode toggle
    if st.checkbox("Debug Mode", value=DEBUG_MODE):
        st.session_state.debug_mode = True
    else:
        st.session_state.debug_mode = False
    
    st.divider()
    
    # About section
    st.header("About")
    st.markdown("""
    **FoodieSpot Restaurant Reservations**
    
    An AI-powered restaurant reservation system.
    
    This application helps you find restaurants and make reservations using natural language.
    """)