import re
import chardet

def find_abbreviations(file_path):
    abbreviations = []

    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding'] or 'latin-1'
        
        try:
            text = raw_data.decode(encoding)
            pattern = r'\b[A-Z]{3,}\b'
            matches = re.findall(pattern, text)
            abbreviations = list(set(matches))
        except UnicodeDecodeError:
            print(f"Unable to decode the file using encoding: {encoding}")
    
    return abbreviations

# Usage
file_path = 'F:/Pro Learn/doc.docx'
result = find_abbreviations(file_path)
print(result)
