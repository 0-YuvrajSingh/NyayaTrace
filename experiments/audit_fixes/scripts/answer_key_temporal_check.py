import json
import sys

def parse_year(val):
    if not val: return None
    try:
        return int(str(val)[:4])
    except ValueError:
        return None

def process_file(filepath, is_extension):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    if is_extension:
        entries = data['extension']['cases']
        top_keys = list(data.keys())
        first_keys = list(entries[0].keys())
    else:
        entries = [e for e in data['entries'] if e.get('status', 'evaluation') == 'evaluation']
        top_keys = list(data.keys())
        first_keys = list(entries[0].keys())
        
    print(f"\n--- {filepath} ---")
    print(f"Top-level keys: {top_keys}")
    print(f"First entry keys: {first_keys}")
    print(f"Entry count: {len(entries)}")
    
    for e in entries:
        if is_extension:
            case_id = e.get('query_record_id', e.get('candidate_case_id'))
            qy = e.get('query_year')
            auth_id = e.get('authority_source_id')
            auth_date = e.get('authority_decision_date')
            auth_year = e.get('authority_year')
        else:
            case_id = e.get('query_case_id')
            qy = e.get('query_decision_date')
            qy = parse_year(qy) if qy else None
            auth_id = e.get('authority_citation')
            auth_date = e.get('authority_decision_date')
            auth_year = parse_year(auth_date)
            
        qy_int = parse_year(qy) if qy else qy
        ay_int = parse_year(auth_date) if auth_date else auth_year
        if ay_int is None and auth_date and len(str(auth_date)) >= 10:
            if '-' in auth_date:
                parts = auth_date.split('-')
                if len(parts[-1]) == 4:
                    ay_int = int(parts[-1])
        
        status = 'missing'
        if qy_int is not None and ay_int is not None:
            if ay_int < qy_int:
                status = 'earlier'
            elif ay_int == qy_int:
                status = 'same-year'
            else:
                status = 'later'
                
        print(f"Case {case_id} (QY {qy_int}) -> Auth {auth_id} (Date {auth_date} / AY {ay_int}) [{status}]")

def main():
    try:
        with open('/repo/experiments/audit_fixes/answer_key_temporal_check_output.txt', 'w') as out_f:
            sys.stdout = out_f
            process_file('/repo/answer_key/authority_answer_key.json', False)
            process_file('/repo/answer_key/extension_v6/verified_7_case_extension.json', True)
    finally:
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    main()
