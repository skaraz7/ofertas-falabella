import json
import re

def fix_json_file():
    # Read the file
    with open('data/ofertas_falabella_completo.json', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Original file size:", len(content))
    
    # Remove all Git merge conflict markers
    lines = content.split('\n')
    cleaned_lines = []
    skip_until_end = False
    
    for line in lines:
        # Skip merge conflict markers
        if line.startswith('<<<<<<< HEAD:'):
            skip_until_end = False
            continue
        elif line.startswith('======='):
            skip_until_end = True
            continue
        elif line.startswith('>>>>>>> '):
            skip_until_end = False
            continue
        
        # Only add lines that are not in the "skip" section
        if not skip_until_end:
            cleaned_lines.append(line)
    
    # Join back the lines
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Fix common JSON issues
    # Remove trailing commas before closing brackets/braces
    cleaned_content = re.sub(r',(\s*[}\]])', r'\1', cleaned_content)
    
    # Fix any double commas
    cleaned_content = re.sub(r',,+', ',', cleaned_content)
    
    # Remove empty lines that might cause issues
    cleaned_content = re.sub(r'\n\s*\n', '\n', cleaned_content)
    
    print("Cleaned file size:", len(cleaned_content))
    
    # Try to parse the JSON
    try:
        data = json.loads(cleaned_content)
        print("JSON is valid!")
        
        # Write back the properly formatted JSON
        with open('data/ofertas_falabella_completo.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("File successfully cleaned and reformatted!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"JSON error at line {e.lineno}, column {e.colno}: {e.msg}")
        
        # Write the cleaned content for manual inspection
        with open('data/ofertas_falabella_completo_cleaned.json', 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        # Try to find and show the problematic area
        lines = cleaned_content.split('\n')
        start = max(0, e.lineno - 5)
        end = min(len(lines), e.lineno + 5)
        
        print(f"\nProblematic area around line {e.lineno}:")
        for i in range(start, end):
            marker = " >>> " if i == e.lineno - 1 else "     "
            print(f"{marker}{i+1:4d}: {lines[i]}")
        
        return False

if __name__ == "__main__":
    fix_json_file()