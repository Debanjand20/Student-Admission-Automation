from crewai import Agent, Task, Crew
from langchain.tools import tool
from state.admission_status import get_status_report

# Tool to generate overview of admission status
@tool
def admission_overview(_):
    status = get_status_report()
    summary = f"""
🎓 Admission Process Overview
-----------------------------
✅ Total Shortlisted: {status['shortlisted']}
📥 Total Admitted: {status['total_admitted']}
💰 Loan Budget Remaining: ₹{status['loan_remaining']}
🏦 Approved Loans: {len(status['approved_loans'])}

📚 Admitted Students:
{', '.join([s['name'] for s in status['students']]) if status['students'] else 'None yet'}
"""
    return summary

# Define the director bot agent
director_bot = Agent(
    role="University Director Assistant",
    goal="Answer the university director’s queries about the admission process in real-time.",
    backstory="An intelligent assistant aware of all admission activities, designed to help the university director with real-time insights.",
    tools=[admission_overview],
    verbose=True
)

# Function to run chatbot query
def run_director_query(query):
    task = Task(
        description=f"The director asked: {query}. Use current admission status to answer.",
        agent=director_bot
    )
    crew = Crew(
        agents=[director_bot],
        tasks=[task],
        verbose=True
    )
    return crew.run()
