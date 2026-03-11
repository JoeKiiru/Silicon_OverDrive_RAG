# Silicon Overdrive RAG Q&A System

> The Silicon Overdrive Assessment is a technical evaluation of a RAG (Retrieval-Augmented Generation) Q&A system. This project demonstrates a practical application of Large Language Models (LLMs) and the vector embeddings that serve as the foundation for modern RAG pipelines and AI agents.

---

## Overview
In order to establish a RAG System ready for real world use, the following needs to be established: 

* 1. Obtaining the data and then cleaning it. This is necessary to establish the data in a format and state that it can be effectively used for processing.
* 2. Chunking the data into smaller parts, so that they can be converted to an embedding vector. These will then be stored in a Relational Database.
* 3. Retrieving the data from the Database by use of the Cosine similarity Search (in this implementation).
* 4. Establishing an LLM API, and then as part of it's invocation, including the retrieved documents from the RAG Relational Database. A User Query is used to retrieve the documents from the RAG DB.
* 5. Providing the necessary functionality to prevent hallucinations, such as citing the source of the retrieved documents from the RAG DB.
* 6. And then finally, evaluating the reliability of the RAG Q&A System, and it's ability to faithfully retrieve and present the most relevant document to the user query.

## 1. Ingestion & Chunking:
The documents are obtained from: https://paulgraham.com/articles.html, which contains a list of links pointing to the essays that will be the datasets for the RAG System.
Therefore in order to do so, **BeautifulSoup4** was used to download each essay, which were all stored in **src/ingestion/dataset**.

Next, in order to setup the documents for RAG functionality in such a way that they can efficiently be retrieved, they need to be chunked and embedded to a Database. The chunking code can be found in **src/ingestion/chunking.py**. 

The chunking strategy used is **Sentence Aware**, where each document is broken down into a list of sentences. This is more effective because the context of the current sentence is maintained, but this technique also overlaps more than one sentence to further emphasise the context. This is done so up to a maximum chunk size of 500 characters.

The next step is to then ingest the chunks to the RAG DB. In addition to the chunks being ingested, each chunk needs to be converted to a vector embedding, which will be used to efficiently retrieve the documents. This is done so using the **all-MiniLM-L6-v2** model to embed the chunks. The database used to store the chunks and embeddings is Chroma, an open-source Vector Database.

Additionally, the source of the document chunk and embedding vector is included as part of the table entry in the Chroma DB. This will be used to mitigate hallucinations.

A limitation of making use of a **Sentence Aware** chunking strategy, is that for a very long sentence, or even paragraph once the maximum chunk size is exceeded, the context will not be as relevant. The whole document would need to be considered, especially if it contains a lot of text, therefore a more thorough chunking strategy would be needed. There is also the context window that would need to be considered, as each chunk used in the generation phase may be too large for the Chat LLM and the Embedding LLM to process (of course up to a very high chunk size).
## 2. Retrieval:
The retrieval from the Chroma Vector DB is done by making use of Cosine Similarity. The user query is converted to a vector embedding automatically when querying from the Chroma Vector DB (making use of the Chroma DB **collection** object). The user query is then used to compare with the embedding vectors for each document, as part of the Cosine Similarity Search, which finds the documents embedding vectors that are the most similar to the user query embedding vector. Therefore, the documents that correlate to the user query (so in context with the user query) are obtained.
## 3. Generation:
The retrieved documents from the Chroma Vector DB are then included as part of a prompt to an LLM API, which essentially analyses the retrieved documents, and checks to see if it matches the user query. The LLM then responds to a query, providng the context from the RAG DB. If the context does not make sense, or nothing of value is provided from the RAG DB, the LLM just answers that it doesn't know.

The HuggingFace Inference API is used, where the **Qwen/Qwen2.5-72B-Instruct** is the chat model integrated as part of the RAG System. This is all consolidated as part of a simple FastAPI Application that contains a query post request endpoint, where it can be invoked to query the LLM API and the RAG DB. Additionally, the source of the consolidated documents is included in the response (as instructed as part of the prompt), where the file name of the document is used.
## 4. Hallucination Mitigation: 
To mitigate hallucinations, citations were used, where the retrieved document's file name was included as part of the response from the LLM API. This ensure that the LLM can show where it got it's information from. If no source is provided, then it is not a valid answer, and the LLM responds that it does not know.

