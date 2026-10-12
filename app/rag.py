import os
from openai import OpenAI

def  retrieve(question, k=4):
    q_emb = model.encode([question]).tolist()
    result = collection.query(
        query_embeddings=q_emb,
        n_results=k)
    return result['documents'][0]

def answer(question):
    chunks = retrieve(question)
    context = "\n---\n".join(chunks)
    prompt = f"""Answer the question based on the context below. If the question can't be answered based on the context, say "I don't know"

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

text, chunks, usage = answer("How much SRAM does the RP2040 have?")
print(text)
print(usage)