from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from collections import Counter

model = SentenceTransformer("all-MiniLM-L6-v2")
db = chromadb.PersistentClient(path="chromadb")
collection = db.get_or_create_collection("docs")

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages)

def chunck_text(text, chunk_size=800, overlap=150):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start = (start + chunk_size) - overlap
    return chunks

def ingest(pdf_path):
    chunks = chunck_text(extract_text(pdf_path))
    embeddings = model.encode(chunks).tolist()
    collection.add(
        ids = [f"{pdf_path}-{i}" for i in range(len(chunks))],
        documents= chunks,
        embeddings= embeddings,
        metadatas= [{"source": pdf_path, "chunk": i} for i in range(len(chunks))]
    )


pdf_list = ["../data/all.pdf",
            "../data/Electronics for Dummies.pdf",
            "../data/make-electronics-excerpt.pdf",
            "../data/RP-008307-DS-2-pico-datasheet.pdf",
            "../data/SIK_v4_Book_Oct_25_FINAL.pdf"
            ]


for file in pdf_list:
    ingest(file)

data = collection.get(include=["metadatas"])
print(Counter(m["source"] for m in data["metadatas"]))