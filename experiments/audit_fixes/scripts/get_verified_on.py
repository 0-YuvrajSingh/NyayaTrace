import json

def main():
    data = json.load(open('/repo/answer_key/authority_answer_key.json'))
    cases = ['1977_99', '1980_217', '1980_133', '1978_33', '1981_187', '1980_222', '1977_145', '1981_55', '1980_105', '2013_35']
    for e in data['entries']:
        if e.get('query_case_id') in cases:
            print(f"{e['query_case_id']}: {e.get('verified_on', 'MISSING')}")

if __name__ == '__main__':
    main()
