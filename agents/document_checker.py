from langchain.tools import tool

@tool
def verify_documents(application):
    """
    Verifies that the application contains all required fields.
    
    Checks if the provided application dictionary includes the fields:
    'name', 'dob', 'marks', and 'documents'. Returns a status and message 
    indicating whether the verification succeeded or lists the missing fields.
    
    Parameters:
        application (dict): The application data.
        
    Returns:
        dict: A dictionary with a status ('success' or 'error') and a message.
    """
    required_fields = ["name", "dob", "marks", "documents"]
    missing_fields = [field for field in required_fields if field not in application]
    
    if missing_fields:
        return {"status": "error", "message": f"Missing fields: {', '.join(missing_fields)}"}
    return {"status": "success", "message": "All documents are verified."}



from crewai import Agent, Task, Crew
from langchain.tools import tool

# Define a simple document verification tool
@tool
def verify_documents(application):
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

# Define the agent
document_checker = Agent(
    role="Document Checking Agent",
    goal="Verify uploaded admission documents and flag incomplete applications.",
    backstory="Expert in document validation with experience in university admissions.",
    tools=[verify_documents],
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
