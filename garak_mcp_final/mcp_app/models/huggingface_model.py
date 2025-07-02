import requests
import os

def huggingface_model(prompt):
    headers = {
        "Authorization": f"Bearer {os.environ.get('HUGGINGFACEHUB_API_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200
        }
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    elif isinstance(result, list) and "output" in result[0]:
        return result[0]["output"]
    else:
        return str(result)
