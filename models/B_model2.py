from openai import OpenAI

import os, json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)
def load_prompt(prompt_name):
    with open(f"prompts/{prompt_name}.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

def inspect_images(model_name, prompt_file, image_urls):
    system_prompt = load_prompt(prompt_file)

    user_message = [
        {"type": "text", "text": "Inspect these images and return the JSON described in the system prompt."}
    ] + [
        {"type": "image_url", "image_url": {"url": url}} for url in image_urls
    ]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    resp = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.0
    )

    answer = resp.choices[0].message.content


    try:
        result = json.loads(answer)
    except Exception:
        result = {"raw": answer}

    return result

if __name__ == "__main__":
    model_name = "gpt-4-turbo"
    prompt_file = "B_Promp2"   
    images = [
        "https://drivemanagementgroup.jotform.com/uploads/!team_252604236568056/231796495163972/5727653497911078576/9_image_1414.jpeg"
    ]

    output = inspect_images(model_name, prompt_file, images)
    print(json.dumps(output, indent=2, ensure_ascii=False))
