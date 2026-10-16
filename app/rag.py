import os
from openai import OpenAI
from app.ingest import model, collection
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(

    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = "gemini-3-flash-preview"


def  retrieve(question, k=6):
    q_emb = model.encode([question]).tolist()
    result = collection.query(
        query_embeddings=q_emb,
        n_results=k)
    return result['documents'][0]

def answer(question):
    chunks = retrieve(question)
    context = "\n---\n".join(chunks)
    prompt = f"""You are a helpful electronics tutor for a beginner.
Use the context below to answer the question. Base your answer on the context and do not add facts that are not in the context..

- If the context fully answers the question, answer clearly.
- If it answers only part, give that part and say what is missing.

Context:
{context}

Question: {question}"""

    # 2. Send the prompt
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    # 3. Pull out the two things you need
    text = response.choices[0].message.content
    usage = {
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
    }
    return text, chunks, usage

text, chunks, usage = answer("What does an electronics usually consist of?")
print(text)
print(usage)
print(collection.count())