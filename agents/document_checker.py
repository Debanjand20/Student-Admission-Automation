from crewai import Agent, Task, Crew
from langchain.tools import tool

# Define a simple document verification tool
@tool
def verify_documents(application):
    """
    Verifies the student application for required fields and documents.

    This function checks if the application contains all the necessary fields:
    'name', 'dob', 'marks', and 'documents'. It then verifies that the required
    documents ('marksheet', 'id_proof') are present in the application's documents.

    Parameters:
        application (dict): A dictionary representing a student application.

    Returns:
        str: A message indicating which fields or documents are missing,
             or a success message if all validations pass.
    """
    required_fields = ["name", "dob", "marks", "documents"]
    missing_fields = [field for field in required_fields if field not in application]

    if missing_fields:
        return f"❌ Missing fields: {', '.join(missing_fields)}"

    # Required documents
    required_docs = ["marksheet", "id_proof"]
    uploaded_docs = application.get("documents", {})

    missing_docs = [doc for doc in required_docs if doc not in uploaded_docs]
    if missing_docs:
        return f"❌ Missing required documents: {', '.join(missing_docs)}"

    return "✅ All documents verified successfully."

# Define the agent with the tool converted to a dictionary.
document_checker = Agent(
    role="Document Checking Agent",
    goal="Verify uploaded admission documents and flag incomplete applications.",
    backstory="Expert in document validation with experience in university admissions.",
    tools=[verify_documents.dict()],  # Convert the StructuredTool to a dict
    verbose=True
)

# Function to run document check as a task
def run_doc_check(application):
    task = Task(
        description=f"Please validate this student application: {application}",
        agent=document_checker
    )
    crew = Crew(
        agents=[document_checker],
        tasks=[task],
        verbose=True
    )
    return crew.run()
