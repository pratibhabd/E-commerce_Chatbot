from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL")

talk_prompt = """You are an expert in answering or chatting with the user, 
answer only as much required"""

def small_talk_chain(question):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    model_name = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": talk_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.2,
        #max_tokens=1024
    )
    return chat_completion.choices[0].message.content.strip()


if __name__ == '__main__':
    query = "How are you?"
    res = small_talk_chain(query)
    #print(res)

