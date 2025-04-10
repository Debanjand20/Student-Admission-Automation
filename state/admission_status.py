# In-memory admission state (shared across agents)
# You can later replace this with SQLite or a real database

admitted_students = []
loan_summary = {
    "approved": [],  # List of (name, amount)
    "remaining_budget": 500000  # ₹5,00,000 starting
}
shortlist_count = 0
MAX_SEATS = 100

def save_admission(application, loan=False):
    """Save student admission info to the global list."""
    global shortlist_count
    if shortlist_count < MAX_SEATS:
        shortlist_count += 1
        admitted_students.append({
            "name": application.get("name", "Unknown"),
            "marks": application.get("marks", "NA"),
            "loan_approved": loan
        })

def get_status_report():
    """Returns full state for the Director Bot and Report Generator."""
    return {
        "shortlisted": shortlist_count,
        "total_admitted": len(admitted_students),
        "loan_remaining": loan_summary["remaining_budget"],
        "approved_loans": loan_summary["approved"],
        "students": admitted_students
    }
