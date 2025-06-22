# Themis - AI-Powered Legal Document Assistant
<p style="text-align: center;"> <a href="https://themis-wfyk.onrender.com">Homepage</a> | <a href="https://drive.google.com/file/d/1-wOSayhetrsw0OR_SP39Q1wbkjURgn6C/view?usp=sharing">Demo</a></p>

## Introduction

Themis is an intelligent legal assistant designed to streamline the analysis and review of legal documents. Leveraging the power of LLMs, Themis helps legal professionals and individuals quickly understand complex contracts and court cases, saving valuable time and effort.

## Features

Themis offers a range of powerful features:

*   **Contract Analysis & Review:** Get comprehensive insights into your contracts.
*   **Clause Identification:** Automatically identify and extract distinct clauses from legal documents.
*   **Termination Clause Extraction:** Specifically locate and pull out termination clauses.
*   **Court Case Summarization:** Generate concise summaries of lengthy court case documents.
*   **Case Metadata Extraction:** Extract key information like case number, appellant, respondent, and relevant facts.
*   **Case Outcome Prediction:**  Provides predictive insights into potential case outcomes.

## Setup

Follow these steps to set up Themis on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Tanmoy0077/Themis
    cd themis
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Create Environment File:**
    Create a file named `.env` in the root directory of the project.

4.  **Add API Keys:**
    Open the `.env` file and add your API keys like this:

    ```dotenv
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
    PINECONE_API_KEY=YOUR_PINECONE_API_KEY
    GROQ_API_KEY=YOUR_GROQ_API_KEY
    ```
    Replace `YOUR_GOOGLE_API_KEY`, `YOUR_PINECONE_API_KEY`, and `YOUR_GROQ_API_KEY` with your actual keys.

## Usage

To start the Themis application:

1.  Navigate to the project's root directory in your terminal.
2.  Run the main application file:
    ```bash
    python main.py
    ```
3.  This will start the Flask development server. Open your web browser and navigate to the address provided.

Now you can start using Themis to analyze your legal documents!
