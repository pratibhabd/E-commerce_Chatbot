from pathlib import Path
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from uuid import uuid4
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_MODEL"]

faqs_path = Path(__file__).parent / "faq_data.csv"
chroma_client = chromadb.Client()
collection_name_faq = "faqs"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "sentence-transformers/all-miniLM-L6-v2"
)

def ingest_faq_data(path):
     if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
         print("Ingesting FAQ data in chromadb...")
         collection = chroma_client.get_or_create_collection(
             name=collection_name_faq,
             embedding_function=ef)

         df = pd.read_csv(path)
         docs = df['question'].to_list()
         metadata = [{'answer': ans} for ans in df['answer'].to_list()]
         ids=[f'id_{i}' for i in range(len(docs))]

         collection.add(
             documents=docs,
             metadatas=metadata,
             # ids=[str(uuid4()) for _ in range(len(docs))]  # one ID per document
             ids=ids
         )

         print(f"FAQ Data sucessfully ingested into Chroma Collection{collection_name_faq}")
     else:
         print(f"Collection name {collection_name_faq} already exists!")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(collection_name_faq)
    result = collection.query(
        query_texts = [query],
        n_results = 2
    )
    return result

def faq_chain(query):
    result = get_relevant_qa(query)
    context = "".join([r.get("answer") for r in result["metadatas"][0]])

    answer  = generate_answer(query, context)
    return answer

def generate_answer(query, context):
    prompt = f"""
    Given the question and context below generate the answer based on the context only,
    if you don't find the answer inside the context then say I don't know.
    Donot make things up.

    QUESTION : {query}
    CONTEXT : {context}
    """

    # Initialize client — Groq() automatically reads GROQ_API_KEY from env
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    model_name = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    chat_completion = client.chat.completions.create(
        model = model_name,  # you can change to mixtral-8x7b or llama3-70b
        messages=[
            {"role": "user", "content":prompt,}
        ],
    )
    # Print the assistant's reply
    return chat_completion.choices[0].message.content

if __name__ == '__main__':
    ingest_faq_data(faqs_path)
    query = "Are there any ongoing offers?"
    #result = get_relevant_qa(query)
    answer = faq_chain(query)
    print(answer)
