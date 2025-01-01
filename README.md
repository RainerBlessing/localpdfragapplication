# Python RAG application to query local PDF documents

## Installation Notes

- Copy .env.sample to .env and enter your Phidata and Groq API key.
  Define a collection name for your PDF data collection.
- Run "poetry install" to install the dependencies.
- run db.sh to create the DB docker container.

## Usage

- Copy PDF files to the pdfs subdirectory.
- run "python pdf_assistant.py". This will import the PDF files and run the
  query interface.
