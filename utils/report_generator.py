from state.admission_status import get_status_report

def generate_summary_report():
    status = get_status_report()
    report = f"""
📊 Admission Summary Report

✅ Total Shortlisted: {status['shortlisted']}
🎓 Students Admitted: {len(status['students'])}
💰 Total Loan Budget Left: ₹{status['loan_remaining']}

Approved Loans:
----------------
"""
    for name, amount in status['approved_loans']:
        report += f"- {name}: ₹{amount}\n"

    report += "\nAdmitted Students:\n------------------\n"
    for s in status['students']:
        report += f"- {s['name']} (Marks: {s['marks']}) | Loan Approved: {'Yes' if s['loan_approved'] else 'No'}\n"

    return report
