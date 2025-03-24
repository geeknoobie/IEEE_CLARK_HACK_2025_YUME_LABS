import streamlit as st
from main import initialize_chatbot, generate

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []  # Initialize an empty list to store the conversation history.
if 'initialized' not in st.session_state:
    st.session_state.initialized = False  # Initialize a boolean to track if the chatbot has been initialized.

# Streamlit app
st.title("ClarkBot - Your Virtual Assistant")  # Set the title of the Streamlit app.
st.write("Ask me anything about Clark University!")  # Display a message to the user.

# Initialize chatbot
if not st.session_state.initialized:  # Check if the chatbot has been initialized.
    with st.spinner("Initializing ClarkBot and processing files..."):  # Display a spinner while initializing.
        client, model, conversation_history, files = initialize_chatbot()  # Initialize the chatbot.
        if client is not None:  # Check if the chatbot was initialized successfully.
            st.session_state.client = client  # Store the client in session state.
            st.session_state.model = model  # Store the model in session state.
            st.session_state.conversation_history = conversation_history  # Store the conversation history in session state.
            st.session_state.files = files  # Store the uploaded files in session state.
            st.session_state.initialized = True  # Set the initialized flag to True.
            st.success("ClarkBot is ready!")  # Display a success message.
        else:
            st.error("Failed to initialize ClarkBot. Please check your API key and files.")  # Display an error message.
            st.stop()  # Stop the app execution.

# Display conversation history
for message in st.session_state.conversation:  # Iterate through the conversation history.
    if message['role'] == 'user':  # Check if the message is from the user.
        st.markdown(f"**You:** {message['content']}")  # Display the user message.
    else:
        st.markdown(f"**ClarkBot:** {message['content']}")  # Display the chatbot message.
    st.write("---")  # Display a separator between messages.

# User input
user_input = st.chat_input("Ask me a question...")  # Get the user's input.

if user_input:
    # Add user message to conversation
    st.session_state.conversation.append(
        {'role': 'user', 'content': user_input})  # Add the user message to the conversation history.

    # Generate response
    with st.spinner("ClarkBot is thinking..."):  # Display a spinner while generating the response.
        generate(
            st.session_state.client,
            st.session_state.model,
            st.session_state.conversation_history,
            user_input,
            st.session_state.files
        )  # Generate the response.

        # Get the last response from conversation history
        if st.session_state.conversation_history:
            last_response = st.session_state.conversation_history[-1].parts[
                0].text  # Extract the last response from the conversation history.
            st.session_state.conversation.append({'role': 'assistant',
                                                  'content': last_response})  # Add the chatbot's response to the conversation history.

    # Rerun to update the conversation display
    st.rerun()  # Rerun the Streamlit app to update the display.