Perhaps a secondary LLM can be used to verify that the user query matches the response from the LLM. A middle-man LLM Judge, to verify that the LLM is not hallucinating?
## 4. Evaluation:
The sentence_transformer **cross-encoder/nli-deberta-v3-small** model is used to evaluate the RAG Q&A System. This is done so by making use of sample queries in json format, where for each json, there is a user query and the expected response from the LLM, which the evaluation model will use as part of it's analysis. The evaluation process is specifically checking for **Faithfulness**, as this is effective as part of the RAG System, as since the source data is already available, in order for the RAG System to be useful and reliable, it would need to be faithful to it's source data.

The following is a table of the evaluation results:
| Query | Source Document | Generated Answer | Faithfulness (Raw NLI) | Status |
| :--- | :--- | :--- | :--- | :--- |
| What is the primary benefit of writing? | Writing Briefly.txt | The primary benefit of writing besides communicating ideas is that it generates ideas. | **5.18** | ✅ Faithful |
| Why is it hard to reproduce SV in Japan? | Why Startups Condense in America.txt | Japan's less open immigration policies would hinder the creation of a diverse innovation environment. | **5.13** | ✅ Faithful |
| What prediction is made about Java? | The HundredYear Language.txt | The author predicts Java might not be successful due to concerns about hype and bureaucracy. | **5.50** | ✅ Faithful |
| How will web startups affect performance? | The Future of Web Startups.txt | Performance measurement will propagate back to high school, potentially reducing arbitrary criteria. | **3.57** | ⚠️ Partial |
| What is the 2nd biggest cause of startup death? | A Fundraising Survival Guide.txt | *I don't know the answer based on the provided context.* | **-0.37** | ❌ Failed |
| What was the 'flimsy' software the author worked on? | Six Principles for Making New Things.txt | *The provided context does not mention any 'flimsy' software.* | **-1.68** | ❌ Failed |
| What example is used for ideas 'under your nose'? | Six Principles for Making New Things.txt | *I don't know. The context does not include an example...* | **-1.62** | ❌ Failed |

A possible solution to improve the evaluation results, is by making use of a more comprehensive retrieval process, such as a hybrid approach, where in addition to Cosine Similarity, a keyword search can be used to see if the user query has any keywords that can be found in the document, which is a great way to remove any retrieved documents that are not faithful, and therefore making the quality of retrieved documents compared a lot more better and reliable. This at the same time can help with choosing from similar documents, as a document with more keywords from the user query than other documents may be the most relevant document to the user query.

## 5. Next steps to improve the solution.

Going forward, deploying and hosting the RAG Q&A System would be the way to go. This would require finding a cloud service such as AWS, where various services can be used to enhance the offering, in terms of availablity, scalability, and better processing capabilities. An architecture of AWS Services including Vector DB offerings such as Aurora RDS Postgresql.

For documents that are quite similar to each other, and in order to more effectively retrieve them at a faster or more efficient rate, GraphRAG can also be considered, where similar documents can be clustered as part of a group of connected nodes, making it eaiser to search for the similar documents while traversing through the Graph RAG. Amazon Neptune can be used for this implementation.

---




## Tech Stack
List the primary languages, frameworks, and technologies used:
* **Backend:** Python (FastAPI / Pydantic)
* **Web Scraping:** BeautifulSoup4
* **RAG Vector DB:** Chroma 
* **Similarity Search Method:** Cosine Similarity using **all-MiniLM-L6-v2** model from sentence_transformers for ingestion.
* **Evaluation Model and Metric:** **cross-encoder/nli-deberta-v3-small** from sentence_transformers

---

## Getting Started

### Prerequisites
List the software or accounts needed before running the code.
* Python 3.10+
* A HuggingFace Account Setup. You will need to obtain an access token with permissions set to use the Inference API: https://huggingface.co/docs/hub/en/security-tokens
* A Unix-Based Terminal

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