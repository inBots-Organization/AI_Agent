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


path = r"C:\Users\DELL\Downloads\9_image_1414.jpeg"
with open(path, "rb") as f:
    img_bytes = f.read()


if __name__ == "__main__":
    model_name = "gpt-4-turbo"
    prompt_file = "A_Prom1"   
    images = [
        img_bytes
    ]

    output = inspect_images(model_name, prompt_file, images)
    print(json.dumps(output, indent=2, ensure_ascii=False))
