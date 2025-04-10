from fpdf import FPDF
import datetime
import os

def generate_admission_letter_pdf(application, fee_structure, save_path="generated_letters"):
    os.makedirs(save_path, exist_ok=True)

    name = application.get("name", "Student")
    date = datetime.date.today().strftime("%d-%m-%Y")
    total = sum(fee_structure.values())

    # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="🏫 University Admission Letter", ln=True, align="C")
    pdf.ln(10)

    pdf.multi_cell(0, 10, txt=f"""
Date: {date}

Dear {name},

Congratulations! You have been successfully admitted to our university.

Please find the fee structure below:
- Tuition Fee: ₹{fee_structure['tuition']}
- Hostel Fee: ₹{fee_structure['hostel']}
- Exam Fee: ₹{fee_structure['exam']}

Total Payable: ₹{total}

Kindly pay the fees before the deadline to confirm your admission.

Regards,
Admission Office
    """)

    filename = f"{save_path}/{name.replace(' ', '_')}_admission_letter.pdf"
    pdf.output(filename)
    return filename
