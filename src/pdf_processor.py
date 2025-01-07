import PyPDF2
import sys
import os

def extract_text_from_pdf(file_path, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    
    # Generate output file path using the PDF filename
    pdf_filename = os.path.basename(file_path)
    output_filename = os.path.splitext(pdf_filename)[0] + ".txt"
    output_path = os.path.join(output_folder, output_filename)
    
    # Write the extracted text to file
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(text.strip())
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pdf_processor.py <pdf_path> <output_folder>")
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    output_folder = sys.argv[2]
    output_file = extract_text_from_pdf(pdf_path, output_folder)
    print(f"Text extracted and saved to: {output_file}")
