import re

keywords = ["decision_date", "case_date", "<=", "Temporal", "missing", "unresolved", "predefined", "Eligible("]

def contains_keyword(text):
    for kw in keywords:
        if kw.lower() in text.lower() or kw in text:
            return True
    return False

def main():
    lines = open('/repo/experiments/audit_fixes/spec_full_text.txt', encoding='utf-8').read().split('\n')
    
    with open('/repo/experiments/audit_fixes/spec_temporal_quotes.md', 'w', encoding='utf-8') as f:
        f.write("# Spec Quotes for Temporal Rule\n\n")
        
        f.write("## Operational Definitions Section\n")
        for i in range(46, 56):
            if lines[i].strip():
                f.write(f"{lines[i]}\n")
                
        f.write("\n## Temporal Integrity Protocol Section\n")
        for i in range(148, 154):
            if lines[i].strip():
                f.write(f"{lines[i]}\n")
        
        f.write("\n## All Keyword Matches in Document\n")
        # To determine section heading, we can just keep track of the last capitalized short line or something similar
        # but to keep it simple, we just print the matching lines. The prompt says "plus section heading and paragraph/table origin"
        
        current_heading = "Start of Document"
        for idx, line in enumerate(lines):
            if not line.strip(): continue
            if "[PARAGRAPH]" in line and len(line) < 100 and not line.endswith('.') and line.isupper():
                current_heading = line.replace('[PARAGRAPH]', '').strip()
            elif "[PARAGRAPH]" in line and len(line) < 60 and not line.endswith('.'):
                current_heading = line.replace('[PARAGRAPH]', '').strip()
                
            if contains_keyword(line):
                # Don't duplicate if already in the two sections above, but printing all is safer.
                f.write(f"- **Section:** {current_heading}\n")
                f.write(f"  **Origin:** {line}\n\n")

if __name__ == '__main__':
    main()
