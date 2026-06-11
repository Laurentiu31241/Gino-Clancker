# indicizza.py
from dotenv import load_dotenv
import os
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import psycopg2 # modifica

load_dotenv()

# --- Configurazione ---
embedding = OllamaEmbeddings(
    model="bge-m3",
    base_url=os.getenv("OLLAMA_HOST")
)

# Stringa di connessione PostgreSQL
connection_string = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

# --- Documenti di esempio ---
# In un progetto reale, qui caricheresti file .txt, .pdf, ecc.

testi = []

with open("document.txt", "r") as f:
    for riga in f:
        testi.append(riga.strip())

print(testi)


# Crea oggetti Document da LangChain
documenti = [Document(page_content=testo) for testo in testi]

# --- Chunking ---
# RecursiveCharacterTextSplitter divide i testi in pezzi
# chunk_size: max caratteri per chunk
# chunk_overlap: quanti caratteri si sovrappongono tra chunk adiacenti
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
chunks = splitter.split_documents(documenti)
print(f"Documenti originali: {len(documenti)}")
print(f"Chunk dopo la divisione: {len(chunks)}")

# --- Salvataggio nel Vector DB ---
# PGVector crea automaticamente la tabella nel DB se non esiste
vector_store = PGVector.from_documents(
    documents=chunks,
    embedding=embedding,
    connection=connection_string,
    collection_name="clancker",   # nome della "collezione" nel DB
    pre_delete_collection=True        # ricrea la collezione ogni volta (utile in fase di test)
)

print("Indicizzazione completata! I chunk sono stati salvati in PostgreSQL.")