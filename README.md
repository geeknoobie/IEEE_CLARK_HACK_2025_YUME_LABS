# IEEE Clark Hack 2025 – Yume Labs: ClarkuBot
An AI-powered chatbot system designed to answer questions about Clark University, leveraging Google’s Gemini API for intelligent responses via a Streamlit frontend and Python backend. 

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [Repository Structure](#repository-structure)
5. [Setup & Installation](#setup--installation)
6. [Usage](#usage)

   * [Data & Knowledge Base](#data--knowledge-base)
   * [Streamlit Frontend (`app.py`)](#streamlit-frontend-apppy)
   * [Main Processing Logic (`main.py`)](#main-processing-logic-mainpy)
7. [Configuration & Environment](#configuration--environment)
8. [Dependencies & Requirements](#dependencies--requirements)
9. [Development Environment](#development-environment)
10. [License](#license)

---

## Project Overview

ClarkuBot is an AI-driven chatbot tailored for Clark University information, built during IEEE Clark Hack 2025 for the Yume Labs track. It integrates a Streamlit-based frontend with a Python backend that communicates with Google’s Gemini AI to process university-specific data (e.g., course catalogs, career services, general content) and provide real-time, context-aware responses to users.

The system automatically discovers and ingests various data files (CSV, TXT) containing Clark University knowledge and maintains conversation history to ensure continuity in multi-turn interactions.
---

## Key Features

* **Streamlit Frontend**:
  A user-friendly web interface (`app.py`) that allows users to ask questions about Clark University and view chatbot responses instantaneously.
* **Google Gemini AI Integration**:
  Utilizes Gemini API for generating intelligent responses with configurable parameters (temperature, top-p, top-k, max tokens).
* **Session State Management**:
  Maintains conversation history, initialization flags, and loaded files using Streamlit’s session state to preserve context across requests.
* **Automated File Processing**:
  Discovers and uploads `.csv` and `.txt` files from a designated directory into the Gemini knowledge base at initialization (`initialize_chatbot()`), enabling dynamic knowledge updates.
* **Modular Design**:
  Separation of concerns between data handling, AI interaction, and UI components, allowing easy extension to new data sources and features.

---

## System Architecture

The system operates in layered components:

1. **Frontend Interface (`app.py`)**

   * Built with Streamlit for rapid prototyping and deployment.
   * Manages user inputs, session state, and displays AI responses.
   * Communicates with the processing logic in `main.py`.

2. **Processing Logic (`main.py`)**

   * Initializes the chatbot by uploading data files to Gemini.
   * Handles message generation via a `generate()` function with parameters:

     * `temperature`: 0.5
     * `top_p`: 0.95
     * `top_k`: 40
     * `max_tokens`: 2048
     * Safety filters enforced for content.
   * Maintains a `conversation_history` list of user-assistant exchanges.

3. **Data & Knowledge Base**

   * Supports ingestion of multiple data file types (`*.csv`, `*.txt`, etc.).
   * Automatically processes any files in the project root or designated data folder during initialization.
   * Data files include:

     * **Course Catalog Data** (`*.csv`): Academic program details.
     * **University Content** (`*.txt`): General university information and policies.
     * **Career Services Data** (`*.csv`/`*.txt`): Internship/job guides, event schedules.

4. **AI Integration (Gemini API)**

   * Leverages Google’s Gemini for natural language understanding and generation.
   * Configuration via environment variables (API keys) for authentication. 
   * Implements a secure content-filtering pipeline to ensure compliance. 

---

## Repository Structure

```
IEEE_CLARK_HACK_2025_YUME_LABS/
├── README.md                   # This file
├── app.py                      # Streamlit frontend
├── main.py                     # Core processing logic (chatbot initialization & response generation)
├── data/                       # (Optional) Dedicated folder for CSV/TXT knowledge files
│   ├── course_catalog.csv
│   ├── university_content.txt
│   └── career_services.csv
├── config/                     # Configuration files
│   ├── .env                    # Environment variables (API keys, etc.)
│   └── secrets.toml            # Secure token storage
├── notebooks/                  # (Optional) Jupyter notebooks for exploration
│   └── data_inspection.ipynb
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container setup for development/production
└── .github/                    # CI/CD workflows (if any)
    └── workflows/
        └── python-app.yml      # Example GitHub Actions workflow
```

> **Note:** If `data/` folder is not present, the system will scan the project root for any `.csv` or `.txt` files and ingest them dynamically. 

---

## Setup & Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/geeknoobie/IEEE_CLARK_HACK_2025_YUME_LABS.git
   cd IEEE_CLARK_HACK_2025_YUME_LABS
   ```

2. **Create & Activate a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   * Copy `.env.example` (if provided) to `.env` and populate with your own Google Gemini API key and any other required tokens. For example:

     ```text
     GEMINI_API_KEY=your_gemini_api_key_here
     OTHER_SECRET=...
     ```
   * Alternatively, create `secrets.toml` with the same key-value pairs if your code is configured to read from it.
5. **(Optional) Build & Run via Docker**

   ```bash
   docker build -t clarkubot:latest .
   docker run --env-file .env -p 8501:8501 clarkubot:latest
   ```

   * This will serve the Streamlit app on `http://localhost:8501`.

---

## Usage

### Data & Knowledge Base

* **Automatic Discovery**:
  On first run, `main.py` scans the working directory (and/or `data/` folder) for any files ending in `.csv` or `.txt`.
* **Uploading to Gemini**:

  * Each discovered file is uploaded to Gemini using `client.files.upload()`.
  * `initialize_chatbot()` builds `conversation_history` entries that reference these uploads.
* **Supported Formats**:

  * Course catalogs and numeric data in CSV.
  * General university content in plain text.
  * Ensure file names clearly describe content (e.g., `course_catalog.csv`, `career_services.txt`).

### Streamlit Frontend (`app.py`)

1. **Run Streamlit App**

   ```bash
   streamlit run app.py
   ```
2. **User Interface Flow**

   * **Initialization**: On first access, `app.py` checks if `initialized` is `False`. It then calls `initialize_chatbot()` from `main.py` to ingest files and set up the conversation.
   * **User Question Input**: A text box appears for users to type questions about Clark University (courses, events, policies, etc.).
   * **Display Chat History**: All previous user-assistant messages are displayed in a scrollable area using Streamlit’s session state.
   * **Submit & Generate**: Upon hitting “Submit,” `app.py` calls `generate(user_input)` from `main.py`, appends the user message to `conversation_history`, sends it to Gemini, and displays the assistant’s response. 

### Main Processing Logic (`main.py`)

1. **Environment & Imports**

   * Loads environment variables (e.g., `GEMINI_API_KEY`) using `dotenv`.
   * Imports `google.genai` client, `os`, `streamlit`, and related utility modules. 

2. **`initialize_chatbot()` Function**

   * Scans for supported data files (`.csv`, `.txt`).
   * Uploads each file to Gemini via `client.files.upload()`.
   * Constructs an initial `conversation_history` list containing system-level prompts referencing the uploaded file IDs.
   * Sets `initialized = True` in Streamlit’s session state. 

3. **`generate(user_input)` Function**

   * Appends the new user message (wrapped in a `types.Message`) to `conversation_history`.
   * Calls `client.generate()` using `conversation_history` as context with parameters:

     ```python
     response = client.generate(
         model="gemini-pro",
         prompt=conversation_history,
         temperature=0.5,
         top_p=0.95,
         top_k=40,
         max_output_tokens=2048,
         safety_settings=[...]
     )
     ```
   * Extracts the assistant’s reply from `response.candidates[0].content`, appends it to `conversation_history`, and returns it to `app.py`. 

4. **Session State Keys**

   * `session_state['conversation']`: List of `{ "role": "user"/"assistant", "content": ... }`.
   * `session_state['initialized']`: Boolean to prevent reloading files on each rerun.
   * `session_state['client']`, `session_state['model']`: Gemini client and model references. 

---

## Configuration & Environment

* **`.env`**

  ```ini
  GEMINI_API_KEY=your_gemini_api_key
  ```
* **`secrets.toml`** (alternative)

  ```toml
  [credentials]
  gemini_api_key = "your_gemini_api_key"
  ```
* Ensure that your code in `main.py` references these variables:

  ````python
  from dotenv import load_dotenv
  import os

  load_dotenv()
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  client = genai.Client(api_key=GEMINI_API_KEY)
  ``` :contentReference[oaicite:26]{index=26}

  ````
* **Streamlit Session State**

  * Initializes on first run:

    ```python
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.conversation = []
    ```
  * After `initialize_chatbot()`, set `st.session_state.initialized = True`.
---

## Dependencies & Requirements

```txt
# Core
streamlit>=1.12.0
python-dotenv>=0.19.0
google-genai>=0.1.0                     # Google Gemini API client
toml>=0.10.2

# Utility
pandas>=1.3.5                          # If data inspection is needed in notebooks
```

* Verify exact versions in `requirements.txt` for reproducibility.

---

## Development Environment

* **Python Version**: 3.9+ recommended.

* **IDE**: VSCode, PyCharm, or any editor supporting Python and Streamlit debugging.

* **Development Container** (Optional):
  A `.devcontainer/devcontainer.json` can specify a Docker-based VSCode environment with all dependencies preinstalled. For example:

  ```json
  {
    "name": "ClarkuBot Dev Container",
    "build": {
      "dockerfile": "../Dockerfile"
    },
    "workspaceFolder": "/workspace",
    "extensions": [
      "ms-python.python",
      "ms-python.vscode-pylance",
      "ms-toolsai.jupyter"
    ]
  }
  ```


* **IDE Configuration**:

  * Ensure that `python.envFile` is set to `${workspaceFolder}/.env` in VSCode’s `settings.json`.
  * Configure Streamlit debugging:

    ```json
    {
      "name": "Python: Streamlit",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/app.py",
      "console": "integratedTerminal",
      "args": ["run"]
    }
    ```
