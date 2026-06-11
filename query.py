# query.py
from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate,  MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from rich import print

load_dotenv()

# --- Configurazione (uguale a indicizza.py) ---
embedding = OllamaEmbeddings(
    model="bge-m3",
    base_url=os.getenv("OLLAMA_HOST")
)

connection_string = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

llm = ChatOllama(
    model="llama3.1:8b",
    base_url=os.getenv("OLLAMA_HOST"),
    temperature=0.4  
)

# --- Connessione al Vector Store esistente ---
vector_store = PGVector(
    embeddings=embedding,
    connection=connection_string,
    collection_name="clancker"
)

# --- Retriever: recupera i 3 chunk più simili alla domanda ---
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# --- Prompt RAG ---
template = ChatPromptTemplate.from_messages([
    ("system", 
    "Ti chiami Gino"
    "Rispondi sempre in italiano non superando 300 caratteri, utilizzando il contesto quando necessario."
    "Contesto:{contesto}"
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{domanda}")
])

#a = -1
chat_history = []

def rag_query(domanda: str) -> str:
    """Cerca i chunk rilevanti e genera una risposta contestualizzata."""
    # 1. Recupera i chunk più simili dal database
    chunk_rilevanti = retriever.invoke(domanda)

    # 2. Unisci il testo dei chunk in un unico blocco di contesto
    contesto = "\n\n---\n\n".join([c.page_content for c in chunk_rilevanti])

    # 3. Costruisci e invia il prompt
    chain = template | llm
    risposta = chain.invoke({
        "contesto": contesto,
        "domanda": domanda,
        "chat_history": chat_history
    })

    #a += 1

    # Salva nella memoria
    """
    if a > 10:
        chat_history = []
        a = 0
    """
    
    chat_history.append(HumanMessage(content=domanda))
    chat_history.append(AIMessage(content=risposta.content))


    return risposta.content

# --- Test ---
if __name__ == "__main__":
    while True:
        domanda = input("Tu: ").strip()
        print("\n")

        if domanda.lower() in ['esci']:
            break
        elif domanda.lower() in ['/reset']:
            chat_history = []
        else:
            print("[bold yellow]Gino: " + rag_query(domanda) + "[/bold yellow]\n")