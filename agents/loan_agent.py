from crewai import Agent, Task, Crew
from langchain.tools import tool
from state.admission_status import loan_summary, save_admission

# Total budget for loans
UNIVERSITY_LOAN_BUDGET = 500000  # ₹5,00,000

@tool
def process_loan(application):
    request = application.get("loan_request", 0)
    name = application.get("name", "Unknown")

    # No loan requested
    if request <= 0:
        save_admission(application, loan=False)
        return "ℹ️ No loan requested."

    # Check if sufficient budget is available
    if request > loan_summary["remaining_budget"]:
        save_admission(application, loan=False)
        return f"❌ Loan request of ₹{request} denied due to insufficient funds. Remaining budget: ₹{loan_summary['remaining_budget']}"

    # Approve loan
    loan_summary["remaining_budget"] -= request
    loan_summary["approved"].append((name, request))
    save_admission(application, loan=True)

    return f"✅ Loan approved for ₹{request}. Remaining budget: ₹{loan_summary['remaining_budget']}"

# Define the Loan Agent
loan_agent = Agent(
    role="Loan Processing Agent",
    goal="Process student loan requests within the university's allocated budget.",
    backstory="A finance-aware AI assistant that handles all student loan applications and maintains budget discipline.",
    tools=[process_loan],
    verbose=True
)

# Function to execute loan processing
def run_loan_check(application):
    task = Task(
        description=f"Review this loan request and process it: {application}",
        agent=loan_agent
    )
    crew = Crew(
        agents=[loan_agent],
        tasks=[task],
        verbose=True
    )
    return crew.run()
