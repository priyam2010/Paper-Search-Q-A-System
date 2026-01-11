from pdf_loader import extract_text_from_pdf

text = extract_text_from_pdf("data/standard-treatment-guidelines.pdf")
print(text[:2000])