# ucl-de2
# MSIN0166 Individual Coursework — Tuhan Sapumanage

This repo contains a RAG-based AI information assistant with the following features:

- Ingests data from multiple sources: Web scraping/API+MongoDB (Hacker News Stories & Comments), PDFs (EU AI Act), CSVs (benchmarks)
- Handles both structured and unstructured data formats, including Parquet, CSV, PDF, and raw JSON.
- Implements preprocessing pipelines for cleaning, deduplication, chunking, and anonymisation of data to prepare it for LLM input.
- Ensures data privacy and sensitivity handling, including HTML decoding and PII anonymisation (emails, usernames, URLs).
- Uses secure handling of secrets via .env and GitHub Codespaces secrets to avoid hardcoded credentials.
- Combines and enriches datasets using PySpark with fuzzy matching to simulate a scalable enterprise data transformation workflow.
- Builds semantic vector indexes using Chroma and FAISS for scalable Retrieval-Augmented Generation (RAG).
- Deploys a full RAG-based LLM assistant using Langchain and Gemini API, with prompt chaining and strict citation instructions to reduce hallucinations.
- Implements prompt versioning, hallucination detection, and logging of similarity scores to Neptune for LLMOps-style observability.
- Tracks complete data lineage using W3C PROV standard, capturing all stages from ingestion to model response.
- Provides a modular, reproducible, and Docker-compatible pipeline structure, with environment and dependency isolation.
- Follows enterprise best practices across MLOps/LLMOps including structured codebase, observability, provenance, and automation.

`msin0166-individual.ipynb` — Core development notebook  
`docker/msin0166-individual-docker.py` — Flask API deployment script  
`store/` — Vector DBs  
`data/` — PDFs, CSVs  
`chunks/` — Preprocessed, chunked content  
