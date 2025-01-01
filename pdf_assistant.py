from typing import List, Optional

import os
import typer
from dotenv import load_dotenv
from phi.assistant import Assistant
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.model.groq.groq import Groq
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.vectordb.pgvector import PgVector2

load_dotenv()

collection = os.getenv('COLLECTION')
llm_id = os.getenv('LLM')
db_url = os.getenv('DB_URL')

knowledge_base = PDFKnowledgeBase(
    path="pdfs",
    vector_db=PgVector2(collection=collection, db_url=db_url),
    model=Groq(id=llm_id),
)

knowledge_base.load()

storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)


def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        # Show tool calls in the response
        show_tool_calls=True,
        # Enable the assistant to search the knowledge base
        search_knowledge=True,
        # Enable the assistant to read the chat history
        read_chat_history=True,
    )
    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    assistant.cli_app(markdown=True)


if __name__ == "__main__":
    typer.run(pdf_assistant)
