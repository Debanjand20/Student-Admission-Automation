from crewai import Agent, Task, Crew
from langchain.tools import tool
from state.admission_status import MAX_SEATS, save_admission, get_status_report

MIN_MARKS = 75  # Eligibility criteria

@tool
def check_eligibility(application):
    marks = application.get("marks", 0)
    name = application.get("name", "Unknown")

    # Check current shortlist count
    current = get_status_report()["shortlisted"]

    if current >= MAX_SEATS:
        return f"❌ University capacity reached ({MAX_SEATS} students). Cannot admit {name}."

    if marks >= MIN_MARKS:
        save_admission(application)
        return f"✅ {name} shortlisted successfully with {marks}% marks."
    else:
        return f"❌ {name} not eligible. Required: {MIN_MARKS}%, Got: {marks}%"

shortlisting_agent = Agent(
    role="Shortlisting Agent",
    goal="Evaluate students and select eligible candidates based on marks and capacity.",
    backstory="An academic assistant who ensures only eligible candidates are admitted.",
    tools=[check_eligibility],
    verbose=True
)

def run_shortlisting(application):
    task = Task(
        description=f"Shortlist this student if eligible: {application}",
        agent=shortlisting_agent
    )
    crew = Crew(
        agents=[shortlisting_agent],
        tasks=[task],
        verbose=True
    )
    return crew.run()
