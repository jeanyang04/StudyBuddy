import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

if __name__ == "__main__":
    # Example usage
    pdf_path = "example.pdf"  # Replace with your test file
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)
