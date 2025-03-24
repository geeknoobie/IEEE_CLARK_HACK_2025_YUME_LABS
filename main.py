import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from google.api_core import exceptions as google_exceptions

load_dotenv()

def initialize_chatbot(directory="."): #added directory parameter
    """Initializes the chatbot, including setting up the client, uploading files from the specified directory,
    and defining the initial conversation history.
    Returns a tuple: (client, model, conversation_history, files)
    """
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("The GEMINI_API_KEY environment variable is not set.")

    # Initialize the genai client using the API key from environment variables.
    client = genai.Client(api_key=gemini_api_key)

    try:
        files = []
        # Iterating over files in our specified directory.
        for filename in os.listdir(directory):
            if filename.endswith(".csv") or filename.endswith(".txt"): #only upload .csv and .txt
                filepath = os.path.join(directory, filename)

                # Upload the file to the genai service and store the file object.
                files.append(client.files.upload(file=filepath))

        if not files: # check for file upload.
            print("No .csv or .txt files found in the specified directory.")
            return None, None, None, None

    except Exception as e:
        print(f"Error uploading files: {e}")
        return None, None, None, None  # Return None values on error
    # Specifying the model to use for generating responses.
    model = "gemini-2.0-flash"

    # Initializing the conversation history with a system prompt and an initial model response and structure .
    conversation_history = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""You are ClarkBot, an intelligent and helpful virtual assistant. You have access to information from the files I uploaded. Use that information to answer my questions. If you cannot find the information, please inform the user that you do not have the information available."""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Okay, I understand..."""),  # Your initial model response
            ],
        ),
    ]
    # Add data to our conversation history.
    for file in files:
        conversation_history.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=file.uri,
                        mime_type=file.mime_type,
                    ),
                ],
            ),
        )
        conversation_history.append(
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(text=f"Okay, I have processed the {file.name} data."),
                ],
            ),
        )
    # Returns the client, model, conversation history, and uploaded files.
    return client, model, conversation_history, files



def generate(client, model, conversation_history, user_input, files):
    """Generates a response and updates the conversation history.

    Args:
        client: The genai client.
        model: The model name.
        conversation_history:  The list of Content objects.
        user_input: The user's input string.
        files: The uploaded files list.
    """
    # Appending the user's input to the conversation history.
    conversation_history.append(
        types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
    )
    # Configuring the generation settings.
    generate_content_config = types.GenerateContentConfig(
        temperature=0.5,
        top_p=0.95,
        top_k=40,
        max_output_tokens=2048,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_LOW_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_LOW_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_CIVIC_INTEGRITY", threshold="BLOCK_LOW_AND_ABOVE"),
        ],
        response_mime_type="text/plain",
    )

    try:
        # Generating the response stream from the model.
        response_stream = client.models.generate_content_stream(
            model=model,
            contents=conversation_history,
            config=generate_content_config,
        )
        # Processing the response stream and print the response.
        response_text = ""
        for chunk in response_stream:
            if chunk.text:
                print(chunk.text, end="")
                response_text += chunk.text
        print()
        # Appending the model's response to the conversation history.
        conversation_history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=response_text)])
        )

    except google_exceptions.ClientError as e:
        # Handling API errors
        print(f"API Error: {e}")
    except Exception as e:
        # Handling other unexpected errors.
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    directory = "." #current directory
    # Initializing the chatbot
    client, model, conversation_history, files = initialize_chatbot(directory)
    if client is None:  # Checking for initialization errors
        exit()

    while True:
        print("Hey welcome to ClarkBot! your one stop solution to all questions clark ")
        user_input = input("Ask me a question: ")
        if user_input.lower() == 'exit':
            break
        if files: #Making sure files are uploaded
            generate(client, model, conversation_history, user_input, files)
        else:
            print("File upload failed, cannot continue.")
            break