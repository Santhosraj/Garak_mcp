import requests

AZURE_ENDPOINT = "https://opeanai-eastus.openai.azure.com/"
API_KEY = ""
MODEL = "gpt-4o"  # Latest GPT-4 model
API_VERSION = "2024-07-01-preview"  # Latest API version

def azure_model(prompt):
    url = f"{AZURE_ENDPOINT}openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        # Azure returns choices[0].message.content for chat models
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Azure API Error] {e}" 