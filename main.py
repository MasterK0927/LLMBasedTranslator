import requests
import re
import time
import json

# Local Ollama API URL for chat endpoint
OLLAMA_API_URL = 'https://b28e-2409-40e1-10f0-778-10a6-d5cb-3a07-b19b.ngrok-free.app/api/chat'

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def append_to_file(file_path, content):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content)

def is_hindi(text):
    return any('\u0900' <= char <= '\u097F' for char in text)

def translate_text(text):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'llama3:latest',
        'messages': [
            {"role": "system", "content": "You are a translator that translates text from French to Hindi, who returns the translated text omly, and doesnt returns any other text just the translated text. Just return the translated text not the jargon or explanations. Don't translate the technical terms in hindi,just convert them in hindi and also keep the urls in english only."},
            {"role": "user", "content": text}
        ]
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data, stream=False)
        response.raise_for_status()
        
        translated_content = ""
        print(f"Translation in progress for text: '{text}'")
        for line in response.iter_lines():
            if line:
                try:
                    response_data = json.loads(line.decode('utf-8'))
                    if 'message' in response_data and 'content' in response_data['message']:
                        translated_content += response_data['message']['content']
                        print("Partial translation received:", response_data['message']['content'])
                    if 'done' in response_data and response_data['done']:
                        break
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    continue

        translated_content = translated_content.strip()
        print(f"Translation completed for text: '{text}' -> '{translated_content}'")
        return translated_content

    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return "[Translation Failed]"

def parse_and_translate(input_file, output_file):
    content = read_file(input_file)
    pattern = re.compile(r'(".*?") = "(.*?)";')
    matches = pattern.findall(content)

    total_batches = len(matches)
    current_batch = 1

    for key, value in matches:
        print(f"Processing {current_batch}/{total_batches}...")
        if not is_hindi(value):
            translated_value = translate_text(value)
            entry = f'{key} = "{translated_value}";\n'
            print(f"{value} -> {translated_value}")  # Log original and translated text
            time.sleep(1)  # Sleep to avoid rate limiting
        else:
            entry = f'{key} = "{value}";\n'
        
        append_to_file(output_file, entry)  # Write the translation to the file in real-time
        current_batch += 1

    print("Translation completed.")

if __name__ == "__main__":
    input_file = 'BraveShared.strings'
    output_file = 'translated_string.strings'
    
    # Clear the output file if it already exists
    open(output_file, 'w').close()
    
    parse_and_translate(input_file, output_file)
