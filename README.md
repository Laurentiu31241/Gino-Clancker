# Gino Clancker

Gino parlerà con te utilizzando le informazioni che gli fornirai in un file di testo "document.txt".
Ti servirà però un qualcosa da usare come server remoto brochaccio.
La situa dovrebbe esser qualcosa del genere:

```
TUO PC (client)
│
│  codice Python + LangChain
│
├──► SERVER REMOTO
│       ├── Ollama  →  modello llama3.1:8b  (LLM)
│       ├── Ollama  →  modello bge-m3        (Embedding)
│       └── PostgreSQL + pgvector            (Vector Database)
│
└──► RISPOSTA al tuo terminale
```

### I componenti

| Componente | Strumento | Ruolo |
|---|---|---|
| **LLM** | `llama3.1:8b` via Ollama | Genera le risposte in linguaggio naturale |
| **Embedding** | `bge-m3` via Ollama | Converte il testo in vettori numerici |
| **Vector DB** | PostgreSQL + pgvector | Salva e cerca i vettori (per il RAG) |
| **Framework** | LangChain | Collega tutto insieme |
| **Configurazione** | python-dotenv | Gestisce le credenziali in modo sicuro |


## 1 - Pullappa la repository

Io quando Git Bash:

```
git clone https://github.com/utente/progetto.git
cd progetto
python -m venv .venv
source .venv/bin/activate        # (source .venv/Scripts/activate se su Windows)
pip install -r requirements.txt
```

## 2 - Crea un file .env

Crea il file .env nella cartella che contiene le seguenti info:

```
# Indirizzo del server remoto
OLLAMA_HOST= # http://POSTGRES_HOST:11434

# Credenziali PostgreSQL
POSTGRES_HOST= # indirizzo IP
POSTGRES_PORT= # di solito è 5432
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Esempio popo tanto generico:

```
OLLAMA_HOST=http://127.0.67.1:11434

POSTGRES_HOST=127.0.67.1
POSTGRES_PORT=5432
POSTGRES_DB=db_mio
POSTGRES_USER=io
POSTGRES_PASSWORD=password1234
```

## 3 - Crea un file document.txt

Crea un file document.txt contenente tutte le informazioni che Gino conoscerà.
Consiglio di mandare a capo spesso.

## 4 - Esegui i file python

Sempre su Git Bash o su altro, bho vedi te cosa ti piace:

```
python ind.py # solo all'inizio o quando modifichi document.txt
python query.py # ti fà chattare con il bro
```

## 5 - Chatta con il Gino

Fai domande e lui ti risponderà
Per uscire dal programma scrivi: esci
Per fargli dimenticare la conversazione che stavi avendo: /reset
Se Gino diventa estremamente lento dopo una 20 di domande consiglio di fare /reset

Bho cambia te il codice di ind.py e query.py se vuoi sperimentare.
Mi dispiace se hai voluto legger questo file per intero.

Questo README.md non è serio.
