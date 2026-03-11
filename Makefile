PYTHON = python3
VENV = env
BIN = $(VENV)/bin

.PHONY: all install run clean

all: install run

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt

# Run the python script
scrape-data:
	$(BIN)/python -m src.ingestion.web_scraper

ingest-data:
	$(BIN)/python -m src.ingestion.main

evaluate-rag:
	$(BIN)/python -m src.evaluation.evaluate

run:
	$(BIN)/python -m src.app

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +