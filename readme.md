# Translation Script with Llama3

This Python script utilizes the Llama3 model via an API to translate text from French to Hindi, verify translations, and log results into a `.strings` file.


## Introduction

The Translation Script with Llama3 is designed to automate the translation of text from French to Hindi (or any other languages) using Large Language Model, running locally in the system. It verifies translations and logs them into a `.strings` file. This script is useful for tasks requiring automated translation and verification processes.

- **Objective**: Automate translation from one language to other using the Llama3 model or any other equivalent ollama compatible llm model, with verification, and log results.
- **Features**:
  - Translate text from one language to other using Llama3.
  - Verify translations using Llama3.
  - Log translated key-value pairs into a `.strings` file.
- **Technologies**: Python, requests library, Llama3, Ollama.

## Installation

To run the script, follow these installation steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/translation-script.git
   cd translation-script
   python main.py

## More Details

- **Retry Mechanism**: The script automatically retries translation for failed or inaccurate translations up to five times before marking it as "[Translation Failed]".
- **Real-time Updates**: Each translated key-value pair is logged immediately into the output file (translated_string.strings) once confirmed as accurate.
- **Error Handling**: Errors during translation or verification are logged to the console, providing transparency on translation status.
- **Performance**: The script includes a built-in rate limiter to avoid overwhelming the Ollama API and ensure reliable translation performance.
