import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from groq import Groq
from datetime import datetime
import base64

load_dotenv()
text = """Ты опытный QA инженер. Проанализируй этот скриншот веб-страницы и найди:

1. ВИЗУАЛЬНЫЕ БАГИ — сломанная вёрстка, перекрывающиеся элементы, обрезанный текст
2. UX ПРОБЛЕМЫ — неочевидные кнопки, плохая навигация, непонятные элементы  
3. ДОСТУПНОСТЬ — низкий контраст, мелкий шрифт, отсутствие подписей
4. ПОДОЗРИТЕЛЬНЫЕ МЕСТА — что стоит проверить дополнительно

Отвечай структурированно. Если баг найден — опиши где именно на странице."""

def open_url(page, url):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    path_filename = f"C:/Users/Администратор/Desktop/AI_QA/screenshots/{filename}"
    page.goto(url, wait_until="load")
    page.screenshot(path=path_filename, full_page=True)
    work_ai(path_filename)

def work_ai(path_filename):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    with open(path_filename, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    )

    print(response.choices[0].message.content)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    open_url(page, "https://playwright.dev/python/")
    browser.close()