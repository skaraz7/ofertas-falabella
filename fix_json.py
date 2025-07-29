import json
import re

# Read the file with merge conflicts
with open('data/ofertas_falabella_completo.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove Git merge conflict markers
# Pattern to match merge conflict blocks
conflict_pattern = r'<<<<<<< HEAD:.*?\n(.*?)\n=======\n(.*?)\n>>>>>>> .*?\n'

def resolve_conflict(match):
    # Take the first version (HEAD) for now
    return match.group(1) + '\n'

# Remove all merge conflict markers
cleaned_content = re.sub(conflict_pattern, resolve_conflict, content, flags=re.DOTALL)

# Also remove any remaining conflict markers that might be standalone
cleaned_content = re.sub(r'<<<<<<< HEAD:.*?\n', '', cleaned_content)
cleaned_content = re.sub(r'=======\n', '', cleaned_content)
cleaned_content = re.sub(r'>>>>>>> .*?\n', '', cleaned_content)

# Fix trailing commas before closing brackets/braces
cleaned_content = re.sub(r',\s*([}\]])', r'\1', cleaned_content)

# Try to parse and reformat the JSON to ensure it's valid
try:
    data = json.loads(cleaned_content)
    # Write back the cleaned JSON
    with open('data/ofertas_falabella_completo.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("JSON file cleaned and validated successfully!")
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
    # Write the cleaned content anyway
    with open('data/ofertas_falabella_completo.json', 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print("Cleaned content written, but JSON may still have issues")