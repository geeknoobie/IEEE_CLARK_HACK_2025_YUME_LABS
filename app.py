import streamlit as st
from main import initialize_chatbot, generate

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# Streamlit app
st.title("ClarkBot - Your Virtual Assistant")
st.write("Ask me anything about Clark University!")

# Initialize chatbot
if not st.session_state.initialized:
    with st.spinner("Initializing ClarkBot and processing files..."):
        client, model, conversation_history, files = initialize_chatbot()
        if client is not None:
            st.session_state.client = client
            st.session_state.model = model
            st.session_state.conversation_history = conversation_history
            st.session_state.files = files
            st.session_state.initialized = True
            st.success("ClarkBot is ready!")
        else:
            st.error("Failed to initialize ClarkBot. Please check your API key and files.")
            st.stop()

# Display conversation history
for message in st.session_state.conversation:
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**ClarkBot:** {message['content']}")
    st.write("---")

# User input
user_input = st.chat_input("Ask me a question...")

if user_input:
    # Add user message to conversation
    st.session_state.conversation.append({'role': 'user', 'content': user_input})
    
    # Generate response
    with st.spinner("ClarkBot is thinking..."):
        generate(
            st.session_state.client,
            st.session_state.model,
            st.session_state.conversation_history,
            user_input,
            st.session_state.files
        )
        
        # Get the last response from conversation history
        if st.session_state.conversation_history:
            last_response = st.session_state.conversation_history[-1].parts[0].text
            st.session_state.conversation.append({'role': 'assistant', 'content': last_response})
            
    # Rerun to update the conversation display
    st.rerun() 