# Silicon Overdrive RAG Q&A System

> The Silicon Overdrive Assessment is a technical evaluation of a RAG (Retrieval-Augmented Generation) Q&A system. This project demonstrates a practical application of Large Language Models (LLMs) and the vector embeddings that serve as the foundation for modern RAG pipelines and AI agents.

---

## Overview
In order to establish a RAG System ready for real world use, the following needs to be established: 

* 1. Obtaining the data and then cleaning it. This is necessary to establish the data in a format and state that it can be effectivley used for processing.
* 2. Chunking the data into smaller parts, so that they can be converted to an embedding vector. These will then be stored in a Relational Database.
* 3. Retrieving the data from the Database by use of the Cosine Simlariy Search (in this implementation).
* 4. Establishing an LLM API, and then as part of it's invocation, including the retrieved documents from the RAG Relational Database. A User Query is used to retrieve the documents from the RAG DB.
* 5. Providing the necessary functionaltiy to prevent hallucinations, such as citing the source of the retrieved documents frm the RAG DB.
* 6. And then finally, evaluating the reliablity of the RAG Q&A System, and it's ability to faithfully retrieve and present the most relevant document to the user query.

## 1. Ingestion & Chunking:
In order to setup the documents for RAG functionality in such a way that they can efficiently be retrieved, they need to be chunked and embedded to a Database. 
## 2. Retrieval: 
## 3. Generation: 
## 4. Hallucination Mitigation: 
## 4. Evaluation:

| Query | Source Document | Generated Answer | Faithfulness (Raw NLI) | Status |
| :--- | :--- | :--- | :--- | :--- |
| What is the primary benefit of writing? | Writing Briefly.txt | The primary benefit of writing besides communicating ideas is that it generates ideas. | **5.18** | ✅ Faithful |
| Why is it hard to reproduce SV in Japan? | Why Startups Condense in America.txt | Japan's less open immigration policies would hinder the creation of a diverse innovation environment. | **5.13** | ✅ Faithful |
| What prediction is made about Java? | The HundredYear Language.txt | The author predicts Java might not be successful due to concerns about hype and bureaucracy. | **5.50** | ✅ Faithful |
| How will web startups affect performance? | The Future of Web Startups.txt | Performance measurement will propagate back to high school, potentially reducing arbitrary criteria. | **3.57** | ⚠️ Partial |
| What is the 2nd biggest cause of startup death? | A Fundraising Survival Guide.txt | *I don't know the answer based on the provided context.* | **-0.37** | ❌ Failed |
| What was the 'flimsy' software the author worked on? | Six Principles for Making New Things.txt | *The provided context does not mention any 'flimsy' software.* | **-1.68** | ❌ Failed |
| What example is used for ideas 'under your nose'? | Six Principles for Making New Things.txt | *I don't know. The context does not include an example...* | **-1.62** | ❌ Failed |

---


## Tech Stack
List the primary languages, frameworks, and technologies used:
* **Backend:** Python (FastAPI / Pydantic)
* **Web Scraping:** BeautifulSoup4
* **RAG Vector DB:** Chroma 
* **Similarity Search Method:** Cosine Similarity Using all-MiniLM-L6-v2 model from sentence_transformers
* **Evaluation Model and Metric:** cross-encoder/nli-deberta-v3-small from sentence_transformers

---

## Getting Started

### Prerequisites
List the software or accounts needed before running the code.
* Python 3.10+
* A HuggingFace Account Setup. You will need to obtain an access token with permissions set to use the Inference API: https://huggingface.co/docs/hub/en/security-tokens
* A Unix Based Terminal

### Installation
1. **Clone the repository:**
   ```bash
   git clone git@github.com:JoeKiiru/Silicon_OverDrive_RAG.git
   cd Silicon_OverDrive_RAG

2. **Install the Python Packages**
   ```bash
   make install

3. **Login To HuggingFace locally, you will need to add your Access Token as input**
   ```bash
   hf auth login
4. **Download the datasets from https://paulgraham.com/articles.html**
   ```bash
   make scrape-data
5. **Process and Ingest the datasets into your local ChromaDB**
   ```bash
   make ingest-data
6. **Run the FastAPI Application to query the RAG Q&A System**
   ```bash
   make run
7. **To query the RAG Q&A System, you can use a curl request like so:**
   ```bash
   curl -X POST http://127.0.0.1:8000/query      -H "Content-Type: application/json"      -d '{"query": "What is VC Suckage"}'
8. **To evaluate the RAG Q&A System using a faithfulness metric, run the following:**
   ```bash
   make evaluate-rag
9. **To clean your local repositoru and therefore remove your virtual environment, run:**
   ```bash
   make clean