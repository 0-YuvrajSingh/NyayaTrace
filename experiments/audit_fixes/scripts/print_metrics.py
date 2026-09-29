import json

def parse_e1():
    try:
        data = json.load(open('/repo/artifacts/e1_baseline_results.json'))
        print("e1_baseline_results.json:")
        print(f"  accuracy: {data['metrics'].get('accuracy')}")
        print(f"  macro_f1: {data['metrics'].get('macro_f1')}")
    except: pass

def parse_e3():
    try:
        data = json.load(open('/repo/artifacts/e3_e4_evidence_augmented_evaluation.json'))
        print("e3_e4_evidence_augmented_evaluation.json:")
        if 'metrics' in data:
            print(f"  accuracy: {data['metrics'].get('accuracy')}")
            print(f"  macro_f1: {data['metrics'].get('macro_f1')}")
        else:
            print(f"  metrics: {data.get('metrics')}")
    except: pass

def parse_week11():
    try:
        data = json.load(open('/repo/artifacts/week11_temporal_prerank_evaluation.json'))
        print("week11_temporal_prerank_evaluation.json:")
        if 'aggregate_metrics' in data:
            print(f"  Recall@5: {data['aggregate_metrics'].get('Recall@5')}")
            print(f"  Recall@100: {data['aggregate_metrics'].get('Recall@100')}")
        else:
            print(f"  aggregate_metrics: {data.get('aggregate_metrics')}")
    except: pass

def parse_e2():
    try:
        data = json.load(open('/repo/artifacts/e2_correction_manifest.json'))
        print("e2_correction_manifest.json:")
        if 'accepted_result_chunk_and_pool' in data:
            res = data['accepted_result_chunk_and_pool']['metrics']
            print(f"  accuracy: {res.get('accuracy')}")
            print(f"  macro_f1: {res.get('macro_f1')}")
    except: pass

if __name__ == '__main__':
    parse_e1()
    parse_e2()
    parse_e3()
    parse_week11()
