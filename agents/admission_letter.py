from crewai import Agent, Task, Crew
from langchain.tools import tool
import datetime

# Define the fee structure
FEE_STRUCTURE = {
    "tuition": 50000,
    "hostel": 30000,
    "exam": 5000
}

# Tool to generate admission letter content
@tool
def generate_admission_documents(application):
    name = application.get("name", "Student")
    date = datetime.date.today().strftime("%d-%m-%Y")
    total_fee = sum(FEE_STRUCTURE.values())

    letter = f"""
    -------------------------
    🏫 University Admission Letter
    -------------------------
    Date: {date}

    Dear {name},

    Congratulations! You have been successfully admitted to our university.

    Please find the fee structure below:

    - Tuition Fee: ₹{FEE_STRUCTURE['tuition']}
    - Hostel Fee: ₹{FEE_STRUCTURE['hostel']}
    - Exam Fee: ₹{FEE_STRUCTURE['exam']}

    Total Payable: ₹{total_fee}

    Kindly pay the fees before the deadline to confirm your admission.

    Regards,  
    Admission Office
    """

    return letter

# Define the agent
letter_agent = Agent(
    role="Student Counsellor",
    goal="Send final admission letters and fee slips to selected students.",
    backstory="A warm communicator responsible for guiding students post-admission.",
    tools=[generate_admission_documents],
    verbose=True
)

# Function to run the letter generation
def run_admission_letter(application):
    task = Task(
        description=f"Generate an admission letter and fee slip for the student: {application}",
        agent=letter_agent
    )
    crew = Crew(
        agents=[letter_agent],
        tasks=[task],
        verbose=True
    )
    return crew.run()
