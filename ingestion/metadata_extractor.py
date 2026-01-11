import re 
def extract_title(text:str) -> str:
    lines = text.split("\n")
    return lines[0][:200]
def extract_abstract(text:str) -> str:
    match = re.search(r"abstract(.+?)introduction",text,re.S|re.I)
    return match.group(1).strip() if match else ""
def extract_authors(text:str):
    lines = text.split("/n")
    return lines[1].split(",") if len(lines) > 1 else[]


