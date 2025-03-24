import streamlit as st
from main import initialize_chatbot, generate

# Initializing a session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []  # Initializing an empty list to store the conversation history.
if 'initialized' not in st.session_state:
    st.session_state.initialized = False  # Initializing a boolean to track if the chatbot has been initialized.

# Streamlit app
st.title("ClarkuBot - Your Virtual Assistant")  # Setting the title of the Streamlit app.
st.write("Ask me anything about Clark University!")  # Displaying a message to the user.

# Initialize chatbot
if not st.session_state.initialized:  # Checking if the chatbot has been initialized.
    with st.spinner("Initializing ClarkuBot and processing files..."):  # Displaying a spinner while initializing.
        client, model, conversation_history, files = initialize_chatbot()  # Initializing the chatbot.
        if client is not None:  # Checking if a chatbot was initialized successfully.
            st.session_state.client = client  # Storing the client in session state.
            st.session_state.model = model  # Storing the model in session state.
            st.session_state.conversation_history = conversation_history  # Storing the conversation history in session state.
            st.session_state.files = files  # Storing the uploaded files in session state.
            st.session_state.initialized = True  # Setting the initialized flag to True.
            st.success("ClarkuBot is ready!")  # Displaying a success message.
        else:
            st.error("Failed to initialize ClarkuBot. Please check your API key and files.")  # Displaying an error message.
            st.stop()  # Stopping the app execution.

# Display conversation history
for message in st.session_state.conversation:  # Iterating through the conversation history.
    if message['role'] == 'user':  # Checking if the message is from the user.
        st.markdown(f"**You:** {message['content']}")  # Displaying the user message.
    else:
        st.markdown(f"**ClarkuBot:** {message['content']}")  # Displaying the chatbot message.
    st.write("---")  # Displaying a separator between messages.

# User input
user_input = st.chat_input("Ask me a question...")  # Getting the user's input.

if user_input:
    st.session_state.conversation.append(
        {'role': 'user', 'content': user_input})  # Adding the user message to the conversation history.

    # Generate response
    with st.spinner("ClarkuBot is thinking..."):  # Displaying a spinner while generating the response.
        generate(
            st.session_state.client,
            st.session_state.model,
            st.session_state.conversation_history,
            user_input,
            st.session_state.files
        )  # Generateing the response.

        # Getting the last response from conversation history
        if st.session_state.conversation_history:
            last_response = st.session_state.conversation_history[-1].parts[
                0].text  # Extracting the last response from the conversation history.
            st.session_state.conversation.append({'role': 'assistant',
                                                  'content': last_response})  # Adding the chatbot's response to the conversation history.

    st.rerun()  # Rerun the Streamlit app to update the display.